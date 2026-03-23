"""
output.py — Format Q&A results, save to JSON, and copy to clipboard.
"""

import json
import pyperclip
from datetime import datetime
from pathlib import Path


RESULTS_DIR = Path(__file__).parent.parent / "results"

DIVIDER      = "-" * 45
HEADER       = "-- Q&A Extracted " + "-" * 27


def format_qa(data: dict, result_path: str) -> str:
    """Return a human-readable Q&A summary string."""
    lines = [HEADER]

    qa_list = data.get("questions_and_answers", [])
    if qa_list:
        for i, item in enumerate(qa_list, start=1):
            lines.append(f"\nQ{i}: {item.get('question', '')}")
            lines.append(f"A{i}: {item.get('answer', '')}")
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
