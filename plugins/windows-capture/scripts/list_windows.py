# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pywin32>=306",
# ]
# ///
"""List all visible windows with their titles, positions, and sizes."""

import json
import win32gui
import win32con
import win32process
import os


def get_visible_windows() -> list[dict]:
    windows = []

    def enum_callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        # Skip minimized windows from main list but still include them
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        is_minimized = bool(style & win32con.WS_MINIMIZE)

        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        # Skip tiny/invisible windows
        if width <= 0 or height <= 0:
            return

        # Get process info
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
        except Exception:
            pid = None

        windows.append({
            "hwnd": hwnd,
            "title": title,
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "minimized": is_minimized,
            "pid": pid,
        })

    win32gui.EnumWindows(enum_callback, None)

    # Sort by title for readability
    windows.sort(key=lambda w: w["title"].lower())
    return windows


def main():
    windows = get_visible_windows()
    print(json.dumps(windows, indent=2))


if __name__ == "__main__":
    main()
