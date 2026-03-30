# Plan — Issue #17: Group flagged/low-confidence questions by SAFe topic area

## Goal
Add a **Weak Topic Areas** table to the `checker.py` validation report that groups all questions (flagged + confirmed) by SAFe topic, showing total questions, flagged count, and average confidence per topic.

## Approach
Keyword-based topic classification against a curated SAFe topic list derived from `safe-overview.md`. Each question is matched to the first topic whose keywords appear in the question text (case-insensitive). Unmatched questions fall into an "Other / General" bucket.

## Changes — `checker.py` only

1. **Add `SAFE_TOPICS` list** — ordered list of `(topic_name, [keywords])` tuples, covering the major SAFe LPM topic areas from the safe-overview table of contents.

2. **Add `classify_topic(question_text)` function** — iterates `SAFE_TOPICS`, returns the first match or `"Other / General"`.

3. **Add `build_topic_table(flagged, confirmed)` function** — aggregates stats per topic:
   - total questions
   - flagged count
   - average confidence (from `solved_confidence`)
   - Sorts by flagged count desc, then avg confidence asc (weakest areas first)
   - Returns markdown table rows

4. **Insert "Weak Topic Areas" section** in `run_checker()` between the summary line and the `---` separator, only when there is at least one question.

## Output format
```
## Weak Topic Areas

| Topic | Questions | Flagged | Avg Confidence |
|---|---|---|---|
| Portfolio Kanban | 3 | 1 | 72% |
| Participatory Budgeting | 4 | 0 | 81% |
```

Topics with 0 flagged and high confidence (≥85%) are still shown so the full picture is visible.

## No schema changes
The existing JSON result format is unchanged. No new CLI flags needed.
