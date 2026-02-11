---
name: Windows Screen Capture
description: >-
  Use this skill when the user asks to capture a screenshot, take a screen grab,
  see what's on screen, list open windows, get monitor information, or debug visual
  issues on Windows. Also activates when the user mentions screen capture, screenshot,
  screen recording, monitor layout, or window enumeration.
version: 1.0.0
---

Capture screenshots and gather screen information on Windows using Python scripts managed by `uv`.

## Available Commands

- **`/capture`** - Take a screenshot. Accepts: `full`, `all`, `monitor N`, `window "TITLE"`, `region X,Y,W,H`
- **`/list-windows`** - List all visible windows with titles, positions, and sizes
- **`/screen-info`** - Show monitor count, resolutions, and layout

## Available Agent

- **screen-capture** - Autonomous agent that captures and analyzes screenshots. Triggers proactively when visual context is needed.

## Quick Reference

### Capture Modes

| Mode | Command | Description |
|------|---------|-------------|
| Primary monitor | `/capture` or `/capture full` | Captures the main monitor |
| All monitors | `/capture all` | Captures all monitors as one image |
| Specific monitor | `/capture monitor 2` | Captures monitor by number |
| Specific window | `/capture window "Chrome"` | Captures window by title match |
| Screen region | `/capture region 100,200,800,600` | Captures rectangular area (x,y,w,h) |

### Running Scripts Directly

All scripts use `uv run` with inline dependencies that auto-install on first run:

```bash
# Screen info
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/screen_info.py

# List windows
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/list_windows.py

# Capture screenshot
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py full
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py window "Visual Studio Code"
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py region 0,0,1920,1080
```

### Python Dependencies

Managed automatically via `uv` inline script metadata:
- `mss` - Fast multi-monitor screen capture
- `Pillow` - Image processing and format conversion
- `pywin32` - Windows API for window enumeration and PrintWindow capture

### Output

Screenshots are saved as PNG files in the system temp directory. The capture script returns JSON:
```json
{
  "status": "success",
  "path": "C:\\Users\\...\\AppData\\Local\\Temp\\capture_20260211_143022_abc123.png",
  "mode": "full"
}
```

After capture, read the image file to see and analyze its contents.

## Typical Workflows

1. **Quick screenshot**: `/capture` → auto-analyzes the primary monitor
2. **Capture specific app**: `/list-windows` → find title → `/capture window "title"`
3. **Debug UI issue**: `/screen-info` → understand layout → `/capture` the relevant area
4. **Multi-monitor**: `/screen-info` → `/capture monitor N` for the right screen
