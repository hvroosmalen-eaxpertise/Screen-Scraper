"""
paths.py — Resolve BASE_DIR correctly whether running as source or frozen exe.
           USER_DATA_DIR is where screenshots and results are stored.
"""
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle — paths relative to the .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Running from source — paths relative to project root
    BASE_DIR = Path(__file__).parent.parent

# User data folder — screenshots and results go here regardless of install location
USER_DATA_DIR = Path.home() / "ScreenScraper"
