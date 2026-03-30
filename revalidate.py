"""
revalidate.py — Post-exam review tool for SAFe solver results.

Step 1 — Generate review markdown:
  python revalidate.py --generate-review
  python revalidate.py --generate-review --results C:/Users/hanva/ScreenScraper/results

Step 2 — Revalidate questions where Selected Answer differs from Solver Answer:
  python revalidate.py --revalidate
  python revalidate.py --revalidate --review C:/Users/hanva/ScreenScraper/revalidation_review.md
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

sys.path.insert(0, str(Path(__file__).parent))
from checker import classify_topic

DEFAULT_RESULTS = Path("C:/Users/hanva/ScreenScraper/results")
DEFAULT_OUTPUT  = Path("C:/Users/hanva/ScreenScraper")
DEFAULT_REVIEW  = DEFAULT_OUTPUT / "revalidation_review.md"
DEFAULT_MATERIAL = Path(__file__).parent / "safe-material"

_REVALIDATE_PROMPT = """\
You are a SAFe/LPM certification exam expert. A student took the exam and there is a \
disagreement between what the AI solver suggested and what the student actually selected.

SOURCE MATERIAL:
{context}

QUESTION: {question}

OPTIONS:
{options}

AI solver originally suggested: {solver_answer}
Student selected: {student_answer}

Using ONLY the source material above, provide a thorough analysis. Determine the best answer \
and explain clearly why it is correct. If the student's answer differs from the solver's, \
explain which is more likely correct and why the other is less suitable.

