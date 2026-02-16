# Draxi's Claude Plugins

A custom Claude Code plugin marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [windows-capture](plugins/windows-capture/) | Capture Windows screenshots - full screen, monitors, windows, or regions |
| [ralph-loop](plugins/ralph-loop/) | Windows-compatible Ralph Loop for iterative AI development (fork of Anthropic's official plugin) |

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
- **[uv](https://docs.astral.sh/uv/)** - Python package manager (for windows-capture)
- **[Node.js](https://nodejs.org/)** (for ralph-loop)
