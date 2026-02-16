# Ralph Loop Plugin (Windows-Compatible Fork)

Windows-compatible fork of Anthropic's official Ralph Loop plugin for Claude Code.

## What Changed

The original plugin uses bash scripts (`.sh`) for hooks and setup. On Windows, `${CLAUDE_PLUGIN_ROOT}` expands to a path with backslashes (`C:\Users\...`), which bash interprets as escape sequences, breaking the path.

**Fix:** All scripts rewritten as Node.js (`.mjs`). Node handles Windows paths natively. Hook commands use single-quoted paths to prevent bash backslash interpretation.

### Files Changed
- `hooks/stop-hook.sh` -> `hooks/stop-hook.mjs`
- `scripts/setup-ralph-loop.sh` -> `scripts/setup-ralph-loop.mjs`
- `hooks/hooks.json` - uses `node` with single-quoted path
- `commands/ralph-loop.md` - uses `node` with single-quoted path

## Quick Start

```
/ralph-loop "Build a REST API" --completion-promise "COMPLETE" --max-iterations 20
```

## Original

Based on [Anthropic's official Ralph Loop plugin](https://github.com/anthropics/claude-code-plugins).
Technique by [Geoffrey Huntley](https://ghuntley.com/ralph/).
