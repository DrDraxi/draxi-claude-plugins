---
description: "Explain Ralph Loop plugin and available commands"
hide-from-slash-command-tool: "true"
---

# Ralph Loop Plugin Help

Please explain the following to the user:

## What is Ralph Loop?

Ralph Loop implements the Ralph Wiggum technique - an iterative development methodology based on continuous AI loops, pioneered by Geoffrey Huntley.

**Core concept:** The same prompt is fed to Claude repeatedly. Claude sees its own previous work in files and git history, iteratively improving until completion.

## Available Commands

### /ralph-loop <PROMPT> [OPTIONS]

**Options:**
- `--max-iterations <n>` - Max iterations before auto-stop
- `--completion-promise <text>` - Promise phrase to signal completion

### /cancel-ralph

Cancel an active Ralph loop.

## Windows Compatibility

This is a Windows-compatible fork. Bash scripts replaced with Node.js (.mjs) to avoid backslash path issues.

## Learn More

- Original technique: https://ghuntley.com/ralph/
