# Plan — Issue #9: Warn if user entered the wrong answer

## Goal

When a SAFe question screenshot is captured and the user has already selected an answer
(filled radio button), compare it to the solver's recommendation and warn clearly if
they don't match.

## Current state

- `extractor.py` extracts `answer` from the screenshot — this is already the
  user-selected option (filled circle), but the prompt language is ambiguous.
- `output.py` displays `answer` (extracted) and `solved_answer` (solver) separately,
  but never compares them or highlights a mismatch.

## Implementation

### Step 1 — Clarify extraction prompt (`scraper/extractor.py`)

The `EXTRACTION_PROMPT` currently says `answer` is "selected/correct labels", which
is ambiguous.  Update the wording to make it explicit:

- `answer` = **the option the user has currently selected** (filled radio button /
  checked checkbox).  If nothing is selected, set `null` / `[]`.
- Add a rule: look specifically for a **filled/solid circle** (●) or **checked box**
  (☑) to identify the user's current choice.

No schema change — `answer` keeps the same type.

### Step 2 — Add comparison + warning to console output (`scraper/output.py`)

In `format_qa()`, after displaying the solver block, add a verdict line:

```
  CHECK:   ✓ Your answer (B) matches the solver — good luck!
```
or
```
  CHECK:   ✗ WARNING — you selected B but solver says C
```

Only show the CHECK line when both `answer` and `solved_answer` are present.
For multi-select, compare sets (order-independent).

### Step 3 — Add comparison to session markdown (`scraper/output.py`)

In `format_qa_md()`, after the solver block, add a verdict line:

```
**Check:** ✓ Your answer matches — **B**
```
or
```
**Check:** ✗ WRONG — you selected **B**, solver says **C**
```

## Files changed

| File | Change |
|------|--------|
| `scraper/extractor.py` | Clarify `answer` = user-selected in prompt |
| `scraper/output.py` | Add verdict comparison to `format_qa()` and `format_qa_md()` |

## Out of scope

- No new fields added to the JSON schema.
- No changes to solver or hotkey logic.
- Does not try to auto-select the correct answer.
