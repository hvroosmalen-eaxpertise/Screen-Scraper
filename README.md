# Screen-Scraper

Capture a screenshot on Windows and extract questions & answers from it using Claude Vision AI. Includes a SAFe/LPM exam solver that looks up the correct answer from bundled source material, explains why it is correct, and explains why each other option is wrong.

## How It Works

1. Press `Ctrl+`` (or run `--mode once`)
2. A screenshot is taken and sent to Claude Vision
3. Claude extracts all Q&A pairs from the image
4. The SAFe/LPM solver searches the source material and returns the correct answer with a confidence percentage, reasoning, and a why-not for every wrong option
5. Results are printed to the console, saved as JSON, and copied to your clipboard

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

On startup the solver indexes all PDFs and Markdown files in `safe-material/` into memory so there is no delay during the exam. For each captured question it:

1. Finds the most relevant pages from the source material using keyword matching
2. Sends the question, options, and context to Claude
3. Returns the correct answer with:
   - A **confidence percentage** (0–100%)
   - **Why** the answer is correct (quoted from the material)
   - **Why not** for every other option
   - The **source** document and page number

### Example solver output

```
Q1: What is the primary goal of Lean Portfolio Management?
    A. Maximise team velocity
    B. Align strategy and execution
    C. Reduce headcount
    D. Eliminate retrospectives
A1: B  (extracted from screen)

  ANSWER:  B. Align strategy and execution
  SURE:    █████████░ 91%
  WHY:     LPM connects portfolio strategy to ART execution through continuous alignment of investment and delivery.
  NOT A    Team velocity is a team-level metric, not a portfolio-level goal.
  NOT C    SAFe focuses on value delivery, not headcount reduction.
  NOT D    Retrospectives are a core Agile practice encouraged at all levels in SAFe.
  SOURCE:  SAFe_Explained_Ebook_2025.pdf p.8
```

## Source Material

Place PDFs or Markdown files in `safe-material/`. The folder currently contains:

| File | Contents |
|---|---|
| `SAFe_Explained_Ebook_2025.pdf` | SAFe overview and core concepts |
| `Lean Portfolio Management Workbook (6.0.2).pdf` | Full LPM workbook |
| `LPM Adoption Roadmap.pdf` | LPM adoption guidance |
| `LPM Align Practice Guide Action Plan.pdf` | Align practice actions |
| `LPM In Practice - Align-1.pdf` | LPM in practice guide |
| `Scrum Process.pdf` | Scrum process reference |
| `White_Paper_Compliance_04-08-17-1.pdf` | Compliance white paper |
| `SAFe_Roles_and_Responsibilities.md` | All SAFe roles grouped by level |
| `SAFe_Activities_and_Ceremonies.md` | All SAFe activities grouped by level |

## Output

| Location | Contents |
|---|---|
| `%USERPROFILE%\ScreenScraper\screenshots\` | Timestamped PNG files |
| `%USERPROFILE%\ScreenScraper\results\` | Timestamped JSON files with extracted Q&A and solver results |
| Clipboard | Formatted summary after each scrape |

## Project Structure

```
Screen-Scraper/
├── main.py                      # CLI entry point
├── requirements.md
├── screen-scraper.spec          # PyInstaller build spec
├── build.bat                    # convenience build script
├── .env                         # your API key (git-ignored)
├── .env.example                 # template
├── safe-material/               # source PDFs and MD reference files
├── scraper/
│   ├── capture.py               # screenshot via mss
│   ├── extractor.py             # Claude Vision API — extract Q&A
│   ├── safe-lpm-solver.py       # SAFe/LPM answer solver
│   ├── safe_lpm_solver.py       # import shim (Python can't import hyphens)
│   ├── output.py                # format, save JSON, copy to clipboard
│   ├── hotkey.py                # keyboard listener
│   └── paths.py                 # BASE_DIR resolution (source vs frozen)
├── screenshots/                 # auto-saved PNGs (git-ignored)
└── results/                     # JSON results (git-ignored)
```
