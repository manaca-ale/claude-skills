"""
Standalone Gemini Deep Research automation via Playwright.

Two modes:
  Full:    python gemini_deep_research.py --prompt "Your research prompt"
  Wait:    python gemini_deep_research.py --wait-for-completion --output result.md
           (attaches to already-open Playwright browser and polls until done)

Options:
  --prompt TEXT           Prompt text to send
  --prompt-file PATH     Read prompt from file
  --output PATH          Output file (default: ~/AppData/Local/Temp/deep_research_result.md)
  --wait-for-completion  Skip sending, just poll the current page until done and extract
  --poll-interval N      Seconds between polls (default: 30)
  --max-wait N           Max seconds to wait (default: 900 = 15 min)

Requires:
  pip install playwright && playwright install chromium

Uses a persistent browser profile at ~/.gemini-playwright-profile so Google login
is preserved across runs. First run requires manual login.
"""

import argparse
import asyncio
import os
import sys
import tempfile
import time
from pathlib import Path

PROFILE_DIR = Path.home() / ".gemini-playwright-profile"
GEMINI_URL = "https://gemini.google.com/app"
DEFAULT_POLL = 30
DEFAULT_MAX_WAIT = 900


async def activate_deep_research(page):
    """Click Ferramentas > Deep Research in the Gemini UI."""
    print("[2/6] Activating Deep Research via Ferramentas menu...")

    # Click the "Ferramentas" button
    tools_btn = page.get_by_role("button", name="Ferramentas")
    try:
        await tools_btn.click(timeout=5000)
        await asyncio.sleep(1)
    except Exception:
        print("   WARNING: Could not find Ferramentas button. Trying alternative...")
        # Fallback: look for page_info icon button near input
        alt = page.locator('button:has(img[alt="page_info"])')
        await alt.first.click(timeout=5000)
        await asyncio.sleep(1)

    # Click Deep Research in the menu
    dr_item = page.get_by_role("menuitemcheckbox", name="Deep Research")
    try:
        await dr_item.click(timeout=5000)
        await asyncio.sleep(1)
        print("   Deep Research activated!")
    except Exception:
        print("   ERROR: Deep Research not found in Ferramentas menu.")
        print("   Please activate it manually in the browser.")
        input("   Press Enter when ready...")


async def insert_prompt(page, prompt: str):
    """Insert prompt text into the Gemini input field."""
    print("[3/6] Inserting prompt...")

    textbox = page.get_by_role("textbox", name="Insira um comando para o")
    await textbox.click(timeout=5000)
    await asyncio.sleep(0.5)

    # Use evaluate + textContent for long prompts (fill truncates at newlines)
    await textbox.evaluate(
        "(el, text) => { el.textContent = text; el.dispatchEvent(new Event('input', {bubbles: true})); }",
        prompt,
    )
    await asyncio.sleep(1)
    print(f"   Inserted {len(prompt)} chars")


async def send_and_confirm(page):
    """Click send, wait for research plan, and click Start research."""
    print("[4/6] Sending prompt...")

    # Click send button
    send_btn = page.get_by_role("button", name="Enviar mensagem")
    try:
        await send_btn.click(timeout=5000)
    except Exception:
        # Fallback: press Enter
        await page.keyboard.press("Enter")
    await asyncio.sleep(5)

    print("[5/6] Waiting for research plan and confirming...")
    # Wait for the "Start research" button (appears after ~15-30s)
    for _ in range(12):  # up to 2 minutes
        try:
            start_btn = page.locator('[data-test-id="confirm-button"]')
            if await start_btn.is_visible(timeout=1000):
                await start_btn.click()
                print("   Research plan confirmed! Deep Research is running...")
                return True
        except Exception:
            pass

        # Also try text-based selectors
        for text in ["Start research", "Iniciar pesquisa"]:
            try:
                btn = page.get_by_role("button", name=text)
                if await btn.is_visible(timeout=500):
                    await btn.click()
                    print("   Research plan confirmed! Deep Research is running...")
                    return True
            except Exception:
                continue

        await asyncio.sleep(10)

    print("   WARNING: Could not find Start research button.")
    print("   Please confirm manually in the browser if needed.")
    input("   Press Enter when research is running...")
    return True


