# Screen-Scraper — Implementation Plan

## Project Goal
A Windows Python application that:
1. Listens for a trigger (hotkey / CLI command)
2. Captures a screenshot
3. Extracts questions & answers using Claude Vision AI
4. Outputs structured JSON / formatted text

---

## Phase 0 — Documentation Discovery (Allowed APIs)

### Verified Libraries & Signatures

| Library | Install | Key API |
|---|---|---|
| `mss` | `pip install mss` | `sct.grab(monitor)` → PIL-compatible |
| `Pillow` | `pip install Pillow` | `Image.open()`, `.convert("L")` |
| `anthropic` | `pip install anthropic` | `client.messages.create(model, messages, max_tokens)` |
| `python-dotenv` | `pip install python-dotenv` | `load_dotenv()` |
| `keyboard` | `pip install keyboard` | `keyboard.add_hotkey(key, fn)`, `keyboard.wait()` |
| `pyperclip` | `pip install pyperclip` | `pyperclip.copy(text)` — copy result to clipboard |

### Vision API (Claude) — Confirmed Pattern
```python
import anthropic, base64

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env

with open("screenshot.png", "rb") as f:
    img_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-3-5-haiku-20241022",   # cheapest vision model
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64",
                                         "media_type": "image/png",
                                         "data": img_b64}},
            {"type": "text", "text": "Extract all questions and answers ..."}
        ]
    }]
)
```

### Screenshot — Confirmed Pattern
```python
import mss, mss.tools
with mss.mss() as sct:
    monitor = sct.monitors[0]          # 0 = all screens combined, 1 = primary
    shot = sct.grab(monitor)
    mss.tools.to_png(shot.rgb, shot.size, output="screenshot.png")
```

### Anti-patterns to avoid
- ❌ `pytesseract` alone — poor accuracy for styled UI text; use Claude Vision
- ❌ `keyboard` requires **admin/elevated** prompt on Windows for global hotkeys
- ❌ Do not store API key in source files — use `.env` only
- ❌ `sct.monitors[0]` = combined all monitors; `sct.monitors[1]` = primary only

---

## Folder Structure
```
m:/Screen-Scraper/
├── .env                  # ANTHROPIC_API_KEY=sk-...  (git-ignored)
├── .gitignore
├── requirements.txt
├── README.md
├── scraper/
│   ├── __init__.py
│   ├── capture.py        # screenshot logic
│   ├── extractor.py      # Claude Vision Q&A extraction
│   ├── output.py         # format & save results
│   └── hotkey.py         # keyboard trigger
├── screenshots/          # auto-saved shots (git-ignored)
├── results/              # JSON output files (git-ignored)
└── main.py               # CLI entry point
```

---

## Phase 1 — Project Scaffold & Config
**Goal:** Runnable skeleton with dependency management and config loading.

### Tasks
1. Create folder structure above
2. Write `requirements.txt`:
   ```
   mss
   Pillow
   anthropic
   python-dotenv
   keyboard
   pyperclip
   ```
3. Write `.gitignore` (ignore `.env`, `screenshots/`, `results/`, `__pycache__/`)
4. Write `scraper/__init__.py` (empty)
5. Write `main.py` with:
   - `argparse` for `--mode` flag: `hotkey` (default) or `once`
   - `load_dotenv()` at top
   - Validates `ANTHROPIC_API_KEY` is present, exits with clear message if not
6. Write `.env.example`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

### Verification
- [ ] `python main.py --help` prints usage without errors
- [ ] Running without `.env` prints: `ERROR: ANTHROPIC_API_KEY not set`
- [ ] `pip install -r requirements.txt` completes cleanly

### Anti-pattern guards
- No hardcoded keys anywhere
- `main.py` must call `load_dotenv()` before any `os.getenv()`

---

## Phase 2 — Screenshot Capture (`scraper/capture.py`)
**Goal:** Capture full screen on demand and save to `screenshots/`.

### Tasks
1. Write `capture.py` with function:
   ```python
   def take_screenshot(monitor_index: int = 1) -> str:
       """Captures screen, saves PNG, returns file path."""
   ```
   - Uses `mss.mss()` context manager
   - `monitor_index=1` → primary monitor (change to 0 for all monitors)
   - Saves to `screenshots/YYYY-MM-DD_HH-MM-SS.png`
   - Returns absolute path string

2. Create `screenshots/` directory if it doesn't exist (use `pathlib.Path.mkdir`)

### Verification
- [ ] `python -c "from scraper.capture import take_screenshot; print(take_screenshot())"` creates a PNG file
- [ ] File is non-empty (> 10 KB)
- [ ] Filename contains timestamp

### Anti-pattern guards
- Use `pathlib.Path` not `os.path` string joins
- Always close `mss` via context manager (`with mss.mss() as sct`)

---

## Phase 3 — Q&A Extraction (`scraper/extractor.py`)
**Goal:** Send screenshot to Claude Vision, receive structured Q&A JSON.

### Tasks
1. Write `extractor.py` with function:
   ```python
   def extract_qa(image_path: str) -> dict:
       """Sends image to Claude, returns {"questions_and_answers": [...]}"""
   ```

