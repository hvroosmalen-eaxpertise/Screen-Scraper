# Plan — Issue #8: Improve rendering in session MD file

## Issue
> "The Extracted answer should be in a bigger font, the Why/Why not/Source should each start on a new line."

**GitHub:** hvroosmalen-eaxpertise/Screen-Scraper#8

---

## Approach

One function needs to change: `format_qa_md()` in `scraper/output.py`.

Current output uses `**bold**` inline for everything. The fix:
- Promote **Extracted answer** to a `###` heading so it renders larger
- Add a blank line before Solver answer, each Why not, and Source so they each start on their own paragraph line

No other files need to change.

---

## Files to Change

| File | Change |
|---|---|
| `scraper/output.py` | Update `format_qa_md()` — heading for extracted answer, blank lines between solver fields |

---

## Target Format

```markdown
### Extracted answer: B

Solver answer: The Product Owner (PO) — 85% confident

Why: Product Management is identified as ...

Why not The Scrum Master: The Scrum Master is a servant leader ...

Why not Product Management: While Product Management holds content authority ...

Source: SAFe_Explained_Ebook_2025.pdf p.21
```

---

## Phase 1 — Update `format_qa_md()` in `scraper/output.py`

Change the extracted answer line from:

```python
lines.append(f"**Extracted answer:** {_answer_str(item.get('answer'))}")
```

To a `###` heading:

```python
lines.append(f"### Extracted answer: {_answer_str(item.get('answer'))}")
lines.append("")
```

Change the solver block from inline bold fields to blank-line-separated paragraphs:

```python
lines.append(f"Solver answer: {_answer_str(item['solved_answer'])} \u2014 {conf}% confident")
lines.append("")
if item.get("solved_why"):
    lines.append(f"Why: {item['solved_why']}")
    lines.append("")
for opt_label, reason in (item.get("solved_why_not") or {}).items():
    lines.append(f"Why not {opt_label}: {reason}")
    lines.append("")
if item.get("solved_source"):
    lines.append(f"Source: {item['solved_source']}")
    lines.append("")
```

---

## Phase 2 — Commit and close issue

```
Improve MD rendering: extracted answer as heading, blank lines between solver fields — fixes #8
```

### Verification checklist
- [ ] Extracted answer renders as `###` heading (larger font in MD preview)
- [ ] Solver answer, Why, each Why not, and Source each start on their own line
- [ ] Existing JSON output and console output are unaffected

---

## Summary of all changes

```
scraper/output.py   MOD  format_qa_md() — heading + blank-line-separated solver fields
```
