"""
checker.py — Validate SAFe solver answers by re-solving all questions in the results folder.

Usage:
  python checker.py
  python checker.py --results C:/Users/hanva/ScreenScraper/results
  python checker.py --material M:/screen-scraper/safe-material
  python checker.py --output C:/Users/hanva/ScreenScraper/validation_2026-03-27.md
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)


# ---------------------------------------------------------------------------
# SAFe topic classification
# ---------------------------------------------------------------------------

SAFE_TOPICS: list[tuple[str, list[str]]] = [
    ("Portfolio Kanban",            ["portfolio kanban", "kanban state", "kanban board", "funnel", "reviewing", "analyzing", "backlog", "implementing", "done"]),
    ("Participatory Budgeting",     ["participatory budget", "participatory budgeting", "pb event"]),
    ("WSJF / Epic Sequencing",      ["wsjf", "weighted shortest job", "job duration", "sequenc"]),
    ("Epic Lifecycle",              ["epic lifecycle", "epic owner", "epic hypothesis", "lean business case", "mvp", "minimum viable"]),
    ("Lean Budget Guardrails",      ["lean budget guardrail", "budget guardrail", "guardrail", "capacity allocation", "color of money"]),
    ("OKRs",                        ["okr", "objective and key result", "key result"]),
    ("Value Streams",               ["value stream", "ars", "agile release train"]),
    ("Portfolio Vision & Strategy", ["portfolio vision", "portfolio canvas", "portfolio roadmap", "strategic theme", "portfolio strategy"]),
    ("Strategic Analysis",          ["horizon thinking", "horizon 1", "horizon 2", "horizon 3", "swot", "strategic analysis", "market analysis"]),
    ("Flow Metrics",                ["flow metric", "flow velocity", "flow load", "flow time", "flow efficiency", "flow distribution", "flow debt", "how does safe measure"]),
    ("Agile Portfolio Operations",  ["agile portfolio operation", "portfolio sync", "apo", "coach", "scrum of scrums"]),
    ("Lean Governance",             ["lean governance", "audit", "compliance", "forecast", "dynamic budgeting", "agile capitalization", "capitalization"]),
    ("CALMR / DevOps",              ["calmr", "devops", "continuous delivery", "continuous deployment", "release on demand", "built-in quality"]),
    ("LPM Roles",                   ["epic owner", "lpm team", "portfolio manager", "enterprise architect", "business owner", "product management", "release train engineer", "rte"]),
    ("LPM Implementation",          ["implementation roadmap", "lpm adoption", "kickoff", "community of practice", "cop", "change leadership", "impediment"]),
    ("SAFe Principles",             ["safe principle", "lean principle", "systems thinking", "decentralize", "cadence", "economic framework"]),
    ("Scrum / Team Agility",        ["sprint", "iteration", "retrospective", "backlog refinement", "scrum master", "product owner", "velocity", "story point"]),
    ("Traditional vs Lean PM",      ["traditional", "project-based", "project management", "legacy", "stage gate"]),
    ("AI & Portfolio Management",   ["artificial intelligence", "ai-enabled", "machine learning", "ai "]),
]


def classify_topic(question: str) -> str:
    """Return the first matching SAFe topic name, or 'Other / General'."""
    lower = question.lower()
    for topic, keywords in SAFE_TOPICS:
        if any(kw in lower for kw in keywords):
            return topic
    return "Other / General"


def build_topic_table(flagged: list[dict], confirmed: list[dict]) -> list[str]:
    """Return markdown lines for the Weak Topic Areas table."""
    stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "flagged": 0, "conf_sum": 0})

    for entry in flagged:
        t = classify_topic(entry["question"])
        stats[t]["total"] += 1
        stats[t]["flagged"] += 1
        stats[t]["conf_sum"] += entry.get("solved_confidence", 0)

    for entry in confirmed:
        t = classify_topic(entry["question"])
        stats[t]["total"] += 1
        stats[t]["conf_sum"] += entry.get("solved_confidence", 0)

    rows = []
    for topic, s in stats.items():
        avg_conf = round(s["conf_sum"] / s["total"]) if s["total"] else 0
        rows.append((topic, s["total"], s["flagged"], avg_conf))

    # Sort: most flagged first, then lowest avg confidence first
    rows.sort(key=lambda r: (-r[2], r[3]))

    lines = [
        "## Weak Topic Areas",
        "",
        "| Topic | Questions | Flagged | Avg Confidence |",
        "|---|---|---|---|",
    ]
    for topic, total, n_flagged, avg_conf in rows:
        lines.append(f"| {topic} | {total} | {n_flagged} | {avg_conf}% |")
    lines.append("")
    return lines


# ---------------------------------------------------------------------------

DEFAULT_RESULTS  = Path("C:/Users/hanva/ScreenScraper/results")
DEFAULT_MATERIAL = Path(__file__).parent / "safe-material"
DEFAULT_OUTPUT   = Path("C:/Users/hanva/ScreenScraper")


def _answers_match(a, b) -> bool:
    """Case-insensitive comparison; set-based for multi-select lists."""
    if isinstance(a, list) and isinstance(b, list):
        return {x.strip().upper() for x in a} == {x.strip().upper() for x in b}
    sa = (a or "").strip().upper() if isinstance(a, str) else ""
    sb = (b or "").strip().upper() if isinstance(b, str) else ""
    return bool(sa and sb and sa == sb)


def _answer_str(answer) -> str:
    if isinstance(answer, list):
        return ", ".join(answer)
    return answer or ""


def load_unique_questions(results_dir: Path) -> tuple[list[dict], int, int]:
    """
    Read all JSON result files and deduplicate by normalised question text.

    Returns:
        (unique_questions, total_seen, duplicate_count)

    Each unique_question dict has keys:
        question, options, multi_select, solved_answer, solved_confidence,
        solved_why, solved_why_not, solved_source, seen_in (list of filenames)
    """
    seen: dict[str, dict] = {}   # normalised question → entry
    total_seen = 0
    duplicate_count = 0

    for json_path in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"[Checker] WARNING: skipping {json_path.name}: {exc}")
            continue

        for item in data.get("questions_and_answers", []):
            if not item.get("solved_answer"):
                continue  # not yet solved — skip

            total_seen += 1
            key = item.get("question", "").strip().lower()

            if key in seen:
                seen[key]["seen_in"].append(json_path.name)
                duplicate_count += 1
            else:
                seen[key] = {
                    "question":          item.get("question", ""),
                    "options":           item.get("options"),
                    "multi_select":      item.get("multi_select", False),
                    "solved_answer":     item.get("solved_answer"),
                    "solved_confidence": item.get("solved_confidence", 0),
                    "solved_why":        item.get("solved_why", ""),
                    "solved_why_not":    item.get("solved_why_not", {}),
                    "solved_source":     item.get("solved_source", ""),
                    "seen_in":           [json_path.name],
                }

    return list(seen.values()), total_seen, duplicate_count


def run_checker(results_dir: Path, material_dir: Path, output_path: Path) -> None:
    # Load material index
    sys.path.insert(0, str(Path(__file__).parent))
    from scraper.safe_lpm_solver import MaterialIndex, solve_question

    print(f"[Checker] Loading material from {material_dir} ...")
    material = MaterialIndex(material_dir)
    if not material.ready:
        print("[Checker] ERROR: no material loaded — check --material path.")
        sys.exit(1)

    # Load and deduplicate questions
    print(f"[Checker] Reading results from {results_dir} ...")
    questions, total_seen, duplicate_count = load_unique_questions(results_dir)
    unique_count = len(questions)
    print(f"[Checker] {unique_count} unique questions ({duplicate_count} duplicates skipped from {total_seen} total)")

    if not questions:
        print("[Checker] Nothing to check.")
        return

    # Re-solve each unique question
    flagged = []
    confirmed = []

    for i, entry in enumerate(questions, start=1):
        q = entry["question"]
        print(f"[Checker] [{i}/{unique_count}] {q[:80]}...")
        new = solve_question(q, entry["options"], material, entry["multi_select"])

        if _answers_match(entry["solved_answer"], new["answer"]):
            confirmed.append({**entry, "new": new})
        else:
            flagged.append({**entry, "new": new})

    # Write markdown report
    now = datetime.now()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Validation Report — {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"{unique_count} unique questions checked "
        f"({duplicate_count} duplicates skipped across {total_seen} total) "
        f"— **{len(flagged)} flagged**, {len(confirmed)} confirmed.",
        "",
    ]

    if questions:
        lines += build_topic_table(flagged, confirmed)

    lines += [
        "---",
        "",
    ]

    # Flagged section
    lines.append("## Flagged (answer changed)")
    lines.append("")
    if flagged:
        for entry in flagged:
            lines.append(f"### {entry['question']}")
            lines.append("")
            orig_conf = entry["solved_confidence"]
            new_conf  = entry["new"].get("confidence", 0)
            delta     = new_conf - orig_conf
            delta_str = f"+{delta}%" if delta >= 0 else f"{delta}%"
            trend     = "new material more confident" if delta > 0 else ("same confidence" if delta == 0 else "new material less confident")
            if entry.get("options"):
                lines.append("**Options:**")
                lines.append("")
                for opt in entry["options"]:
                    lines.append(opt)
                    lines.append("")
            lines.append(f"**Original answer:** {_answer_str(entry['solved_answer'])} — {orig_conf}% confident")
            lines.append("")
            lines.append(f"**New answer:** {_answer_str(entry['new']['answer'])} — {new_conf}% confident")
            lines.append("")
            lines.append(f"**Confidence delta:** {delta_str} ({trend})")
            lines.append("")
            lines.append(f"**Original why:** {entry['solved_why']}")
            lines.append("")
            lines.append(f"**New why:** {entry['new'].get('why', '')}")
            lines.append("")
            if entry["new"].get("why_not"):
                for label, reason in entry["new"]["why_not"].items():
                    lines.append(f"**Why not {label}:** {reason}")
                    lines.append("")
            lines.append(f"**New source:** {entry['new'].get('source', '')}")
            lines.append("")
            lines.append(f"**Seen in:** {', '.join(entry['seen_in'])}")
            lines.append("")
    else:
        lines.append("*(none — all answers confirmed)*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Confirmed section
    lines.append("## Confirmed (answer unchanged)")
    lines.append("")
    if confirmed:
        for entry in confirmed:
            lines.append(f"### {entry['question']}")
            lines.append("")
            if entry.get("options"):
                lines.append("**Options:**")
                lines.append("")
                for opt in entry["options"]:
                    lines.append(opt)
                    lines.append("")
            lines.append(f"**Answer:** {_answer_str(entry['solved_answer'])} — {entry['solved_confidence']}% confident")
            lines.append("")
            lines.append(f"**Source:** {entry['solved_source']}")
            lines.append("")
            lines.append(f"**Seen in:** {', '.join(entry['seen_in'])}")
            lines.append("")
    else:
        lines.append("*(none confirmed)*")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[Checker] Report written to {output_path}")
    print(f"[Checker] {len(flagged)} flagged / {len(confirmed)} confirmed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-validate solved SAFe exam results against source material.")
    parser.add_argument("--results",  default=str(DEFAULT_RESULTS),  help="Folder with JSON result files")
    parser.add_argument("--material", default=str(DEFAULT_MATERIAL), help="Folder with SAFe PDF/MD source material")
    parser.add_argument("--output",   default=None,                  help="Output MD file path (default: results folder)")
    args = parser.parse_args()

    results_dir  = Path(args.results)
    material_dir = Path(args.material)

    if args.output:
        output_path = Path(args.output)
    else:
        ts = datetime.now().strftime("%Y-%m-%d")
        output_path = Path(args.results).parent / f"validation_{ts}.md"

    if not results_dir.exists():
        print(f"[Checker] ERROR: results folder not found: {results_dir}")
        sys.exit(1)
    if not material_dir.exists():
        print(f"[Checker] ERROR: material folder not found: {material_dir}")
        sys.exit(1)

    run_checker(results_dir, material_dir, output_path)


if __name__ == "__main__":
    main()
