# Screen-Scraper

Capture a screenshot on Windows and extract questions & answers from it using Claude Vision AI.

## How It Works

1. Press `Ctrl+`` (or run `--mode once`)
2. A screenshot is taken and sent to Claude Vision
3. Claude extracts all Q&A pairs from the image
4. Results are printed to the console, saved as JSON, and copied to your clipboard

## Prerequisites

- Python 3.10+
- Windows
- An [Anthropic API key](https://console.anthropic.com) with credits

## Setup

```bash
# 1. Install dependencies
pip install mss Pillow anthropic python-dotenv keyboard pyperclip

# 2. Create your .env file
copy .env.example .env
# Then edit .env and add your real API key:
# ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### One-shot (no admin needed)
```bash
python main.py --mode once
```
Takes one screenshot, extracts Q&A, saves result, then exits.

### Hotkey mode (run as Administrator)
```bash
python main.py --mode hotkey
```
Listens for `Ctrl+`` (backtick/grave key). Press it any time to trigger a scrape.
Press `Ctrl+Q` to stop.

> **Note:** The `keyboard` library requires Administrator privileges on Windows
> for global hotkeys. Right-click your terminal and choose "Run as administrator".

### Options
```
--mode {once,hotkey}   once = single run, hotkey = listen (default: hotkey)
--hotkey HOTKEY        key combo to trigger scrape (default: ctrl+grave i.e. Ctrl+`)
--stop-hotkey HOTKEY   key combo to stop the listener (default: ctrl+q)
--monitor N            1 = primary monitor, 0 = all combined (default: 1)
```

## Output

| Location | Contents |
|---|---|
| `%USERPROFILE%\ScreenScraper\screenshots\` | Timestamped PNG files |
| `%USERPROFILE%\ScreenScraper\results\` | Timestamped JSON files with extracted Q&A |
| Clipboard | Formatted Q&A summary after each scrape |

### Example JSON output
```json
{
  "timestamp": "2026-03-23_15-30-00",
  "screenshot": "M:\\Screen-Scraper\\screenshots\\2026-03-23_15-30-00.png",
  "questions_and_answers": [
    { "question": "What is Python?", "answer": "A high-level programming language." }
  ],
  "source_description": "A Python tutorial web page"
}
```

## Project Structure

```
Screen-Scraper/
├── main.py               # CLI entry point
├── requirements.md
├── .env                  # your API key (git-ignored)
├── .env.example          # template
├── scraper/
│   ├── capture.py        # screenshot via mss
│   ├── extractor.py      # Claude Vision API call
│   ├── output.py         # JSON save + clipboard
│   └── hotkey.py         # keyboard listener
├── screenshots/          # auto-saved PNGs (git-ignored)
└── results/              # JSON results (git-ignored)
```
