# Plan — Issue #7: Deal with multiple correct answers

## Issue
> "It could be that a question is asked to which multiple answers are correct. In front of the answer a square is shown instead of a circle. When multiple answers are correct provide the correct answers. It could be 1, 2, 3, 4 or all."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#7

---

## Approach

Two places need to change:

1. **Extractor** — Claude Vision must detect the checkbox vs radio button visual cue (square = multi-select, circle = single-select) and set a new `multi_select` flag. The `answer` field becomes a list when multiple answers are selected/checked.

2. **Solver** — The prompt must instruct Claude to return a list of correct answers when `multi_select` is true, with why-not reasoning only for options not in the correct set.

Output and session MD formatting then render a comma-separated list where a single answer was shown before.

---

## Files to Change

| File | Change |
|---|---|
| `scraper/extractor.py` | Update `EXTRACTION_PROMPT` to detect square/circle and emit `multi_select` + list `answer` |
| `scraper/safe-lpm-solver.py` | Update `_SOLVE_PROMPT` and `solve_question()` to handle multi-select questions |
| `scraper/output.py` | Update `format_qa()` and `format_qa_md()` to render list answers correctly |

---

## Phase 1 — Update `EXTRACTION_PROMPT` in `scraper/extractor.py`

Add detection of the selection control type and allow `answer` to be a list:

```python
EXTRACTION_PROMPT = """...
For each question also determine the selection type:
- Single-select: answer options have a CIRCLE (radio button) — only one answer is correct.
- Multi-select:  answer options have a SQUARE (checkbox)    — one or more answers may be correct.

Return ONLY valid JSON in this exact format:
{
  "questions_and_answers": [
    {
      "question": "...",
      "multi_select": false,
      "answer": "B",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."]
    },
    {
      "question": "...",
      "multi_select": true,
      "answer": ["A", "C"],
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."]
    }
  ],
  "source_description": "..."
}

Rules:
- "multi_select": true if checkboxes (squares) are shown, false if radio buttons (circles).
- "answer": for single-select a string or null; for multi-select a list of labels (may be empty if none selected).
- "options": list of ALL labelled choices; null if not multiple choice.
..."""
```

---

## Phase 2 — Update solver prompt and return value in `scraper/safe-lpm-solver.py`

Update `_SOLVE_PROMPT` to instruct Claude to return a list when multi-select:

```python
_SOLVE_PROMPT = """...
If this is a MULTI-SELECT question (checkboxes), "answer" must be a JSON list of all correct option labels, e.g. ["A", "C"].
If this is a SINGLE-SELECT question (radio buttons), "answer" must be a single string, e.g. "B".

"why_not" must contain entries for every option NOT in the correct answer set.
..."""
```

Update `solve_question()` to pass `multi_select` flag into the prompt and ensure the return value is consistent:

```python
def solve_question(question, options, material, multi_select=False):
    ...
    # result["answer"] is str (single) or list (multi)
```

Update `solve_all()` to pass `multi_select` from the item:

```python
sol = solve_question(
    item.get("question", ""),
    item.get("options"),
    material,
    multi_select=item.get("multi_select", False),
)
```

---

## Phase 3 — Update display in `scraper/output.py`

`format_qa()` — render list answers as a comma-separated string:

```python
answer = item.get("answer")
answer_str = ", ".join(answer) if isinstance(answer, list) else (answer or "")
lines.append(f"A{i}: {answer_str}")

solved = item.get("solved_answer")
solved_str = ", ".join(solved) if isinstance(solved, list) else (solved or "")
lines.append(f"  ANSWER:  {solved_str}")
```

Same treatment in `format_qa_md()` (added in issue #6).

---

## Phase 4 — Commit and close issue

```
Support multi-select (checkbox) questions with multiple correct answers — fixes #7
```

### Verification checklist
- [ ] Single-select question: `answer` is a string, `multi_select` is false
- [ ] Multi-select question with checkboxes: `answer` is a list, `multi_select` is true
- [ ] Solver returns a list of correct answers for multi-select questions
- [ ] Console output renders list answers as comma-separated string
- [ ] why-not only covers options not in the correct answer set

---

## Summary of all changes

```
scraper/extractor.py       MOD  EXTRACTION_PROMPT — detect checkbox/radio, list answer
scraper/safe-lpm-solver.py MOD  _SOLVE_PROMPT + solve_question() — multi-select support
scraper/output.py          MOD  format_qa() + format_qa_md() — render list answers
```
