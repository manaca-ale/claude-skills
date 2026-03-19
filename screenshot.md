---
name: screenshot
description: Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specific capture capabilities are unavailable and an OS-level capture is needed.
---

# Screenshot Capture

Follow these save-location rules every time:

1) If the user specifies a path, save there.
2) If the user asks for a screenshot without a path, save to the OS default screenshot location.
3) If Claude needs a screenshot for its own inspection, save to the temp directory.

## Tool priority

- Prefer tool-specific screenshot capabilities when available (for example: Playwright for browsers).
- Use this skill when explicitly asked, for whole-system desktop captures, or when a tool-specific capture cannot get what you need.

## Scripts location

All scripts are at `C:/Users/aleco/.codex/skills/screenshot/scripts/`.

## Windows (PowerShell helper)

Run the PowerShell helper:

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1"
```

Common patterns:

- Default location:

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1"
```

- Temp location (Claude visual check):

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1" -Mode temp
```

- Explicit path:

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1" -Path "C:\Temp\screen.png"
```

- Pixel region (x,y,w,h):

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1" -Mode temp -Region 100,200,800,600
```

- Active window (ask the user to focus it first):

```powershell
powershell -ExecutionPolicy Bypass -File "C:/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.ps1" -Mode temp -ActiveWindow
```

## macOS and Linux (Python helper)

```bash
python3 "/c/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.py"
```

Common patterns:

- Default location:
```bash
python3 "/c/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.py"
```

- Temp location:
```bash
python3 "/c/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.py" --mode temp
```

- App/window capture by name (macOS only):
```bash
python3 "/c/Users/aleco/.codex/skills/screenshot/scripts/take_screenshot.py" --app "AppName"
```

## Error handling

- Always report the saved file path in the response.
- If saving to the OS default location fails with permission errors, try the temp directory.
- On Windows, if PowerShell helper fails, fall back to direct Windows API via Python.
