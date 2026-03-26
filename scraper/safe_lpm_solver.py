"""
safe_lpm_solver.py — Import shim for safe-lpm-solver.py.

Python cannot import filenames containing hyphens, so this thin wrapper
loads safe-lpm-solver.py via importlib and re-exports its public API.

Frozen-mode note: in a PyInstaller bundle safe-lpm-solver.py is added as a
data file.  __file__ inside a frozen module does not point to a real path, so
we locate the data file relative to the executable instead.
"""

import importlib.util
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # PyInstaller 6+: data files are always in _MEIPASS (_internal/ for folder builds)
    _base = Path(sys._MEIPASS) / "scraper"
else:
    _base = Path(__file__).parent

_spec = importlib.util.spec_from_file_location(
    "safe_lpm_solver_impl",
    _base / "safe-lpm-solver.py",
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

MaterialIndex = _mod.MaterialIndex
solve_question = _mod.solve_question
solve_all = _mod.solve_all
