# Dependencies

Install all dependencies with:

```bash
pip install mss Pillow anthropic python-dotenv keyboard pyperclip pypdf
```

## Packages

| Package | Purpose |
|---|---|
| `mss` | Fast multi-monitor screenshots on Windows |
| `Pillow` | Image handling and PNG save |
| `anthropic` | Claude Vision API for Q&A extraction |
| `python-dotenv` | Load `ANTHROPIC_API_KEY` from `.env` file |
| `keyboard` | Global hotkey listener (`Ctrl+`` trigger) |
| `pyperclip` | Copy results to clipboard |
| `pypdf` | Extract text from SAFe/LPM source material PDFs (`--solve` mode) |

## Notes

- Python **3.10+** required
- `keyboard` requires **Administrator privileges** on Windows for global hotkeys
- `anthropic` requires a funded account at [console.anthropic.com](https://console.anthropic.com)
