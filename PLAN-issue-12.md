# Plan — Issue #12: Compound safe-material into a structured MD overview

## Goal

Create `compile_material.py` — a script that reads all PDFs in `safe-material/`
and uses Claude to synthesise a single `safe-overview.md` with a structured,
exam-friendly layout. This improves keyword retrieval by using SAFe exam
terminology alongside source material wording.

## Motivation

The keyword-based retriever in the solver cannot bridge terminology gaps, e.g.:
- Exam: "current Solutions" — Source: "existing products and services" (Horizon 1)
- Exam: "increased productivity" — Source: "flow velocity"

A structured MD that captures both phrasings in one place solves this.

## Script: `compile_material.py`

**Inputs:**
```
python compile_material.py
  [--material M:/screen-scraper/safe-material]
  [--output   M:/screen-scraper/safe-material/safe-overview.md]
```

**Steps:**
1. Read all PDFs using `pypdf` (same as `MaterialIndex`).
2. Chunk text into batches to stay within token limits.
3. Send to Claude with a structured synthesis prompt.
4. Write the result to `safe-overview.md`.

## Output structure (`safe-overview.md`)

```markdown
# SAFe LPM Overview

## Key Concepts and Definitions
| Term / Abbreviation | Definition | Also known as / Exam phrasing |
|---|---|---|

## Ceremonies
| Ceremony | Cadence | Inputs | Key Activities | Outputs |
|---|---|---|---|---|

## Roles and Responsibilities
| Role | Responsibilities | Works with |
|---|---|---|

## Teams
| Team | Purpose | Ceremonies | Key Inputs | Key Outputs |
|---|---|---|---|---|

## Metrics and Measures
| Metric | What it measures | Also called |
|---|---|---|

## Horizons
| Horizon | Focus | Investment type | Also known as |
|---|---|---|---|
```

## Experiment validation

After generating `safe-overview.md`:
1. Re-run `python checker.py`
2. Compare confidence scores for previously low-confidence questions
3. Specifically check: flow velocity (35%) and Horizon 1 (45%)

## Files changed

| File | Change |
|------|--------|
| `compile_material.py` | New script |
| `safe-material/safe-overview.md` | Generated output (gitignored like PDFs) |
