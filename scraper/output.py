"""
output.py — Format Q&A results, save to JSON, and copy to clipboard.
"""

import json
import pyperclip
from datetime import datetime

from scraper.paths import USER_DATA_DIR


RESULTS_DIR = USER_DATA_DIR / "results"

DIVIDER = "-" * 45
HEADER  = "-- Q&A Extracted " + "-" * 27


def _confidence_bar(pct: int) -> str:
    """Return a visual bar and percentage, e.g. '████░░░░░░ 42%'."""
    filled = round(pct / 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {pct}%"


def format_qa(data: dict, result_path: str) -> str:
    """Return a human-readable Q&A summary string."""
    lines = [HEADER]

    qa_list = data.get("questions_and_answers", [])
    if qa_list:
        for i, item in enumerate(qa_list, start=1):
            lines.append(f"\nQ{i}: {item.get('question', '')}")
            options = item.get("options") or []
            for opt in options:
                lines.append(f"    {opt}")
            lines.append(f"A{i}: {item.get('answer', '')}")

            # Show solver result if present
            if item.get("solved_answer") is not None:
                conf = item.get("solved_confidence", 0)
                lines.append(f"")
                lines.append(f"  ANSWER:  {item['solved_answer']}")
                lines.append(f"  SURE:    {_confidence_bar(conf)}")
                if item.get("solved_why"):
                    lines.append(f"  WHY:     {item['solved_why']}")
                why_not = item.get("solved_why_not") or {}
                for opt_label, reason in why_not.items():
                    lines.append(f"  NOT {opt_label:<3}  {reason}")
                if item.get("solved_source"):
                    lines.append(f"  SOURCE:  {item['solved_source']}")
    else:
        lines.append("\n(No questions and answers found in screenshot)")

    if data.get("api_error"):
        lines.append(f"\nAPI Error: {data['api_error']}")
    if data.get("parse_error"):
        lines.append("\nNote: Response was not valid JSON — raw text preserved.")

    lines.append(f"\n{DIVIDER}")
    lines.append(f"Source: {data.get('source_description', 'N/A')}")
    lines.append(f"Saved:  {result_path}")

    return "\n".join(lines)


def save_result(data: dict, image_path: str) -> str:
    """Save Q&A JSON, print summary, copy to clipboard.

    Args:
        data:       Dict returned by extract_qa().
        image_path: Path to the source screenshot (stored in JSON for reference).

    Returns:
        Absolute path to the saved JSON result file.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_path = RESULTS_DIR / f"{timestamp}.json"

    # Add metadata to the saved record
    record = {
        "timestamp": timestamp,
        "screenshot": str(image_path),
        **data,
    }

    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Format and print to console
    summary = format_qa(data, str(result_path))
    print(summary)

    # Copy to clipboard
    try:
        pyperclip.copy(summary)
        print("\n[Copied to clipboard]")
    except Exception as e:
        print(f"\n[Clipboard unavailable: {e}]")

    return str(result_path)
