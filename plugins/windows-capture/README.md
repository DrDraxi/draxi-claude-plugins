# Windows Capture

A Claude Code plugin for capturing Windows screenshots. Supports full screen, specific monitors, individual windows, and custom regions.

## Features

- **Full screen capture** - Primary monitor or all monitors combined
- **Window capture** - Capture specific windows by title (partial match)
- **Region capture** - Capture a specific rectangular area
- **Monitor selection** - Choose which monitor to capture
- **Window listing** - Enumerate all visible windows with positions and sizes
- **Screen info** - Get monitor count, resolutions, and layout
- **Auto-analysis** - Claude reads and describes captured screenshots

## Prerequisites

- **Windows** (uses Win32 APIs)
- **[uv](https://docs.astral.sh/uv/)** - Python package manager (dependencies install automatically)
- **Python 3.10+** (managed by uv)

## Installation

```bash
claude /install-plugin /path/to/windows-capture
```

Or for development:
```bash
claude --plugin-dir /path/to/windows-capture
```

## Commands

| Command | Description |
|---------|-------------|
| `/capture` | Capture primary monitor |
| `/capture all` | Capture all monitors |
| `/capture monitor N` | Capture monitor N |
| `/capture window "Title"` | Capture window by title |
| `/capture region X,Y,W,H` | Capture screen region |
| `/list-windows` | List all visible windows |
| `/screen-info` | Show monitor information |

## Agent

The **screen-capture** agent can proactively capture screenshots when visual context would be helpful, such as debugging UI issues.
