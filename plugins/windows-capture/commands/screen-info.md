---
name: screen-info
description: Show monitor count, resolutions, positions, and screen layout information
allowed-tools:
  - Bash
---

Display information about connected monitors using the Windows Capture plugin.

## Execution

Run the screen info script:
```
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/screen_info.py
```

## Output

The script outputs JSON with monitor details. Present the results clearly:

1. **Monitor count**: Total number of monitors
2. **Virtual screen**: Combined dimensions across all monitors
3. **Per-monitor details**: For each monitor show:
   - Monitor number
   - Resolution (width x height)
   - Position (left, top)
   - Whether it's the primary monitor

Format as a clear summary, for example:
```
2 monitors detected:
  Monitor 1 (primary): 1920x1080 at position (0, 0)
  Monitor 2: 2560x1440 at position (1920, 0)
  Virtual screen: 4480x1440
```

## Tips

- Monitor numbers correspond to the `monitor N` argument in `/capture monitor N`.
- Position values indicate monitor arrangement (e.g., monitor 2 at x=1920 means it's to the right of a 1920px-wide primary monitor).
