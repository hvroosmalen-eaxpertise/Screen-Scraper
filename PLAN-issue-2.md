# Plan — Issue #2: Deal with multiple choice questions

## Issue
> "During screen scraping the question that appears on it might contain a selection of multiple answers. It is required to save all possible answers for later processing."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#2

---

## Analysis

The current schema for each item in `questions_and_answers` is:
```json
{"question": "...", "answer": "..."}
```

This only captures one answer string. A multiple-choice question has several labelled options (A, B, C, D or 1, 2, 3, …) and optionally a selected/correct answer. Both need to be saved for later processing.

---

## New JSON Schema

Add an `"options"` field to each Q&A item. It is `null` (or absent) for plain Q&A and a list of strings for multiple choice:

```json
{
  "questions_and_answers": [
    {
      "question": "What is Python?",
      "answer": "A high-level programming language.",
      "options": null
    },
    {
      "question": "Which of the following is a Python data type?",
      "answer": "B",
      "options": [
        "A. JavaScript",
        "B. List",
        "C. Java",
        "D. HTML"
      ]
    }
  ],
  "source_description": "..."
}
```

Rules:
- `answer` = the selected/highlighted/correct answer if visible, otherwise `null`
- `options` = all labelled choices as strings (include the label prefix: "A. …")
- For regular Q&A (no options), `options` is `null`

---

## Files to Change

| File | What changes |
|---|---|
| `scraper/extractor.py` | Update `EXTRACTION_PROMPT` + bump `max_tokens` |
| `scraper/output.py` | Update `format_qa()` to display options under each question |

No changes to `main.py`, `capture.py`, `hotkey.py`, or the CLI interface.

---

## Phase 0 — Documentation Discovery

The anthropic SDK and json handling are unchanged. No new libraries needed.

### Anti-patterns to avoid
- ❌ Do not make `options` a required field — plain Q&A items must still work with `options: null`
- ❌ Do not change `response.content[0].text` — correct as-is
- ❌ Do not increase `max_tokens` beyond what is needed — 2048 is sufficient for a full multiple-choice page

---

## Phase 1 — Update Extraction Prompt (`scraper/extractor.py`)

### Task 1 — New prompt

Replace `EXTRACTION_PROMPT` with:

```python
EXTRACTION_PROMPT = """Look at this screenshot carefully. Extract ALL questions and their answers that appear in the image.

For each question, determine whether it is a plain question or a multiple-choice question:
- Plain question: has a single direct answer.
- Multiple-choice question: has labelled answer options (e.g. A, B, C, D or 1, 2, 3, 4).

Return ONLY valid JSON in this exact format, no markdown, no explanation:
{
  "questions_and_answers": [
    {
      "question": "...",
      "answer": "...",
      "options": null
    },
    {
      "question": "...",
      "answer": "B",
      "options": [
        "A. first option",
        "B. second option",
        "C. third option",
        "D. fourth option"
      ]
    }
  ],
  "source_description": "brief description of what the screenshot shows"
}

Rules:
- "answer": the selected, highlighted, or correct answer if visible; otherwise null.
- "options": list of ALL labelled choices as strings (include the label, e.g. "A. text"); null if not multiple choice.
- If no clear questions/answers are found, return: {"questions_and_answers": [], "source_description": "..."}"""
```

### Task 2 — Increase max_tokens

Change `max_tokens=1024` to `max_tokens=2048` to accommodate longer option lists.

### Verification
- [ ] `EXTRACTION_PROMPT` contains the word `"options"` and the two-branch description
- [ ] `max_tokens` is 2048
- [ ] `json.loads()` still wrapped in `try/except json.JSONDecodeError` — unchanged

---

## Phase 2 — Update Output Formatting (`scraper/output.py`)

### Task — Update `format_qa()`

Currently each item prints:
```
Q1: What is Python?
A1: A high-level programming language.
```

New behaviour:
- If `options` is a non-empty list, print each option on its own line after the question, then print the answer:
```
Q1: Which is a Python data type?
    A. JavaScript
    B. List
    C. Java
    D. HTML
A1: B
```
- If `options` is `null` or absent, print exactly as before (no change to plain Q&A display).

Code change in `format_qa()`:

```python
for i, item in enumerate(qa_list, start=1):
    lines.append(f"\nQ{i}: {item.get('question', '')}")
    options = item.get("options") or []
    for opt in options:
        lines.append(f"    {opt}")
    lines.append(f"A{i}: {item.get('answer', '')}")
```

### Verification
- [ ] Plain Q&A items display unchanged (no indented options line)
- [ ] Multiple-choice items show all options indented under the question
- [ ] Answer line still prints as `A1: B` (or the full text if answer is a sentence)

---

## Phase 3 — Commit and close issue

### Tasks
1. Git commit referencing issue #2:
   ```
   Support multiple-choice questions in extraction and output — fixes #2
   ```
2. Push to `origin main`
3. Verify GitHub issue #2 is auto-closed

### Verification checklist
- [ ] `python main.py --mode once` completes without error
- [ ] Result JSON for a multiple-choice screenshot contains `"options": [...]` array
- [ ] Result JSON for a plain Q&A screenshot contains `"options": null`
- [ ] Console output shows options indented under the question

---

## Summary of all changes

```
scraper/extractor.py   EXTRACTION_PROMPT updated for multiple choice + max_tokens 1024→2048
scraper/output.py      format_qa() prints options list when present
```
