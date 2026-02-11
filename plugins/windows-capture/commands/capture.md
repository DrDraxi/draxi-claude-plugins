---
name: capture
description: Capture a screenshot of the Windows screen, a specific monitor, window, or region
argument-hint: "[full|all|monitor N|window TITLE|region X,Y,W,H]"
allowed-tools:
  - Bash
  - Read
---

Capture a screenshot using the Windows Capture plugin's Python script.

## Arguments

The user may provide arguments specifying the capture mode:

- **No arguments or `full`**: Capture the primary monitor
- **`all`**: Capture all monitors combined into one image
- **`monitor N`**: Capture monitor number N (use `/screen-info` to see available monitors)
- **`window TITLE`**: Capture a specific window matching the title (case-insensitive partial match)
- **`region X,Y,W,H`**: Capture a specific rectangular region (coordinates in pixels)

## Execution

1. Parse the user's arguments to determine mode and target.

2. Run the capture script using `uv run`:
   ```
   uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py <mode> [target]
   ```

   Examples:
   - `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py full`
   - `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py all`
   - `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py monitor 2`
   - `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py window "Visual Studio Code"`
   - `uv run ${CLAUDE_PLUGIN_ROOT}/scripts/capture.py region 0,0,1920,1080`

3. The script outputs JSON with a `path` field containing the saved screenshot location.

4. **After capturing**, use the Read tool to read the screenshot image file at the returned path. This allows you to see and analyze the screenshot content.

5. Describe what you see in the screenshot to the user.

## Error Handling

- If the script returns a JSON `error` field, report it to the user.
- If a window is not found, suggest using `/list-windows` to see available windows.
- If a monitor number is invalid, suggest using `/screen-info` to see available monitors.

## Tips

- For window capture, a partial title match works (e.g., "chrome" matches "Google Chrome").
- The screenshot is saved as a PNG in the system temp directory.
- If the user just says "take a screenshot" or "capture the screen", default to `full` mode.
