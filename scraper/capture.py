"""
capture.py — Take a screenshot and save it to screenshots/.

Verified API (mss 9.x):
  sct.monitors[1]  → primary monitor dict
  sct.grab(monitor) → ScreenShot object with .rgb and .size
  mss.tools.to_png(rgb, size, output=path) → saves PNG
"""

import mss
import mss.tools
from datetime import datetime

from scraper.paths import USER_DATA_DIR


SCREENSHOTS_DIR = USER_DATA_DIR / "screenshots"


def take_screenshot(monitor_index: int = 1) -> str:
    """Capture screen and save as PNG.

    Args:
        monitor_index: 1 = primary monitor, 0 = all monitors combined.

    Returns:
        Absolute path to the saved PNG file.
    """
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = SCREENSHOTS_DIR / f"{timestamp}.png"

    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        shot = sct.grab(monitor)
        mss.tools.to_png(shot.rgb, shot.size, output=str(output_path))

    print(f"Screenshot saved: {output_path}")
    return str(output_path)
