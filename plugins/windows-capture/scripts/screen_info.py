# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mss>=9.0.0",
# ]
# ///
"""Get information about connected monitors."""

import json
import mss


def get_screen_info() -> dict:
    with mss.mss() as sct:
        monitors = []
        # sct.monitors[0] is the combined virtual screen
        # sct.monitors[1:] are individual monitors
        for i, mon in enumerate(sct.monitors[1:], start=1):
            monitors.append({
                "monitor": i,
                "left": mon["left"],
                "top": mon["top"],
                "width": mon["width"],
                "height": mon["height"],
                "primary": i == 1,
            })

        combined = sct.monitors[0]
        result = {
            "monitor_count": len(monitors),
            "virtual_screen": {
                "left": combined["left"],
                "top": combined["top"],
                "width": combined["width"],
                "height": combined["height"],
            },
            "monitors": monitors,
        }
    return result


def main():
    info = get_screen_info()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
