# Draxi's Claude Plugins

A custom Claude Code plugin marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [windows-capture](plugins/windows-capture/) | Capture Windows screenshots - full screen, monitors, windows, or regions |

## Installation

Add this marketplace to Claude Code:
```
/plugin marketplace add drdraxi/draxi-claude-plugins
```

Then install a plugin:
```
/plugin install windows-capture
```

## Requirements

- **Windows** (plugins use Win32 APIs)
- **[uv](https://docs.astral.sh/uv/)** - Python package manager
