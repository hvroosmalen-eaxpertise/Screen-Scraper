"""
hotkey.py — Register a global hotkey and run the full scrape pipeline on trigger.

Windows requirement: the keyboard library needs Administrator privileges for
global hotkeys. A startup check warns the user if not elevated.
"""

import ctypes
import sys
import keyboard

from scraper.capture import take_screenshot
from scraper.extractor import extract_qa
from scraper.output import save_result


def is_admin() -> bool:
    """Return True if the process is running as Windows Administrator."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def on_trigger(monitor_index: int = 1) -> None:
    """Full pipeline: screenshot -> extract Q&A -> save & copy to clipboard."""
    print("\n[Hotkey triggered] Capturing screen ...")
    try:
        path = take_screenshot(monitor_index=monitor_index)
        data = extract_qa(path)
        save_result(data, path)
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")


def start_listener(hotkey: str = "ctrl+shift+s", monitor_index: int = 1) -> None:
    """Register hotkey and block until Ctrl+C.

    Args:
        hotkey:        Key combination string (e.g. "ctrl+shift+s").
        monitor_index: Passed through to take_screenshot().
    """
    if not is_admin():
        print("WARNING: Not running as Administrator.")
        print("  Global hotkeys may not work on Windows without admin privileges.")
        print("  Re-run this script as Administrator for reliable hotkey capture.\n")

    def _trigger():
        on_trigger(monitor_index=monitor_index)

    keyboard.add_hotkey(hotkey, _trigger)
    print(f"Listening for [{hotkey}] ... (Ctrl+C to stop)")

    try:
        keyboard.wait()   # blocks until Ctrl+C
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)
