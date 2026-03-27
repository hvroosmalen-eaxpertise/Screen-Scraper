# Plan — Issue #16: Replace keyword retrieval with semantic/embedding-based search

## Problem

`find_relevant()` scores pages by counting 4+ letter keyword overlap with the query.
This fails when exam phrasing and source material use different words for the same concept:

- Exam: *"investment in current Solutions"* → Source: *"Horizon 1: Optimize and Extend Core"*
- Exam: *"increased productivity metric"* → Source: *"Flow Velocity"*

No keyword overlap = wrong pages retrieved = low confidence despite having the right answer.

## Options considered

| Approach | Quality | Complexity | PyInstaller impact |
|---|---|---|---|
| sentence-transformers (neural) | ★★★★★ | High | +2 GB (torch) |
| scikit-learn TF-IDF | ★★★ | Low | +50 MB |
| LLM query expansion | ★★★★ | Low | None |
| **Hybrid: TF-IDF + keyword** | **★★★★** | **Medium** | **+50 MB** |

**Decision: LLM query expansion** — expand the query with SAFe synonyms before
keyword retrieval. Adds one cheap Claude Haiku call per question but requires no
new dependencies, no model downloads, and no PyInstaller complexity.

If expansion proves insufficient, fall back to TF-IDF as a second phase (tracked
separately).

## How LLM query expansion works

Before calling `find_relevant()`, ask Claude to rewrite the query using SAFe-specific
synonyms and related terms:

```
Input:  "Which horizon is for investment in current Solutions?"
Output: "Horizon 1 current Solutions core business optimize extend existing products
         investment sustaining Run the business cash-cow"
```

The expanded query hits more keyword matches in the source material.

## Implementation

### Step 1 — Add `expand_query()` to `safe-lpm-solver.py`

```python
def expand_query(question: str, options: list, client: anthropic.Anthropic) -> str:
    """Return a keyword-enriched version of the question for better retrieval."""
    prompt = (
        "You are a SAFe terminology expert. Rewrite the following exam question "
        "as a flat list of relevant SAFe keywords and synonyms (no sentences, "
        "no punctuation). Include both the exam phrasing and SAFe source material "
        "wording. Return only the keywords, space-separated.\n\n"
        f"Question: {question}\n"
        f"Options: {' '.join(options or [])}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return question + " " + response.content[0].text.strip()
```

### Step 2 — Use expanded query in `solve_question()`

```python
expanded = expand_query(question, options, client)
relevant  = material.find_relevant(expanded)
```

The `client` is already created in `solve_question()` so no signature change is needed.

### Step 3 — Graceful fallback

If the expansion API call fails (e.g. network error), fall back to the original query.
Wrap in try/except — retrieval degrades silently, solve continues.

## Files changed

| File | Change |
|------|--------|
| `scraper/safe-lpm-solver.py` | Add `expand_query()`, call it in `solve_question()` |

No changes to `requirements.md`, `screen-scraper.spec`, or any other file.

## Validation

After implementing:
1. Re-run `python checker.py`
2. Check confidence for previously weak questions:
   - *"Which metric will show increased productivity"* (was 35%)
   - *"Which horizon is for investment in current Solutions"* (was 45%)
3. Verify overall flagged/confirmed count does not regress

## Trade-offs

- **Cost:** One extra Haiku call per question (~$0.0001). Negligible for exam use.
- **Latency:** ~0.5s extra per question. Acceptable during an exam.
- **Risk:** Expansion could introduce noise. Mitigated by appending (not replacing)
  the original query — original keywords are always present.
