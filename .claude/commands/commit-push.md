Follow these steps in order. Do not skip any step.

## Step 1 — Build the installer

Run PyInstaller to rebuild the distributable:

```bash
cd M:/screen-scraper && python -m PyInstaller screen-scraper.spec --noconfirm
```

Report the result. If the build fails, stop and report the error — do not proceed to the next steps.

## Step 2 — Update README.md

Read the current README.md and verify it is accurate given the current state of the code. Check:
- Output locations match `%USERPROFILE%\ScreenScraper\`
- Hotkey defaults (`ctrl+grave` to scrape, `ctrl+q` to stop) are correct
- CLI options (`--mode`, `--hotkey`, `--stop-hotkey`, `--monitor`) are complete and accurate
- Setup instructions are still valid

Make any corrections needed. If README is already accurate, leave it unchanged.

## Step 3 — Commit

Stage all modified tracked files and any new files relevant to the change. Then create a git commit. Use a clear, concise commit message that describes what changed.

## Step 4 — Push

Push to `origin main`.

Report the final git log oneline for the new commit so the user can see it.
