# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Code plugin marketplace repository. It contains multiple plugins that users install via `/plugin marketplace add drdraxi/draxi-claude-plugins`. All plugins target **Windows only**.

## Repository Structure

```
.claude-plugin/marketplace.json   # Plugin registry — MUST list every plugin
plugins/
  windows-capture/                # Python-based screenshot capture (uses uv + Win32 APIs)
  ralph-loop/                     # Node.js-based iterative AI loop (Windows fork of Anthropic's plugin)
```

## Critical: Marketplace Registration

Every plugin must have an entry in `.claude-plugin/marketplace.json` under the `plugins` array. If a plugin directory exists under `plugins/` but isn't listed in `marketplace.json`, it won't appear when users browse or install plugins.

## Plugin Anatomy

Each plugin lives in `plugins/<name>/` and contains:
- `.claude-plugin/plugin.json` — Plugin metadata (name, description, author)
- `commands/*.md` — Slash commands (frontmatter defines description, allowed-tools, argument-hint)
- `hooks/hooks.json` + hook scripts — Lifecycle hooks (e.g., Stop hook for ralph-loop)
- `scripts/` — Executable scripts invoked by commands
- `agents/*.md` — Subagent definitions (optional)
- `skills/*/SKILL.md` — Skill definitions (optional)

## Plugin-Specific Details

**windows-capture**: Python scripts run via `uv run` with inline PEP 723 dependency metadata (no requirements.txt). Dependencies (`mss`, `Pillow`, `pywin32`) auto-install on first run. Scripts output JSON to stdout.

**ralph-loop**: All scripts are Node.js `.mjs` files (not bash). This is intentional — the original Anthropic plugin uses `.sh` scripts that break on Windows because `${CLAUDE_PLUGIN_ROOT}` expands to backslash paths.

## Windows Path Convention

- **Command markdown code blocks** (` ```! `): These run through bash. Wrap `${CLAUDE_PLUGIN_ROOT}` paths in **single quotes** to prevent bash from interpreting Windows backslashes as escape sequences.
- **Hook commands** (`hooks.json`): These do NOT go through bash the same way — single quotes become literal characters in the path. Use **no quotes** around `${CLAUDE_PLUGIN_ROOT}` in hook commands (e.g., `node ${CLAUDE_PLUGIN_ROOT}/hooks/stop-hook.mjs`).
