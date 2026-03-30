# Plan — Issue #20: Passed exam revalidation

## Goal
Two-step post-exam review:
1. Generate an intermediate markdown overview of all exam questions for manual review
2. Re-run the solver on questions where your answer differed from the solver's suggestion

---

## Step 1 — Generate review markdown

**Command:** `python revalidate.py --generate-review`

**Output:** `C:/Users/hanva/ScreenScraper/revalidation_review.md`

A markdown table with one row per unique question (deduplicated from all result JSONs):

| # | Topic | Question | Options | Solver Answer | Your Answer | Match? |
|---|---|---|---|---|---|---|
| 1 | Portfolio Kanban | What support does reviewing... | A. Coordination\|B. Guardrails\|C. Vision\|D. Flow | D. Flow | A. Coordination | ✗ |
| 2 | ... | | | | | ✓ |

- **Topic** — SAFe topic via keyword classification (reuses `classify_topic` from `checker.py`)
- **Solver Answer** — full option text resolved from the letter in `solved_answer`
- **Your Answer** — full option text resolved from the letter in `answer`
- **Match?** — ✓ if they agree, ✗ if they differ
- Rows sorted: mismatches first (✗), then by topic, then by confidence ascending

User opens the file, checks the "Your Answer" column, and corrects any cells that are wrong before running step 2.

---

## Step 2 — Revalidate mismatches

**Command:** `python revalidate.py --revalidate`

Reads `revalidation_review.md`, parses the table, identifies all rows where Match? = ✗ or where "Your Answer" has been edited.

For each mismatch, re-runs the solver with a prompt that includes:
- The original question and options
- What you answered vs what the solver originally said
- Instruction to explain the best answer with clearer reasoning grounded in the source material

Writes updated results to `revalidation_report.md` covering only the re-examined questions.

---

## Implementation — `revalidate.py` (new standalone script)

- Reuses `load_unique_questions` logic from `checker.py`
- Reuses `classify_topic` and `SAFE_TOPICS` from `checker.py`
- Reuses `MaterialIndex` and `solve_question` from `scraper/safe_lpm_solver`
- No changes to existing files

### Helper: resolve answer letter → full option text
```python
def resolve_option(letter: str, options: list[str]) -> str:
    """Return the full option string matching the given letter prefix (e.g. 'A' → 'A. Coordination')."""
```

### MD table parsing (for step 2)
Parse the pipe-delimited markdown table to extract Your Answer per question, matched back to the question by row number (#).
