# Screen-Scraper Project Rules

## Rebuild After Every Commit

After every `git push`, rebuild the PyInstaller executable:

```
cd M:/screen-scraper
python -m PyInstaller screen-scraper.spec --noconfirm
```

The `dist/` directory is git-ignored, so the exe must be rebuilt locally after each change. The user expects `dist/screen-scraper/screen-scraper.exe` to always reflect the latest code.

## GitHub Issue Workflow

When working on a GitHub issue:

1. **Planning** — after writing the PLAN-issue-N.md file, post the plan content as a comment on the issue via `gh issue comment`.
2. **Closing** — after pushing the fix, post a brief result summary as a comment on the issue before closing it.

Goal: the issue timeline on GitHub should be self-contained — plan and outcome visible without leaving GitHub.
