# Plan — Issue #3: Continue running the scraper in the background

## Issue
> "For each ctrl-` make a new screenshot, until Ctrl-Q or ctrl-q is pressed. If this happens the application can be closed."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#3

---

## Analysis

The existing `--mode hotkey` already does continuous scraping — every Ctrl+` triggers a full pipeline run. The only gap is the stop condition: currently it requires Ctrl+C in the terminal. The issue asks for Ctrl+Q to stop instead.

The `keyboard` library's `keyboard.wait()` blocks until Ctrl+C. To stop on a specific hotkey instead, we replace it with a `threading.Event` that gets set by a Ctrl+Q hotkey handler.

---

## Files to Change

| File | What changes |
|---|---|
| `scraper/hotkey.py` | Add `stop_hotkey` param; replace `keyboard.wait()` with `threading.Event` |
| `main.py` | Add `--stop-hotkey` CLI arg (default `ctrl+q`) |
| `README.md` | Update stop instruction from Ctrl+C to Ctrl+Q |

---

## Phase 0 — Documentation Discovery

### Anti-patterns to avoid
- ❌ Do not call `sys.exit()` from inside a hotkey callback — it runs on a background thread and raises `SystemExit` there, not on the main thread
- ❌ Do not use `keyboard.wait()` when you need a hotkey-driven stop — it only responds to Ctrl+C
- ✅ Use `threading.Event` + `stop_event.wait()` — the stop hotkey calls `stop_event.set()`, the main thread unblocks cleanly

---

## Phase 1 — Update `scraper/hotkey.py`

### Task 1 — Add `import threading`

### Task 2 — Add `stop_hotkey` parameter to `start_listener()`

```python
def start_listener(hotkey: str = "ctrl+grave", stop_hotkey: str = "ctrl+q", monitor_index: int = 1) -> None:
```

### Task 3 — Replace `keyboard.wait()` block with `threading.Event`

```python
stop_event = threading.Event()

keyboard.add_hotkey(hotkey, _trigger)
keyboard.add_hotkey(stop_hotkey, stop_event.set)
print(f"Listening for [{hotkey}] ... press [{stop_hotkey}] to stop")

stop_event.wait()   # blocks until stop_hotkey is pressed
keyboard.unhook_all()
print("\nStopped.")
```

Remove the `try/except KeyboardInterrupt` block — Ctrl+C is no longer the stop mechanism.

### Verification
- [ ] Pressing Ctrl+` triggers a scrape
- [ ] Pressing Ctrl+Q prints "Stopped." and exits cleanly
- [ ] No `sys.exit()` called from a hotkey callback

---

## Phase 2 — Update `main.py`

### Task — Add `--stop-hotkey` CLI arg

```python
parser.add_argument(
    "--stop-hotkey",
    default="ctrl+q",
    help="Hotkey to stop the listener in hotkey mode (default: ctrl+q)",
)
```

Pass it through to `start_listener()`:

```python
start_listener(hotkey=args.hotkey, stop_hotkey=args.stop_hotkey, monitor_index=args.monitor)
```

### Verification
- [ ] `python main.py --help` shows `--stop-hotkey` with default `ctrl+q`

---

## Phase 3 — Update `README.md`

### Task — Replace Ctrl+C stop references with Ctrl+Q

- Usage section: "Press `Ctrl+Q` to stop" (was "Press `Ctrl+C` to stop")
- Hotkey mode example: update inline note

---

## Phase 4 — Commit and close issue

```
Stop hotkey listener with Ctrl+Q instead of Ctrl+C — fixes #3
```

### Verification checklist
- [ ] `python main.py --mode hotkey` starts and shows `press [ctrl+q] to stop`
- [ ] Ctrl+` scrapes repeatedly
- [ ] Ctrl+Q exits cleanly with "Stopped."

---

## Summary of all changes

```
scraper/hotkey.py   add stop_hotkey param + threading.Event stop mechanism
main.py             add --stop-hotkey CLI arg (default ctrl+q)
README.md           update stop instruction to Ctrl+Q
```
