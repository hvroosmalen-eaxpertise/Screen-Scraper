# Screen-Scraper

Capture a screenshot on Windows and extract questions & answers from it using Claude Vision AI. Includes a SAFe/LPM exam solver that looks up the correct answer from bundled source material, warns if your selected answer is wrong, explains why the correct answer is right, and explains why each other option is wrong.

## How It Works

1. Press `Ctrl+`` (or run `--mode once`)
2. A screenshot is taken and sent to Claude Vision
3. Claude extracts all Q&A pairs from the image, including your currently selected answer (filled radio button / checked checkbox)
4. The SAFe/LPM solver searches the source material and returns the correct answer with a confidence percentage, reasoning, and a why-not for every wrong option
5. If your selected answer differs from the solver's answer, a **CHECK: ✗ WARNING** line is shown
6. Results are printed to the console, saved as JSON, copied to your clipboard, and appended to a session Markdown file

## Prerequisites

- Python 3.10+
- Windows
- An [Anthropic API key](https://console.anthropic.com) with credits

## Setup

```bash
# 1. Install dependencies
pip install mss Pillow anthropic python-dotenv keyboard pyperclip pypdf

# 2. Create your .env file
copy .env.example .env
# Then edit .env and add your real API key:
# ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### Run as executable (recommended)

Build once with:
```bash
python -m PyInstaller screen-scraper.spec --noconfirm
```

Then right-click `dist\screen-scraper\screen-scraper.exe` → **Run as administrator**.
The solver and all source material are bundled — no Python installation needed on the target machine.

### Run from source (run as Administrator)

```bash
python main.py
```

The solver auto-enables if `safe-material/` contains PDFs. On first run it pre-reads all material before the exam starts.

### One-shot (no admin needed)
```bash
python main.py --mode once
```
Takes one screenshot, extracts Q&A, solves answers, saves result, then exits.

### Options
```
--mode {once,hotkey}   once = single run, hotkey = listen (default: hotkey)
--hotkey HOTKEY        key combo to trigger scrape (default: ctrl+grave i.e. Ctrl+`)
--stop-hotkey HOTKEY   key combo to stop the listener (default: ctrl+q)
--monitor N            1 = primary monitor, 0 = all combined (default: 1)
--no-solve             disable the SAFe/LPM solver even if safe-material/ exists
--material PATH        path to a custom folder of source PDFs/MDs
```

> **Note:** The `keyboard` library requires Administrator privileges on Windows
> for global hotkeys. Right-click your terminal and choose "Run as administrator".

## SAFe/LPM Solver

On startup the solver indexes all PDFs and Markdown files in `safe-material/` into memory so there is no delay during the exam. Large MD files are split by section for better keyword retrieval. For each captured question it:

1. Finds the 12 most relevant pages/sections from the source material using keyword matching
2. Sends the question, options, and context to Claude
3. Returns the correct answer with:
   - A **confidence percentage** (0–100%)
   - **Why** the answer is correct (quoted from the material)
   - **Why not** for every other option
   - The **source** document and page number
4. Compares the solver's answer to your selected answer and shows a **CHECK** verdict

### Example solver output

```
Q1: What is the primary goal of Lean Portfolio Management?
    A. Maximise team velocity
    B. Align strategy and execution
    C. Reduce headcount
    D. Eliminate retrospectives
A1: B  (your selection)

  ANSWER:  B. Align strategy and execution
  SURE:    █████████░ 91%
  WHY:     LPM connects portfolio strategy to ART execution through continuous alignment of investment and delivery.
  NOT A    Team velocity is a team-level metric, not a portfolio-level goal.
  NOT C    SAFe focuses on value delivery, not headcount reduction.
  NOT D    Retrospectives are a core Agile practice encouraged at all levels in SAFe.
  SOURCE:  SAFe_Explained_Ebook_2025.pdf p.8
  CHECK:   ✓ Your answer (B) matches the solver — good luck!
