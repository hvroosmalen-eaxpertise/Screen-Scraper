"""
output.py — Format Q&A results, save to JSON, copy to clipboard, and append to session MD.
"""

import json
import pyperclip
from datetime import datetime
from pathlib import Path

from scraper.paths import USER_DATA_DIR


RESULTS_DIR = USER_DATA_DIR / "results"

DIVIDER = "-" * 45
HEADER  = "-- Q&A Extracted " + "-" * 27


def _confidence_bar(pct: int) -> str:
    """Return a visual bar and percentage, e.g. '████░░░░░░ 42%'."""
    filled = round(pct / 10)
    bar = "\u2588" * filled + "\u2591" * (10 - filled)
    return f"{bar} {pct}%"


def _answer_str(answer) -> str:
    """Normalise answer to a display string."""
    if isinstance(answer, list):
        return ", ".join(answer)
    return answer or ""


def format_qa(data: dict, result_path: str) -> str:
    """Return a human-readable Q&A summary string for the console."""
    lines = [HEADER]

    qa_list = data.get("questions_and_answers", [])
    if qa_list:
        for i, item in enumerate(qa_list, start=1):
            lines.append(f"\nQ{i}: {item.get('question', '')}")
            options = item.get("options") or []
            for opt in options:
                lines.append(f"    {opt}")
            lines.append(f"A{i}: {_answer_str(item.get('answer'))}")

            # Show solver result if present
            if item.get("solved_answer") is not None:
                conf = item.get("solved_confidence", 0)
                lines.append(f"")
                lines.append(f"  ANSWER:  {_answer_str(item['solved_answer'])}")
                lines.append(f"  SURE:    {_confidence_bar(conf)}")
                if item.get("solved_why"):
                    lines.append(f"  WHY:     {item['solved_why']}")
                for opt_label, reason in (item.get("solved_why_not") or {}).items():
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


def format_qa_md(data: dict, q_index: int, timestamp: str) -> str:
    """Render one scrape result as a Markdown section for the session file."""
    time_str = timestamp.split("_")[1].replace("-", ":") if "_" in timestamp else timestamp
    lines = [f"## Q{q_index} \u2014 {time_str}", ""]

    qa_list = data.get("questions_and_answers", [])
    if not qa_list:
        lines.append("*(No questions found in screenshot)*")
        lines.append("")
        return "\n".join(lines)

    for i, item in enumerate(qa_list, start=1):
        if len(qa_list) > 1:
            lines.append(f"### Part {i}")
            lines.append("")

        lines.append(f"**Question:** {item.get('question', '')}")
        lines.append("")

        options = item.get("options") or []
        if options:
            multi = item.get("multi_select", False)
            control = "Checkbox (multi-select)" if multi else "Radio (single-select)"
            lines.append(f"*{control}*")
            lines.append("")
            lines.append("| Option | Text |")
            lines.append("|---|---|")
            for opt in options:
                # Split "A. text" into label + text
                parts = opt.split(". ", 1)
                label = parts[0] if len(parts) == 2 else ""
                text  = parts[1] if len(parts) == 2 else opt
                lines.append(f"| {label} | {text} |")
            lines.append("")

        lines.append(f"**Extracted answer:** {_answer_str(item.get('answer'))}")

        if item.get("solved_answer") is not None:
            conf = item.get("solved_confidence", 0)
            lines.append("")
            lines.append(f"**Solver answer:** {_answer_str(item['solved_answer'])} \u2014 {conf}% confident")
            if item.get("solved_why"):
                lines.append(f"**Why:** {item['solved_why']}")
            for opt_label, reason in (item.get("solved_why_not") or {}).items():
                lines.append(f"**Why not {opt_label}:** {reason}")
            if item.get("solved_source"):
                lines.append(f"**Source:** {item['solved_source']}")

        lines.append("")

    return "\n".join(lines)


def append_to_session_md(data: dict, session_path: Path, q_index: int) -> None:
    """Append one Q&A block to the running session MD file.

    Creates the file with a session header if it does not exist yet.
    """
    session_path.parent.mkdir(parents=True, exist_ok=True)

    if not session_path.exists():
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        header = f"# Exam Session \u2014 {start_time}\n\n---\n\n"
        session_path.write_text(header, encoding="utf-8")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    block = format_qa_md(data, q_index, timestamp)

    with open(session_path, "a", encoding="utf-8") as f:
        f.write(block)
        f.write("---\n\n")

    print(f"[Session MD] {session_path}  ({q_index} question(s))")


def save_result(
    data: dict,
    image_path: str,
    session_path: Path = None,
    q_index: int = 1,
) -> str:
    """Save Q&A JSON, print summary, copy to clipboard, append to session MD.

    Args:
        data:         Dict returned by extract_qa().
        image_path:   Path to the source screenshot (stored in JSON for reference).
        session_path: Optional Path to the running session MD file.
        q_index:      Question number within the session (for MD heading).

    Returns:
        Absolute path to the saved JSON result file.
    """
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    result_path = RESULTS_DIR / f"{timestamp}.json"

    record = {
        "timestamp": timestamp,
        "screenshot": str(image_path),
        **data,
    }

    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    summary = format_qa(data, str(result_path))
    print(summary)

    try:
        pyperclip.copy(summary)
        print("\n[Copied to clipboard]")
    except Exception as e:
        print(f"\n[Clipboard unavailable: {e}]")

    if session_path is not None:
        append_to_session_md(data, session_path, q_index)

    return str(result_path)
