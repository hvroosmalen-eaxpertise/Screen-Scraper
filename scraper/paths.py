"""
paths.py — Resolve BASE_DIR correctly whether running as source or frozen exe.
"""
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle — paths relative to the .exe
    BASE_DIR = Path(sys.executable).parent
else:
    # Running from source — paths relative to project root
    BASE_DIR = Path(__file__).parent.parent
