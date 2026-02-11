# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mss>=9.0.0",
#     "Pillow>=10.0.0",
#     "pywin32>=306",
# ]
# ///
"""
Capture screenshots on Windows.

Modes:
  full       - Capture primary monitor (default)
  all        - Capture all monitors combined
  monitor N  - Capture monitor number N
  window T   - Capture window matching title T
  region X,Y,W,H - Capture specific region
"""

import argparse
import json
import os
import sys
import tempfile
import time

import mss
import mss.tools
from PIL import Image
import win32gui
import win32con
import win32ui
import ctypes


def capture_monitor(monitor_index: int | None = None, all_monitors: bool = False) -> str:
    """Capture a specific monitor or all monitors."""
    with mss.mss() as sct:
        if all_monitors:
            # monitors[0] is the virtual combined screen
            monitor = sct.monitors[0]
        elif monitor_index is not None:
            if monitor_index < 1 or monitor_index > len(sct.monitors) - 1:
                print(json.dumps({
                    "error": f"Monitor {monitor_index} not found. Available: 1-{len(sct.monitors) - 1}"
                }))
                sys.exit(1)
            monitor = sct.monitors[monitor_index]
        else:
            # Default: primary monitor (index 1)
            monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)
        output_path = _temp_path()
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
        return output_path


def capture_region(x: int, y: int, w: int, h: int) -> str:
    """Capture a specific region of the screen."""
    with mss.mss() as sct:
        region = {"left": x, "top": y, "width": w, "height": h}
        screenshot = sct.grab(region)
        output_path = _temp_path()
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=output_path)
        return output_path


def capture_window(title_query: str) -> str:
    """Capture a specific window by title match."""
    hwnd = _find_window(title_query)
    if hwnd is None:
        print(json.dumps({
            "error": f"No window found matching '{title_query}'",
            "hint": "Use list-windows command to see available windows"
        }))
        sys.exit(1)

    # Bring window to foreground if needed
    try:
        # Check if minimized and restore
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.3)

        # Try to bring to front
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.2)
    except Exception:
        pass  # May fail if window is from another process, continue anyway

    # Get window rect
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        print(json.dumps({"error": f"Window '{title_query}' has invalid dimensions"}))
        sys.exit(1)

    # Use PrintWindow for better capture (works even with overlapping windows)
    output_path = _capture_window_printwindow(hwnd, width, height)
    if output_path:
        return output_path

    # Fallback: use mss to capture the window region
    return capture_region(left, top, width, height)


def _capture_window_printwindow(hwnd: int, width: int, height: int) -> str | None:
    """Capture window using Win32 PrintWindow API."""
    try:
        # Make DPI aware to get correct coordinates
        ctypes.windll.user32.SetProcessDPIAware()

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(bitmap)

        # PW_RENDERFULLCONTENT = 2 for better capture on modern Windows
        result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

        if result == 0:
            # Fallback to flag 0
            result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)

        bmp_info = bitmap.GetInfo()
        bmp_bits = bitmap.GetBitmapBits(True)

        img = Image.frombuffer(
            "RGB",
            (bmp_info["bmWidth"], bmp_info["bmHeight"]),
            bmp_bits,
            "raw",
            "BGRX",
            0,
            1,
        )

        output_path = _temp_path()
        img.save(output_path, "PNG")

        # Cleanup
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return output_path
    except Exception:
        return None


def _find_window(title_query: str) -> int | None:
    """Find a window handle by partial title match (case-insensitive)."""
    query_lower = title_query.lower()
    best_match = None
    best_score = 0

    def enum_callback(hwnd, _):
        nonlocal best_match, best_score
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        title_lower = title.lower()

        # Exact match gets highest priority
        if title_lower == query_lower:
            best_match = hwnd
            best_score = 1000
            return

        # Contains match
        if query_lower in title_lower:
            score = len(query_lower) / len(title_lower) * 100
            if score > best_score:
                best_match = hwnd
                best_score = score

    win32gui.EnumWindows(enum_callback, None)
    return best_match


def _temp_path() -> str:
    """Generate a temp file path for the screenshot."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    fd, path = tempfile.mkstemp(prefix=f"capture_{timestamp}_", suffix=".png")
    os.close(fd)
    return path


def main():
    parser = argparse.ArgumentParser(description="Capture Windows screenshots")
    parser.add_argument("mode", nargs="?", default="full",
                        choices=["full", "all", "monitor", "window", "region"],
                        help="Capture mode")
    parser.add_argument("target", nargs="?", default=None,
                        help="Target: monitor number, window title, or region x,y,w,h")

    args = parser.parse_args()

    if args.mode == "full":
        path = capture_monitor()
    elif args.mode == "all":
        path = capture_monitor(all_monitors=True)
    elif args.mode == "monitor":
        if args.target is None:
            print(json.dumps({"error": "Monitor number required. Example: capture monitor 2"}))
            sys.exit(1)
        path = capture_monitor(monitor_index=int(args.target))
    elif args.mode == "window":
        if args.target is None:
            print(json.dumps({"error": "Window title required. Example: capture window Chrome"}))
            sys.exit(1)
        path = capture_window(args.target)
    elif args.mode == "region":
        if args.target is None:
            print(json.dumps({"error": "Region required as x,y,w,h. Example: capture region 0,0,800,600"}))
            sys.exit(1)
        parts = [int(p.strip()) for p in args.target.split(",")]
        if len(parts) != 4:
            print(json.dumps({"error": "Region must be x,y,w,h (4 values). Example: 0,0,800,600"}))
            sys.exit(1)
        path = capture_region(*parts)
    else:
        print(json.dumps({"error": f"Unknown mode: {args.mode}"}))
        sys.exit(1)

    print(json.dumps({
        "status": "success",
        "path": path,
        "mode": args.mode,
    }))


if __name__ == "__main__":
    main()
