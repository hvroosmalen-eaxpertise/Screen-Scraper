# Plan — Issue #1: Activate screenshot with Ctrl+`

## Issue
> "I like to activate the screen scrape for a single screen capture by pressing Ctrl+` any time."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#1

---

## Phase 0 — Documentation Discovery

### Verified API findings (keyboard library, Windows)

| Key | String to use | Scan code | Notes |
|---|---|---|---|
| Backtick / grave accent (`) | `"grave"` | 41 | ✅ confirmed |
| Ctrl + backtick | `"ctrl+grave"` | 29+41 | ✅ confirmed |
| `"backtick"` | ❌ not valid | — | throws `ValueError` |
| `"ctrl+\`"` | works but fragile | 29+41 | escaping issues in shells |

**Conclusion:** use the string `"ctrl+grave"` everywhere.

### Files to change

| File | Line(s) | Change |
|---|---|---|
| `main.py` | line 40 | default `"ctrl+shift+s"` → `"ctrl+grave"` |
| `scraper/hotkey.py` | line 36 | default `"ctrl+shift+s"` → `"ctrl+grave"` |
| `README.md` | hotkey references | update displayed key combo |

### Anti-patterns to avoid
- ❌ `"backtick"` — not a valid key name in the keyboard library (throws ValueError)
- ❌ `"ctrl+\`"` — escaping is fragile across shells and Python strings; use `"ctrl+grave"` instead
- ❌ Changing `keyboard.wait()` or `keyboard.add_hotkey()` signatures — they are correct as-is

---

## Phase 1 — Change default hotkey to `ctrl+grave`

### Tasks

1. **Edit `main.py` line 40** — change the `--hotkey` argument default:
   ```python
   # Before:
   default="ctrl+shift+s",
   # After:
   default="ctrl+grave",
   ```
   Also update the help string to mention the backtick key:
   ```python
   help="Hotkey to trigger scrape in hotkey mode (default: ctrl+grave  i.e. Ctrl+`)",
   ```

2. **Edit `scraper/hotkey.py` line 36** — change the function signature default:
   ```python
   # Before:
   def start_listener(hotkey: str = "ctrl+shift+s", monitor_index: int = 1) -> None:
   # After:
   def start_listener(hotkey: str = "ctrl+grave", monitor_index: int = 1) -> None:
   ```
   Also update the docstring to note that `ctrl+grave` = Ctrl+`.

3. **Edit `README.md`** — update all references from `ctrl+shift+s` to `ctrl+grave` (Ctrl+`):
   - Usage section: "Press `Ctrl+`` (grave/backtick key)"
   - Options table
   - Example run command at the bottom

### Verification checklist
- [ ] `grep -r "ctrl+shift+s" m:/Screen-Scraper/` returns no matches (in .py and .md files)
- [ ] `grep -r "ctrl+grave" m:/Screen-Scraper/` shows hits in main.py, hotkey.py, README.md
- [ ] `python main.py --help` shows `ctrl+grave` as the default
- [ ] `python -c "import keyboard; keyboard.add_hotkey('ctrl+grave', lambda: None); print('OK')"` prints OK

### Anti-pattern guards
- No use of `"backtick"` anywhere
- No use of `"ctrl+\`"` (backtick literal in string) — always `"ctrl+grave"`

---

## Phase 2 — Commit and close issue

### Tasks

1. Git commit with message referencing issue #1:
   ```
   Change default hotkey to ctrl+grave (Ctrl+`) — fixes #1
   ```

2. Push to `origin main`

3. Verify on GitHub that issue #1 is auto-closed by the `fixes #1` keyword in the commit.
   (If not auto-closed, close it manually via `gh issue close 1`)

### Verification checklist
- [ ] `git log --oneline -1` shows the commit with `fixes #1`
- [ ] GitHub issue #1 is closed
- [ ] `python main.py --help` on a fresh clone shows `ctrl+grave` as default

---

## Summary of all changes

```
main.py           line 40   default="ctrl+grave"  + updated help text
scraper/hotkey.py line 36   default="ctrl+grave"  + updated docstring
README.md         multiple  ctrl+shift+s → ctrl+grave (Ctrl+`)
```
