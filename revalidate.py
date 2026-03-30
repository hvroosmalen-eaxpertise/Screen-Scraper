"""
revalidate.py — Post-exam review tool for SAFe solver results.

Step 1 — Generate review markdown:
  python revalidate.py --generate-review
  python revalidate.py --generate-review --results C:/Users/hanva/ScreenScraper/results

Step 2 (planned) — Revalidate mismatches from the review file:
  python revalidate.py --revalidate
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

sys.path.insert(0, str(Path(__file__).parent))
from checker import classify_topic

DEFAULT_RESULTS = Path("C:/Users/hanva/ScreenScraper/results")
DEFAULT_OUTPUT  = Path("C:/Users/hanva/ScreenScraper")


def load_questions_with_user_answer(results_dir: Path) -> list[dict]:
    """
    Load all unique solved questions, including the user's own answer (answer field).
    Deduplicates by normalised question text; first occurrence wins.
    """
    seen: dict[str, dict] = {}

    for json_path in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[Revalidate] WARNING: skipping {json_path.name}: {exc}")
            continue

        for item in data.get("questions_and_answers", []):
            if not item.get("solved_answer"):
                continue

            key = item.get("question", "").strip().lower()
            if key not in seen:
                seen[key] = {
                    "question":          item.get("question", ""),
                    "options":           item.get("options") or [],
                    "multi_select":      item.get("multi_select", False),
                    "answer":            item.get("answer"),
                    "solved_answer":     item.get("solved_answer"),
                    "solved_confidence": item.get("solved_confidence", 0),
                    "solved_why":        item.get("solved_why", ""),
                    "solved_source":     item.get("solved_source", ""),
                }

    return list(seen.values())


def resolve_option(letter, options: list[str]) -> str:
    """
    Resolve a letter (e.g. 'A') or list of letters to the full option text.
    Falls back to the raw letter if no match is found.
    """
    if isinstance(letter, list):
        return " / ".join(resolve_option(l, options) for l in letter)

    if not letter:
        return ""

    letter = str(letter).strip().upper()
    for opt in options:
        if opt.strip().upper().startswith(letter + ".") or opt.strip().upper().startswith(letter + " "):
            return opt.strip()

    return letter  # fallback


def _escape(text: str) -> str:
    """Escape pipe characters so they don't break markdown table cells."""
    return text.replace("|", "\\|")


def generate_review(results_dir: Path, output_dir: Path) -> None:
    print(f"[Revalidate] Reading results from {results_dir} ...")
    questions = load_questions_with_user_answer(results_dir)

    if not questions:
        print("[Revalidate] No solved questions found.")
        return

    # Sort: mismatches first, then by topic, then confidence ascending
    def sort_key(e):
        solver = resolve_option(e["solved_answer"], e["options"])
        user   = resolve_option(e["answer"], e["options"])
        match  = solver.upper() == user.upper() if solver and user else True
        return (0 if not match else 1, classify_topic(e["question"]), e["solved_confidence"])

    questions.sort(key=sort_key)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Exam Review — {now}",
        "",
        f"{len(questions)} unique questions. Mismatches (✗) are listed first.",
        "",
        "Edit the **Your Answer** column to correct any entries before running step 2.",
        "",
        "| # | Topic | Question | Options | Solver Answer | Your Answer | Match? |",
        "|---|---|---|---|---|---|---|",
    ]

    for i, entry in enumerate(questions, start=1):
        opts        = entry["options"]
        solver_full = _escape(resolve_option(entry["solved_answer"], opts))
        user_full   = _escape(resolve_option(entry["answer"], opts))
        opts_str    = _escape(" / ".join(opt.strip() for opt in opts))
        topic       = _escape(classify_topic(entry["question"]))
        question    = _escape(entry["question"])

        if solver_full and user_full:
            match = "✓" if solver_full.upper() == user_full.upper() else "✗"
        else:
            match = "?"

        lines.append(f"| {i} | {topic} | {question} | {opts_str} | {solver_full} | {user_full} | {match} |")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "revalidation_review.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Revalidate] Review written to {out_path}")
    print(f"[Revalidate] {sum(1 for e in questions if sort_key(e)[0] == 0)} mismatches / {len(questions)} total")


def main() -> None:
    parser = argparse.ArgumentParser(description="Post-exam review and revalidation tool.")
    parser.add_argument("--generate-review", action="store_true", help="Generate the intermediate review markdown")
    parser.add_argument("--revalidate",      action="store_true", help="Revalidate mismatches from the review file (step 2)")
    parser.add_argument("--results",  default=str(DEFAULT_RESULTS), help="Folder with JSON result files")
    parser.add_argument("--output",   default=str(DEFAULT_OUTPUT),  help="Output folder")
    args = parser.parse_args()

    results_dir = Path(args.results)
    output_dir  = Path(args.output)

    if not results_dir.exists():
        print(f"[Revalidate] ERROR: results folder not found: {results_dir}")
        sys.exit(1)

    if args.generate_review:
        generate_review(results_dir, output_dir)
    elif args.revalidate:
        print("[Revalidate] Step 2 (revalidate) is not yet implemented.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
