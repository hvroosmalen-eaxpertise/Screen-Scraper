# Plan — Issue #11: Validate training material via results re-checking

## Goal

A standalone `checker.py` script that re-solves every unique question in
`C:/Users/<user>/ScreenScraper/results/` and compares the new answer to the
stored `solved_answer`. Discrepancies expose gaps or ambiguities in the source
material. Output is a single markdown report.

## Current state

- 47 JSON result files in `C:/Users/hanva/ScreenScraper/results/`
- Each file has one or more `questions_and_answers` entries with:
  `question`, `options`, `multi_select`, `solved_answer`, `solved_confidence`,
  `solved_why`, `solved_why_not`, `solved_source`
- The solver (`scraper/safe-lpm-solver.py`) and `MaterialIndex` are reusable
  without the PyInstaller bundle — they run fine from source.
- The same exam question may appear in multiple result files (e.g. from repeated
  exam sessions). Duplicates should be solved only once.

## Implementation

### New file: `checker.py` (project root)

**Inputs (CLI arguments with defaults):**
```
python checker.py
  [--results  C:/Users/hanva/ScreenScraper/results]
  [--material M:/screen-scraper/safe-material]
  [--output   C:/Users/hanva/ScreenScraper/validation_YYYY-MM-DD.md]
```

**Steps:**
1. Load `MaterialIndex` from `--material` folder (same as the solver does at runtime).
2. Glob all `*.json` files in `--results`.
3. **Deduplicate:** build a dict keyed by normalised question text (stripped, lowercased).
   - First occurrence wins (keeps its `solved_answer`, `options`, `multi_select`).
   - Track which files each duplicate appeared in (for the report).
   - Skip entries with no `solved_answer`.
4. For each unique question:
   - Call `solve_question(question, options, material, multi_select)` → `new`.
   - Compare `new["answer"]` vs stored `solved_answer` (case-insensitive, set-based for multi-select).
   - Classify as **MATCH** or **FLAGGED**.
5. Write the markdown report (see format below).

### Report format (`validation_YYYY-MM-DD.md`)

```markdown
# Validation Report — YYYY-MM-DD HH:MM

X unique questions checked (Y duplicates skipped across Z files) — W flagged, V confirmed.

---

## Flagged (answer changed)

### Question text
- **Original answer:** A
- **New answer:** C
- **Original why:** ...
- **New why:** ...
- **New source:** ...
- **Seen in:** 2026-03-27_10-14-23.json, 2026-03-27_10-17-09.json

---

## Confirmed (answer unchanged)

### Question text
- **Answer:** A — confidence N%
- **Source:** ...
- **Seen in:** 2026-03-27_10-14-23.json
```

### Deduplication logic

- Normalise: `question.strip().lower()`
- Key the seen-dict on this normalised string
- First file encountered wins for the solve; all file names are collected for the report

### Comparison logic

- Single-select: strip + uppercase string compare
- Multi-select: compare as sets

## Files changed

| File | Change |
|------|--------|
| `checker.py` | New standalone script |

No changes to `main.py`, `extractor.py`, `output.py`, or the solver.

## Out of scope

- Does not modify any existing JSON result files.
- Does not rebuild the PyInstaller executable (checker runs from source only).
- Does not re-extract from screenshots — only re-solves already-extracted questions.
