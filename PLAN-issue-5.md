# Plan — Issue #5: Store screenshots and results in user profile folder

## Issue
> "Currently the screenshot and results are stored somewhere on a folder on the workstation, however it is better to place them in the loggedin user folder under ScreenScraper. If this folder does not exist it has to be created."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#5

---

## Approach

Store all user data under `%USERPROFILE%\ScreenScraper\`:
- `C:\Users\<name>\ScreenScraper\screenshots\`
- `C:\Users\<name>\ScreenScraper\results\`

Use `Path.home()` — Python's cross-platform way to get the current user's home folder. On Windows this resolves to `C:\Users\<logged-in-user>`.

Folder creation is already handled by `.mkdir(parents=True, exist_ok=True)` calls in `capture.py` and `output.py` — no change needed there.

---

## Files to Change

| File | Change |
|---|---|
| `scraper/paths.py` | Add `USER_DATA_DIR = Path.home() / "ScreenScraper"` |
| `scraper/capture.py` | Use `USER_DATA_DIR` for `SCREENSHOTS_DIR` |
| `scraper/output.py` | Use `USER_DATA_DIR` for `RESULTS_DIR` |
| `README.md` | Update output locations to show new path |

---

## Phase 0 — Documentation Discovery

`Path.home()` is stdlib — no new dependencies.

### Anti-patterns to avoid
- ❌ `os.environ["USERPROFILE"]` — Windows-only and fails if variable is unset; `Path.home()` is cross-platform and always works
- ❌ Hardcode `C:\Users\...` — must use `Path.home()` to pick up the actual logged-in user
- ✅ Folder creation already handled — `mkdir(parents=True, exist_ok=True)` is already in both capture.py and output.py

---

## Phase 1 — Update `scraper/paths.py`

Add `USER_DATA_DIR`:

```python
# User data folder — screenshots and results go here
USER_DATA_DIR = Path.home() / "ScreenScraper"
```

---

## Phase 2 — Update `scraper/capture.py`

```python
# Before:
from scraper.paths import BASE_DIR
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# After:
from scraper.paths import USER_DATA_DIR
SCREENSHOTS_DIR = USER_DATA_DIR / "screenshots"
```

---

## Phase 3 — Update `scraper/output.py`

```python
# Before:
from scraper.paths import BASE_DIR
RESULTS_DIR = BASE_DIR / "results"

# After:
from scraper.paths import USER_DATA_DIR
RESULTS_DIR = USER_DATA_DIR / "results"
```

---

## Phase 4 — Update `README.md`

Update the Output table:

```
| screenshots/ | → C:\Users\<you>\ScreenScraper\screenshots\ |
| results/     | → C:\Users\<you>\ScreenScraper\results\     |
```

---

## Phase 5 — Commit and close issue

```
Store screenshots and results in %USERPROFILE%\ScreenScraper\ — fixes #5
```

### Verification checklist
- [ ] `python main.py --mode once` saves screenshot to `%USERPROFILE%\ScreenScraper\screenshots\`
- [ ] Result JSON saved to `%USERPROFILE%\ScreenScraper\results\`
- [ ] Folders are created automatically if they don't exist

---

## Summary of all changes

```
scraper/paths.py    ADD  USER_DATA_DIR = Path.home() / "ScreenScraper"
scraper/capture.py  MOD  SCREENSHOTS_DIR uses USER_DATA_DIR
scraper/output.py   MOD  RESULTS_DIR uses USER_DATA_DIR
README.md           MOD  update output location docs
```
