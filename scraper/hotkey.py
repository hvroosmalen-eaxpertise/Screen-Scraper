"""
hotkey.py — Register a global hotkey and run the full scrape pipeline on trigger.

Windows requirement: the keyboard library needs Administrator privileges for
global hotkeys. A startup check warns the user if not elevated.
"""

import ctypes
import itertools
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional
import keyboard

from scraper.capture import take_screenshot
from scraper.extractor import extract_qa
from scraper.output import save_result
from scraper.paths import USER_DATA_DIR


def is_admin() -> bool:
    """Return True if the process is running as Windows Administrator."""
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def on_trigger(monitor_index: int = 1, material=None, session_path: Path = None, q_index: int = 1) -> None:
    """Full pipeline: screenshot -> extract Q&A -> (optionally solve) -> save & append to session MD."""
    print("\n[Hotkey triggered] Capturing screen ...")
    try:
        path = take_screenshot(monitor_index=monitor_index)
        data = extract_qa(path)
        if material is not None:
            from scraper.safe_lpm_solver import solve_all
            print("[Solver] Looking up answers in source material ...")
            solve_all(data, material)
        save_result(data, path, session_path=session_path, q_index=q_index)
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")


def start_listener(
    hotkey: str = "ctrl+grave",
    stop_hotkey: str = "ctrl+q",
    monitor_index: int = 1,
    material: Optional[object] = None,
) -> None:
    """Register hotkey and block until stop_hotkey is pressed.

    Args:
        hotkey:        Key combination to trigger a scrape. Default is "ctrl+grave" (Ctrl+`).
        stop_hotkey:   Key combination to stop the listener. Default is "ctrl+q".
        monitor_index: Passed through to take_screenshot().
        material:      Optional MaterialIndex for SAFe/LPM answer solving.
    """
    if not is_admin():
        print("WARNING: Not running as Administrator.")
        print("  Global hotkeys may not work on Windows without admin privileges.")
        print("  Re-run this script as Administrator for reliable hotkey capture.\n")

    # Create a session MD file path for this listening session
    session_ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    session_path = USER_DATA_DIR / f"session_{session_ts}.md"
    counter = itertools.count(start=1)

    stop_event = threading.Event()

    def _trigger():
        on_trigger(
            monitor_index=monitor_index,
            material=material,
            session_path=session_path,
            q_index=next(counter),
        )

    keyboard.add_hotkey(hotkey, _trigger)
    keyboard.add_hotkey(stop_hotkey, stop_event.set)
    print(f"Listening for [{hotkey}] ... press [{stop_hotkey}] to stop")
    print(f"Session MD:  {session_path}")

    stop_event.wait()   # blocks until stop_hotkey is pressed
    keyboard.unhook_all()
    print("\nStopped.")
    print(f"Session saved to: {session_path}")
