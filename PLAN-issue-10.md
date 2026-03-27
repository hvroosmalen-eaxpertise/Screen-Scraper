# Plan — Issue #10: Improve SAFe exam score

## Current state

Pre-exam result: **91% overall** with 4 weak areas identified:

| Topic | Score |
|-------|-------|
| Strategic Portfolio Review & Portfolio Sync | 50% |
| Participatory Budgeting | 50% |
| Connect Portfolio to Enterprise Strategy | 67% |
| Measure Lean Portfolio Performance | 67% |

## Root cause

The solver is limited by what is in `safe-material/`. The current bundle covers general
LPM and alignment content but has no dedicated material for these four topic areas.
No code change is needed — the solver already reads every PDF in `safe-material/`.

## Required source material

Source each article from **scaledagileframework.com** (print to PDF via browser,
or use Save as PDF). Add all files to `M:/screen-scraper/safe-material/`.

### Must-have (covers the 50% topics)

| Article | URL path | Covers |
|---------|----------|--------|
| Strategic Portfolio Review | `/strategic-portfolio-review` | SPR cadence, purpose, participants, key activities |
| Portfolio Sync | `/portfolio-sync` | Sync cadence, purpose, participants, key activities |
| Participatory Budgeting | `/participatory-budgeting` | Practice steps, guardrails, decision-making process |

### Recommended (covers the 67% topics)

| Article | URL path | Covers |
|---------|----------|--------|
| Enterprise Strategy | `/enterprise` | How portfolio vision links to enterprise goals |
| OKRs | `/okrs` | Objective/key-result connection to portfolio |
| Measuring Portfolio Performance | `/measuring-portfolio-performance` | Flow metrics, OKRs, KPIs |
| Flow Metrics | `/flow-metrics` | Flow velocity, load, efficiency, time, distribution |

### Already in bundle (no action needed)

- SAFe_Explained_Ebook_2025.pdf
- Lean Portfolio Management Workbook (6.0.2).pdf
- LPM Adoption Roadmap.pdf
- LPM In Practice - Align-1.pdf
- LPM Align Practice Guide Action Plan.pdf
- SAFe_Activities_and_Ceremonies.md
- SAFe_Roles_and_Responsibilities.md

## Implementation steps

1. Download / print-to-PDF each article listed above.
2. Place PDFs in `M:/screen-scraper/safe-material/`.
3. Rebuild the executable:
   ```
   cd M:/screen-scraper
   python -m PyInstaller screen-scraper.spec --noconfirm
   ```
4. Re-run the pre-exam and verify scores improve in the weak areas.

## No code changes required

The solver already indexes all PDFs and MD files in `safe-material/` at startup.
Adding files and rebuilding is sufficient.