```

## Source Material

Place PDFs or Markdown files in `safe-material/`. The solver reads all files at startup. The folder currently contains:

| File | Contents |
|---|---|
| `SAFe_Explained_Ebook_2025.pdf` | SAFe overview and core concepts |
| `Lean Portfolio Management Workbook (6.0.2).pdf` | Full LPM workbook |
| `LPM Adoption Roadmap.pdf` | LPM adoption guidance |
| `LPM Align Practice Guide Action Plan.pdf` | Align practice actions |
| `LPM In Practice - Align-1.pdf` | LPM in practice guide |
| `CALMR.pdf` | DevOps and continuous delivery mindset |
| `Enterprise.pdf` | Enterprise strategy and portfolio connection |
| `OKRs.pdf` | Objectives and Key Results |
| `Participatory Budgeting.pdf` | Participatory budgeting practice |
| `Portfolio Sync.pdf` | Portfolio Sync ceremony |
| `Managing a Balanced Portfolio Competency.pdf` | Portfolio balance and horizons |
| `How does SAFe measure flow.pdf` | Flow metrics reference |
| `Understanding horizon thinking...pdf` | Investment horizon definitions |
| `Scrum Process.pdf` | Scrum process reference |
| `White_Paper_Compliance_04-08-17-1.pdf` | Compliance white paper |
| `SAFe_Roles_and_Responsibilities.md` | All SAFe roles grouped by level |
| `SAFe_Activities_and_Ceremonies.md` | All SAFe activities grouped by level |
| `safe-overview.md` | Structured synthesis of all material (generated by `compile_material.py`) |

### Compiling the overview

Run `compile_material.py` to regenerate `safe-overview.md` after adding new PDFs:

```bash
python compile_material.py
```

This uses Claude to synthesise all PDFs into a structured reference with terminology mapping tables, improving keyword retrieval for exam-specific phrasing.

## Validation Tool

`checker.py` re-solves all questions in `%USERPROFILE%\ScreenScraper\results\` and compares answers to the original solver output. Use it to validate source material quality after adding new PDFs.

```bash
python checker.py
```

Output: `%USERPROFILE%\ScreenScraper\validation_YYYY-MM-DD.md`

The report shows:
- **Confirmed** questions (answer unchanged) with confidence score
- **Flagged** questions (answer changed) with original vs new answer, confidence delta, and full reasoning

## Output

| Location | Contents |
|---|---|
| `%USERPROFILE%\ScreenScraper\screenshots\` | Timestamped PNG files |
| `%USERPROFILE%\ScreenScraper\results\` | Timestamped JSON files with extracted Q&A and solver results |
| `%USERPROFILE%\ScreenScraper\session_YYYY-MM-DD_HH-MM.md` | Running session log in Markdown |
| `%USERPROFILE%\ScreenScraper\validation_YYYY-MM-DD.md` | Checker validation report |
| Clipboard | Formatted summary after each scrape |

## Project Structure

```
Screen-Scraper/
├── main.py                      # CLI entry point
├── checker.py                   # Validation tool — re-solves results and reports differences
├── compile_material.py          # Generates safe-overview.md from all PDFs
├── requirements.md
├── screen-scraper.spec          # PyInstaller build spec
├── build.bat                    # convenience build script
├── .env                         # your API key (git-ignored)
├── .env.example                 # template
├── safe-material/               # source PDFs, MD reference files, and safe-overview.md
├── scraper/
│   ├── capture.py               # screenshot via mss
│   ├── extractor.py             # Claude Vision API — extract Q&A and user-selected answer
│   ├── safe-lpm-solver.py       # SAFe/LPM answer solver
│   ├── safe_lpm_solver.py       # import shim (Python can't import hyphens)
│   ├── output.py                # format, save JSON, copy to clipboard, session MD
│   ├── hotkey.py                # keyboard listener
│   └── paths.py                 # BASE_DIR resolution (source vs frozen)
├── screenshots/                 # auto-saved PNGs (git-ignored)
└── results/                     # JSON results (git-ignored)
```
