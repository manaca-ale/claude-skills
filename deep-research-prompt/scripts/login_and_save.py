"""
Open Gemini with persistent profile, handle login, save session.

Usage:
    python login_and_save.py          # Open browser, log in manually, session is auto-saved
    python login_and_save.py --check  # Just check if session is still valid

The persistent profile at ~/.gemini-playwright-profile stores cookies, localStorage,
and session data. Once logged in, all future runs reuse this session automatically.
"""

import argparse
import asyncio
import sys
from pathlib import Path

PROFILE_DIR = Path.home() / ".gemini-playwright-profile"
GEMINI_URL = "https://gemini.google.com/app"


async def open_and_login(check_only: bool = False):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("ERROR: pip install playwright && playwright install chromium")
        sys.exit(1)

    PROFILE_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            str(PROFILE_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = context.pages[0] if context.pages else await context.new_page()

        print(f"Opening {GEMINI_URL}...")
        await page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(3)

        if "accounts.google.com" in page.url:
            if check_only:
                print("NOT LOGGED IN — session expired or first run")
                await context.close()
                return False

            print("=" * 60)
            print("LOGIN REQUIRED")
            print("Please log in to Google in the browser window.")
            print("Complete any 2FA verification if prompted.")
            print("The session will be saved automatically.")
            print("=" * 60)

            # Wait for redirect back to Gemini (up to 5 min for 2FA)
            try:
                await page.wait_for_url("**/gemini.google.com/**", timeout=300000)
                await asyncio.sleep(3)
                print("\nLogin successful! Session saved to persistent profile.")
                print(f"Profile location: {PROFILE_DIR}")
            except Exception:
                print("\nTimeout waiting for login. Try again.")
                await context.close()
                return False
        else:
            print("Already logged in! Session is valid.")
            if check_only:
                await context.close()
                return True

        # Verify we're on Gemini
        title = await page.title()
        print(f"Page title: {title}")
        print(f"URL: {page.url}")

        if not check_only:
            print("\nSession is saved. You can close the browser now.")
            print("Press Ctrl+C to exit, or the browser will close in 10 seconds.")
            try:
                await asyncio.sleep(10)
            except KeyboardInterrupt:
                pass

        await context.close()
        return True


def main():
    parser = argparse.ArgumentParser(description="Gemini login with persistent session")
    parser.add_argument("--check", action="store_true", help="Just check if session is valid")
    args = parser.parse_args()

    result = asyncio.run(open_and_login(check_only=args.check))
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