async def wait_for_completion(page, poll_interval: int, max_wait: int) -> str:
    """Poll until Deep Research completes, then extract the result."""
    print(f"[Polling] Waiting up to {max_wait}s (checking every {poll_interval}s)...")
    start = time.time()

    while time.time() - start < max_wait:
        await asyncio.sleep(poll_interval)
        elapsed = int(time.time() - start)

        # Check if still running: look for "stop" icon (present during generation)
        try:
            stop_icons = await page.locator('img[alt="stop"]').count()
            # Also check for "Exportar para as Planilhas" (present when done)
            export_btns = await page.get_by_role("button", name="Exportar para as Planilhas").count()

            if stop_icons == 0 and export_btns > 0:
                print(f"   [{elapsed}s] Research complete! Extracting result...")
                break
            elif stop_icons > 0:
                print(f"   [{elapsed}s] Still researching...")
                continue
            else:
                # No stop icon but no export either — might be transitioning
                print(f"   [{elapsed}s] Checking state...")
                continue
        except Exception as e:
            print(f"   [{elapsed}s] Check error: {e}")
            continue
    else:
        print(f"   Timeout after {max_wait}s. Attempting extraction anyway...")

    # Extract the result from the side panel
    result_text = ""

    # Strategy 1: Find headings that indicate Deep Research output
    try:
        # The result appears in a panel with h1 headings
        headings = page.locator("h1")
        count = await headings.count()
        for i in range(count):
            text = await headings.nth(i).inner_text(timeout=2000)
            if len(text) > 20 and "Gemini" not in text and "Conversa" not in text:
                # Found the result heading, get its parent container
                parent = headings.nth(i).locator("..")
                result_text = await parent.inner_text(timeout=10000)
                if len(result_text) > 500:
                    break
    except Exception:
        pass

    # Strategy 2: Broader search
    if len(result_text) < 500:
        try:
            # Get all text from response containers
            containers = page.locator('[class*="response-container"]')
            count = await containers.count()
            if count > 0:
                result_text = await containers.last.inner_text(timeout=10000)
        except Exception:
            pass

    # Strategy 3: Full page text as fallback
    if len(result_text) < 500:
        try:
            result_text = await page.locator("main").inner_text(timeout=10000)
        except Exception:
            result_text = "[Could not extract result. Check the browser window.]"

    # Clean up UI artifacts
    lines = result_text.split("\n")
    clean_lines = [
        l for l in lines
        if "Abre em uma nova janela" not in l
        and "Exportar para as Planilhas" not in l
    ]
    return "\n".join(clean_lines)


async def run_full(prompt: str, output_path: str, poll_interval: int, max_wait: int):
    """Full flow: open browser, activate Deep Research, send prompt, wait, extract."""
    from playwright.async_api import async_playwright

    PROFILE_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"[1/6] Opening {GEMINI_URL}...")
        await page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(3)

        if "accounts.google.com" in page.url:
            print("LOGIN REQUIRED: Log in to Google in the browser window.")
            await page.wait_for_url("**/gemini.google.com/**", timeout=300000)
            await asyncio.sleep(3)

        await activate_deep_research(page)
        await insert_prompt(page, prompt)
        await send_and_confirm(page)

        result = await wait_for_completion(page, poll_interval, max_wait)

        Path(output_path).write_text(result, encoding="utf-8")
        print(f"\n[6/6] Result saved to: {output_path}")
        print(f"Result length: {len(result)} chars")

        await context.close()
        return result


async def run_wait_only(output_path: str, poll_interval: int, max_wait: int):
    """Attach to existing Playwright browser and wait for completion."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # Connect to existing browser via CDP
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
            print(f"Connected to existing browser at {page.url}")
        except Exception:
            # Fallback: open persistent context (reuses same profile)
            PROFILE_DIR.mkdir(exist_ok=True)
            context = await p.chromium.launch_persistent_context(
                str(PROFILE_DIR),
                headless=False,
                viewport={"width": 1280, "height": 900},
            )
            page = context.pages[0]
            print(f"Opened browser with persistent profile at {page.url}")

        result = await wait_for_completion(page, poll_interval, max_wait)

        Path(output_path).write_text(result, encoding="utf-8")
        print(f"\nResult saved to: {output_path}")
        print(f"Result length: {len(result)} chars")

        await context.close()
        return result


def main():
    parser = argparse.ArgumentParser(description="Gemini Deep Research automation")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="The research prompt text")
    group.add_argument("--prompt-file", help="Read prompt from file")
    group.add_argument("--wait-for-completion", action="store_true",
                       help="Skip sending, just poll and extract")
    parser.add_argument("--output", help="Output file path",
                        default=str(Path(tempfile.gettempdir()) / "deep_research_result.md"))
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL)
    parser.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT)

    args = parser.parse_args()

    try:
        from playwright.async_api import async_playwright  # noqa: F401
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium")
        sys.exit(1)

    if args.wait_for_completion:
        result = asyncio.run(run_wait_only(args.output, args.poll_interval, args.max_wait))
    else:
        prompt = (
            Path(args.prompt_file).read_text(encoding="utf-8")
            if args.prompt_file
            else args.prompt
        )
        result = asyncio.run(run_full(prompt, args.output, args.poll_interval, args.max_wait))

    print("\n--- Preview ---")
    print(result[:500])
    if len(result) > 500:
        print(f"\n... ({len(result) - 500} more chars)")


if __name__ == "__main__":
    main()