2. Encode image to base64 (from file path)

3. Use this **exact prompt** for extraction:
   ```
   Look at this screenshot carefully. Extract ALL questions and their answers
   that appear in the image.

   Return ONLY valid JSON in this exact format, no markdown, no explanation:
   {
     "questions_and_answers": [
       {"question": "...", "answer": "..."},
       ...
     ],
     "source_description": "brief description of what the screenshot shows"
   }

   If no clear questions/answers are found, return:
   {"questions_and_answers": [], "source_description": "..."}
   ```

4. Parse response text as JSON; if parsing fails, return:
   ```python
   {"questions_and_answers": [], "raw_text": response_text, "parse_error": True}
   ```

5. Use model `claude-3-5-haiku-20241022` (cheapest with vision)

### Verification
- [ ] `from scraper.extractor import extract_qa; print(extract_qa("screenshots/test.png"))` returns a dict
- [ ] Dict contains key `"questions_and_answers"`
- [ ] No crash if Claude returns non-JSON (graceful fallback)

### Anti-pattern guards
- ❌ Do not use `response.content` directly — use `response.content[0].text`
- Always wrap `json.loads()` in `try/except json.JSONDecodeError`
- Use `claude-3-5-haiku-20241022` not `claude-3-opus` to keep costs low

---

## Phase 4 — Output & Formatting (`scraper/output.py`)
**Goal:** Save results to JSON file and optionally copy summary to clipboard.

### Tasks
1. Write `output.py` with function:
   ```python
   def save_result(data: dict, image_path: str) -> str:
       """Saves JSON result, prints summary, copies to clipboard. Returns result path."""
   ```
   - Saves to `results/YYYY-MM-DD_HH-MM-SS.json`
   - Prints formatted Q&A to console
   - Copies formatted text to clipboard via `pyperclip.copy()`
   - Returns path to saved JSON file

2. Format Q&A for console/clipboard:
   ```
   ── Q&A Extracted ──────────────────────────
   Q1: What is ...?
   A1: The answer is ...

   Q2: ...
   A2: ...
   ───────────────────────────────────────────
   Source: [description]
   Saved: results/2026-03-23_14-30-00.json
   ```

### Verification
- [ ] Result JSON file created in `results/`
- [ ] Clipboard contains formatted Q&A after run
- [ ] Console output is readable

---

## Phase 5 — Hotkey Listener (`scraper/hotkey.py`) & CLI Wiring
**Goal:** Wire everything together; listen for `Ctrl+Shift+S` to trigger a scrape.

### Tasks
1. Write `hotkey.py`:
   ```python
   def start_listener(hotkey: str = "ctrl+shift+s"):
       """Registers hotkey, blocks until Ctrl+C."""
       import keyboard
       print(f"Listening for {hotkey} ... (Ctrl+C to stop)")
       keyboard.add_hotkey(hotkey, on_trigger)
       keyboard.wait()   # blocks forever
   ```

2. `on_trigger()` callback:
   ```python
   def on_trigger():
       path = take_screenshot()
       data = extract_qa(path)
       save_result(data, path)
   ```

3. Update `main.py`:
   ```python
   if args.mode == "hotkey":
       start_listener()
   elif args.mode == "once":
       path = take_screenshot()
       data = extract_qa(path)
       save_result(data, path)
   ```

4. Add `--hotkey` CLI arg (default `ctrl+shift+s`) passed through to `start_listener()`

5. Add `--monitor` CLI arg (default `1`) for multi-monitor support

### Verification
- [ ] `python main.py --mode once` completes full pipeline, prints Q&A, saves files
- [ ] `python main.py --mode hotkey` starts listener without crashing
- [ ] Pressing `Ctrl+Shift+S` (as admin) triggers scrape

### Anti-pattern guards
- ❌ `keyboard` hotkey listener **requires running terminal as Administrator** on Windows — add a startup check and warn the user if not elevated
- Add `ctypes.windll.shell32.IsUserAnAdmin()` check at startup

---

## Phase 6 — README & Final Polish
**Goal:** Usable, documented project.

### Tasks
1. Write `README.md`:
   - Prerequisites (Python 3.10+, Windows)
   - Install: `pip install -r requirements.txt`
   - Setup: copy `.env.example` → `.env`, add API key
   - Run once: `python main.py --mode once`
   - Run with hotkey: `python main.py --mode hotkey` (**as Administrator**)
   - Output locations: `screenshots/`, `results/`

2. Add admin elevation check with helpful error message

3. Git commit all files

### Verification
- [ ] Complete end-to-end test: hotkey → screenshot → Claude → JSON saved → clipboard updated
- [ ] `results/*.json` is valid JSON with `questions_and_answers` array
- [ ] README is accurate

---

## Dependency Summary
```
pip install mss Pillow anthropic python-dotenv keyboard pyperclip
```

## Environment Variable
```
ANTHROPIC_API_KEY=sk-ant-...   # set in .env file
```

## Run Commands
```bash
# One-shot (no hotkey, no admin needed)
python main.py --mode once

# Hotkey mode (run as Administrator)
python main.py --mode hotkey --hotkey ctrl+shift+s --monitor 1
```
