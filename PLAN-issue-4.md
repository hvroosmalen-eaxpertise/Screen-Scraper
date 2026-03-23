# Plan — Issue #4: Create an application installer

## Issue
> "Make an installer for the screen scraper."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#4

---

## Approach

Use **PyInstaller** to bundle Python + all dependencies into a standalone `screen-scraper.exe`. The user runs the exe directly — no Python installation needed.

Installer package (in `dist/screen-scraper/`):
- `screen-scraper.exe` — the bundled app
- `.env.example` — API key template
- `README.txt` — quick-start instructions

On first run, if no `.env` is present, the app prompts the user for their API key and saves it automatically.

---

## Key Challenge: Path Handling When Frozen

`Path(__file__).parent.parent` used in `capture.py` and `output.py` points to PyInstaller's temp extraction dir (`_MEIPASS`), not the folder containing the `.exe`. All paths must resolve relative to the exe location instead.

Fix: add a `scraper/paths.py` module with a `BASE_DIR` that works both frozen and unfrozen:

```python
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent   # next to the .exe
else:
    BASE_DIR = Path(__file__).parent.parent  # project root (dev mode)
```

---

## Files to Create

| File | Purpose |
|---|---|
| `scraper/paths.py` | BASE_DIR helper — frozen-aware path resolution |
| `screen-scraper.spec` | PyInstaller spec: onedir, UAC admin elevation |
| `build.bat` | One-command build: runs PyInstaller, copies .env.example |

## Files to Modify

| File | Change |
|---|---|
| `scraper/capture.py` | Use `paths.BASE_DIR` for `SCREENSHOTS_DIR` |
| `scraper/output.py` | Use `paths.BASE_DIR` for `RESULTS_DIR` |
| `main.py` | Use `paths.BASE_DIR` for `load_dotenv()`; add first-run API key prompt |
| `.gitignore` | Add `dist/`, `build/`, `*.spec` build artifacts |

---

## Phase 0 — Documentation Discovery

### PyInstaller confirmed API

```
pip install pyinstaller

# Build from spec file
pyinstaller screen-scraper.spec

# Key EXE() options in spec:
uac_admin=True       # request admin elevation on launch (needed for keyboard)
console=True         # keep console window (we print output to it)
```

### Spec file skeleton

```python
# screen-scraper.spec
a = Analysis(['main.py'], ...)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [],
    exclude_binaries=True,
    name='screen-scraper',
    console=True,
    uac_admin=True,          # Windows UAC: run as Administrator
)
coll = COLLECT(exe, a.binaries, a.datas,
    name='screen-scraper',
)
```

### Anti-patterns to avoid
- ❌ `--onefile` mode — slow on launch (extracts to temp on every run); use `--onedir` (COLLECT)
- ❌ `Path(__file__)` in frozen code — points to temp dir; always use `paths.BASE_DIR`
- ❌ Hardcode `uac_admin=False` — keyboard library needs admin for global hotkeys on Windows
- ❌ Check `sys._MEIPASS` directly — use `getattr(sys, 'frozen', False)` which is safer

---

## Phase 1 — Add `scraper/paths.py`

```python
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
```

### Verification
- [ ] `from scraper.paths import BASE_DIR; print(BASE_DIR)` prints project root in dev

---

## Phase 2 — Update path references in `capture.py` and `output.py`

### `capture.py`
```python
# Before:
SCREENSHOTS_DIR = Path(__file__).parent.parent / "screenshots"

# After:
from scraper.paths import BASE_DIR
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
```

### `output.py`
```python
# Before:
RESULTS_DIR = Path(__file__).parent.parent / "results"

# After:
from scraper.paths import BASE_DIR
RESULTS_DIR = BASE_DIR / "results"
```

### Verification
- [ ] `python main.py --mode once` still works from source (paths unchanged in dev mode)

---

## Phase 3 — Update `main.py`

### Task 1 — Load .env from BASE_DIR

```python
from scraper.paths import BASE_DIR
load_dotenv(BASE_DIR / ".env", override=True)
```

### Task 2 — First-run prompt if no .env exists

Add before `check_api_key()`:

```python
def prompt_for_api_key() -> None:
    """If no .env exists, ask the user for their API key and save it."""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        print("Welcome to Screen-Scraper!")
        print("No .env file found. Please enter your Anthropic API key.")
        print("(Get one at https://console.anthropic.com/settings/api-keys)\n")
        key = input("ANTHROPIC_API_KEY: ").strip()
        if key:
            env_path.write_text(f"ANTHROPIC_API_KEY={key}\n", encoding="utf-8")
            print(f"Saved to {env_path}\n")
            load_dotenv(env_path, override=True)
```

Call it at the top of `main()` before `check_api_key()`.

### Verification
- [ ] Running without .env prompts for key and saves it
- [ ] Running with existing .env skips the prompt

---

## Phase 4 — PyInstaller Spec (`screen-scraper.spec`)

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('.env.example', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='screen-scraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    uac_admin=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='screen-scraper',
)
```

---

## Phase 5 — Build Script (`build.bat`)

```bat
@echo off
echo Building screen-scraper.exe ...
pip install pyinstaller --quiet
pyinstaller screen-scraper.spec --noconfirm
echo.
echo Done. Installer output: dist\screen-scraper\
echo Share the dist\screen-scraper\ folder with end users.
pause
```

---

## Phase 6 — Update `.gitignore`

Add:
```
dist/
build/
```

(Leave `*.spec` tracked — it's part of the source.)

---

## Phase 7 — Commit and close issue

```
Add PyInstaller installer with first-run API key setup — fixes #4
```

### Verification checklist
- [ ] `build.bat` runs without errors and produces `dist/screen-scraper/screen-scraper.exe`
- [ ] Running the `.exe` without a `.env` prompts for API key and saves it
- [ ] Running the `.exe` with a `.env` skips to hotkey listener
- [ ] `python main.py --mode once` still works from source unchanged

---

## Summary of all changes

```
scraper/paths.py        NEW  — frozen-aware BASE_DIR helper
screen-scraper.spec     NEW  — PyInstaller build spec (onedir, UAC admin)
build.bat               NEW  — one-command build script
scraper/capture.py      MOD  — use BASE_DIR for screenshots/
scraper/output.py       MOD  — use BASE_DIR for results/
main.py                 MOD  — load .env from BASE_DIR; first-run key prompt
.gitignore              MOD  — ignore dist/ and build/
```
