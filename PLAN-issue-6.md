# Plan — Issue #6: Combine all scraped questions, answers and solver results into an MD file

## Issue
> "All captured questions and their determined result have to be recorded in a single result file in md format."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#6

---

## Approach

Maintain a single running `session.md` file in `%USERPROFILE%\ScreenScraper\` that accumulates every captured question during a session. Each time a scrape is triggered, the new Q&A block is appended to the file. The file is named after the session start time so separate exam sessions produce separate MD files.

The MD file mirrors what is already printed to the console — question, options, extracted answer, and (if available) the solver's answer, confidence, why, why-not, and source.

---

## Files to Change

| File | Change |
|---|---|
| `scraper/output.py` | Add `format_qa_md()` and `append_to_session_md()` functions |
| `scraper/hotkey.py` | Create session MD path on listener start; pass it through to `on_trigger()` |
| `main.py` | Create session MD path for `--mode once`; pass to `save_result()` |

No new dependencies required.

---

## MD File Format

```markdown
# Exam Session — 2026-03-26 14:05

---

## Q1 — 14:05:32

**Question:** Which event aligns all teams on an ART to a shared mission?

| Option | Text |
|---|---|
| A | PI Planning |
| B | Daily Stand-up |
| C | Iteration Review |
| D | Portfolio Sync |

**Extracted answer:** A

**Solver answer:** A. PI Planning — 94% confident
**Why:** PI Planning is the cadence-based event that aligns all ART teams to a shared mission and Vision.
**Why not B:** Daily Stand-up is a team-level ceremony focused on the next 24 hours, not ART alignment.
**Why not C:** Iteration Review demonstrates completed work but does not align the full ART.
**Why not D:** Portfolio Sync operates at the portfolio level, not the ART level.
**Source:** SAFe_Explained_Ebook_2025.pdf p.14

---

## Q2 — 14:08:11
...
```

---

## Phase 1 — Add `format_qa_md()` to `scraper/output.py`

New function that renders a single Q&A result as a Markdown section:

```python
def format_qa_md(data: dict, index: int, timestamp: str) -> str:
    """Render one scrape result as a Markdown section for the session file."""
```

Outputs:
- `## Q{index} — {time}` heading
- Question text
- Options as a table (if multiple choice)
- Extracted answer
- Solver block (answer, confidence bar, why, why-not per option, source) if present

---

## Phase 2 — Add `append_to_session_md()` to `scraper/output.py`

```python
def append_to_session_md(data: dict, session_path: Path, index: int) -> None:
    """Append one Q&A block to the running session MD file."""
```

- Creates the file with a `# Exam Session — {datetime}` header if it does not exist yet
- Appends the formatted block and a `---` divider
- Increments a per-session question counter

---

## Phase 3 — Thread session state through `hotkey.py`

`start_listener()` creates the session MD path and a question counter on startup. Both are passed into `on_trigger()` so every hotkey trigger appends to the same file:

```python
def start_listener(...):
    session_path = USER_DATA_DIR / f"session_{datetime}.md"
    counter = itertools.count(start=1)
    ...
    def _trigger():
        on_trigger(..., session_path=session_path, q_index=next(counter))
```

---

## Phase 4 — Wire up `main.py`

For `--mode once`: create a session path, pass it to `save_result()`.
For `--mode hotkey`: session path is managed in `hotkey.py` (Phase 3).

`save_result()` gains an optional `session_path` parameter:

```python
def save_result(data, image_path, session_path=None, q_index=1):
```

---

## Phase 5 — Print session file path on startup and after each scrape

After each append, print:
```
[Session MD] M:\Users\...\ScreenScraper\session_2026-03-26_14-05.md  (3 questions)
```

---

## Phase 6 — Commit and close issue

```
Record all exam Q&A into a running session MD file — fixes #6
```

### Verification checklist
- [ ] Each hotkey trigger appends a new Q{n} section to the session MD
- [ ] File is created automatically with a session header on first trigger
- [ ] Solver block appears in MD when solver is active
- [ ] `--mode once` also writes to a session MD
- [ ] Separate runs produce separate session files

---

## Summary of all changes

```
scraper/output.py   ADD  format_qa_md(), append_to_session_md()
                    MOD  save_result() accepts optional session_path + q_index
scraper/hotkey.py   MOD  create session_path + counter; pass to on_trigger()
main.py             MOD  create session_path for --mode once; pass to save_result()
```