Return ONLY valid JSON — no markdown fences, no extra text:
{{
  "best_answer": "<single option label, e.g. \\"B\\">",
  "confidence": <integer 0-100>,
  "why_correct": "<clear explanation of why this is the best answer, grounded in the source material>",
  "why_not_solver": "<only if solver answer differs from best_answer: why the solver was wrong>",
  "why_not_student": "<only if student answer differs from best_answer: why the student's choice is less correct>",
  "source": "<filename and page>"
}}"""


def load_questions_with_user_answer(results_dir: Path) -> list[dict]:
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
                    "first_seen":        json_path.name,
                }

    return list(seen.values())


def resolve_option(letter, options: list[str]) -> str:
    if isinstance(letter, list):
        return " / ".join(resolve_option(l, options) for l in letter)
    if not letter:
        return ""
    letter = str(letter).strip().upper()
    for opt in options:
        if opt.strip().upper().startswith(letter + ".") or opt.strip().upper().startswith(letter + " "):
            return opt.strip()
    return letter


def _escape(text: str) -> str:
    return text.replace("|", "\\|")


# ---------------------------------------------------------------------------
# Step 1 — Generate review
# ---------------------------------------------------------------------------

def generate_review(results_dir: Path, output_dir: Path) -> None:
    print(f"[Revalidate] Reading results from {results_dir} ...")
    questions = load_questions_with_user_answer(results_dir)

    if not questions:
        print("[Revalidate] No solved questions found.")
        return

    questions.sort(key=lambda e: e["first_seen"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Exam Review — {now}",
        "",
        f"{len(questions)} unique questions, in exam sequence.",
        "",
        "Fill in the **Selected Answer** column with what you actually selected, then run step 2.",
        "",
        "| # | Topic | Question | Options | Solver Answer | Your Answer | Match? | Selected Answer |",
        "|---|---|---|---|---|---|---|---|",
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

        solver_letter = str(entry["solved_answer"]).strip().upper() if entry["solved_answer"] else ""
        lines.append(f"| {i} | {topic} | {question} | {opts_str} | {solver_full} | {user_full} | {match} | {solver_letter} |")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "revalidation_review.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[Revalidate] Review written to {out_path}")
    mismatches = sum(1 for e in questions if resolve_option(e["solved_answer"], e["options"]).upper() != resolve_option(e["answer"], e["options"]).upper())
    print(f"[Revalidate] {mismatches} mismatches / {len(questions)} total")


# ---------------------------------------------------------------------------
# Step 2 — Revalidate
# ---------------------------------------------------------------------------

def parse_review(review_path: Path) -> list[dict]:
    """Parse the markdown table and return rows where Selected Answer differs from Solver Answer."""
    rows = []
    lines = review_path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        if not line.startswith("| ") or line.startswith("| #") or line.startswith("|---"):
            continue

        # Split on unescaped pipes
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', line) if c.strip()]
        if len(cells) < 8:
            continue

        # Columns: # | Topic | Question | Options | Solver Answer | Your Answer | Match? | Selected Answer
        num_str        = cells[0]
        question       = cells[2].replace("\\|", "|")
        options_str    = cells[3].replace("\\|", "|")
        solver_full    = cells[4].replace("\\|", "|")
        selected_raw   = cells[7].strip() if len(cells) > 7 else ""

        # Parse options list from " / " separated string
        options = [o.strip() for o in options_str.split(" / ") if o.strip()]

        # Extract solver letter from full option text (first char before ".")
        solver_letter = ""
        m = re.match(r'^([A-D])[\. ]', solver_full.strip())
        if m:
            solver_letter = m.group(1).upper()

        # Selected answer: accept a letter or full option text
        selected_letter = ""
        if selected_raw:
            m2 = re.match(r'^([A-D])[\. ]', selected_raw.strip())
            if m2:
                selected_letter = m2.group(1).upper()
            elif len(selected_raw) == 1 and selected_raw.upper() in "ABCD":
                selected_letter = selected_raw.upper()

        rows.append({
            "num":             num_str,
            "question":        question,
            "options":         options,
            "solver_letter":   solver_letter,
            "solver_full":     solver_full,
            "selected_letter": selected_letter,
            "selected_full":   resolve_option(selected_letter, options) if selected_letter else selected_raw,
        })

    return rows


def revalidate_question(question: str, options: list[str], solver_letter: str,
                        student_letter: str, material) -> dict:
    """Re-run analysis for a single question with context of the disagreement."""
    client = anthropic.Anthropic()
    # Build an enriched query (same approach as expand_query in the solver)
    query = question + " " + " ".join(options)
    relevant = material.find_relevant(query)

    context = "\n\n---\n\n".join(
        f"[{p['source']}, p.{p['page']}]\n{p['text'][:1800]}"
        for p in relevant
    )
    options_text = "\n".join(f"  {opt}" for opt in options)
    solver_full  = resolve_option(solver_letter, options)
    student_full = resolve_option(student_letter, options)

    prompt = _REVALIDATE_PROMPT.format(
        context=context,
        question=question,
        options=options_text,
        solver_answer=f"{solver_letter}. {solver_full}" if solver_full != solver_letter else solver_letter,
        student_answer=f"{student_letter}. {student_full}" if student_full != student_letter else student_letter,
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as exc:
        return {"best_answer": "", "confidence": 0, "why_correct": f"API error: {exc}",
                "why_not_solver": "", "why_not_student": "", "source": ""}

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"why_correct": raw[:400]}

    result.setdefault("best_answer", "")
    result.setdefault("confidence", 0)
    result.setdefault("why_correct", "")
    result.setdefault("why_not_solver", "")
    result.setdefault("why_not_student", "")
    result.setdefault("source", "")
    return result


def run_revalidation(review_path: Path, output_dir: Path, material_dir: Path) -> None:
    from scraper.safe_lpm_solver import MaterialIndex

    print(f"[Revalidate] Parsing review from {review_path} ...")
    rows = parse_review(review_path)

    disagreements = [r for r in rows if r["selected_letter"] and r["selected_letter"] != r["solver_letter"]]
    agreements    = [r for r in rows if not r["selected_letter"] or r["selected_letter"] == r["solver_letter"]]

    print(f"[Revalidate] {len(disagreements)} disagreements to revalidate, {len(agreements)} agreements.")

    if not disagreements:
        print("[Revalidate] Nothing to revalidate — Selected Answer matches Solver Answer for all questions.")
        return

    print(f"[Revalidate] Loading material from {material_dir} ...")
    material = MaterialIndex(material_dir)
    if not material.ready:
        print("[Revalidate] ERROR: no material loaded.")
        sys.exit(1)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Revalidation Report — {now}",
        "",
        f"{len(disagreements)} questions revalidated (solver and selected answer differed).",
        "",
        "---",
        "",
        "## Revalidated Questions",
        "",
    ]

    for i, row in enumerate(disagreements, start=1):
        q       = row["question"]
        opts    = row["options"]
        print(f"[Revalidate] [{i}/{len(disagreements)}] {q[:80]}...")

        result = revalidate_question(q, opts, row["solver_letter"], row["selected_letter"], material)

        best_letter = str(result.get("best_answer", "")).strip().upper()
        best_full   = resolve_option(best_letter, opts)
        conf        = result.get("confidence", 0)

        lines.append(f"### Q{row['num']}. {q}")
        lines.append("")
        lines.append("**Options:**")
        lines.append("")
        for opt in opts:
            lines.append(f"- {opt}")
        lines.append("")
        lines.append(f"**Solver suggested:** {row['solver_full']}")
        lines.append("")
        lines.append(f"**You selected:** {row['selected_full']}")
        lines.append("")
        lines.append(f"**Best answer: {best_letter}. {best_full}** — {conf}% confident")
        lines.append("")
        lines.append(f"**Why correct:** {result['why_correct']}")
        lines.append("")
        if result.get("why_not_solver") and best_letter != row["solver_letter"]:
            lines.append(f"**Why solver was wrong:** {result['why_not_solver']}")
            lines.append("")
        if result.get("why_not_student") and best_letter != row["selected_letter"]:
            lines.append(f"**Why your selection was less correct:** {result['why_not_student']}")
            lines.append("")
        lines.append(f"**Source:** {result['source']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Summary of agreed questions
    lines += [
        "## Agreed Questions (no revalidation needed)",
        "",
        "| # | Question | Answer |",
        "|---|---|---|",
    ]
    for row in agreements:
        lines.append(f"| {row['num']} | {_escape(row['question'])} | {row['solver_full']} |")
    lines.append("")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "revalidation_report.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n[Revalidate] Report written to {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Post-exam review and revalidation tool.")
    parser.add_argument("--generate-review", action="store_true", help="Generate the intermediate review markdown (step 1)")
    parser.add_argument("--revalidate",      action="store_true", help="Revalidate disagreements from the review file (step 2)")
    parser.add_argument("--results",  default=str(DEFAULT_RESULTS),  help="Folder with JSON result files")
    parser.add_argument("--output",   default=str(DEFAULT_OUTPUT),   help="Output folder")
    parser.add_argument("--review",   default=str(DEFAULT_REVIEW),   help="Path to revalidation_review.md (step 2)")
    parser.add_argument("--material", default=str(DEFAULT_MATERIAL), help="Folder with SAFe source material")
    args = parser.parse_args()

    output_dir = Path(args.output)

    if args.generate_review:
        results_dir = Path(args.results)
        if not results_dir.exists():
            print(f"[Revalidate] ERROR: results folder not found: {results_dir}")
            sys.exit(1)
        generate_review(results_dir, output_dir)

    elif args.revalidate:
        review_path  = Path(args.review)
        material_dir = Path(args.material)
        if not review_path.exists():
            print(f"[Revalidate] ERROR: review file not found: {review_path}")
            sys.exit(1)
        if not material_dir.exists():
            print(f"[Revalidate] ERROR: material folder not found: {material_dir}")
            sys.exit(1)
        run_revalidation(review_path, output_dir, material_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
