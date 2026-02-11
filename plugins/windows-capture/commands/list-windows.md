---
name: list-windows
description: List all visible windows with their titles, positions, and sizes
allowed-tools:
  - Bash
---

List all visible windows on the system using the Windows Capture plugin.

## Execution

Run the list windows script:
```
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/list_windows.py
```

## Output

The script outputs a JSON array of window objects. Present the results to the user as a formatted table with these columns:

| Title | Position (x, y) | Size (w x h) | Minimized | PID |
|-------|-----------------|---------------|-----------|-----|

- Sort by title alphabetically (already sorted by the script)
- Omit the `hwnd` field from the displayed output as it's internal
- If a window is minimized, note it in the table
- If there are many windows, focus on the most relevant ones and mention the total count

## Tips

- This command is useful before `/capture window "TITLE"` to find the exact window title.
- Window titles may include document names, URLs, or other context (e.g., "README.md - Visual Studio Code").
