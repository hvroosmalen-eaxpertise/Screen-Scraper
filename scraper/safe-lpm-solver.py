"""
safe-lpm-solver.py — Find correct answers to SAFe/LPM exam questions using source material PDFs.

Workflow:
  1. MaterialIndex loads and indexes all PDFs in a folder (once at startup).
  2. For each question, find_relevant() scores pages by keyword overlap.
  3. solve_question() sends the top pages + question to Claude for the answer,
     returning a confidence percentage, why the answer is correct, and why each
     other option is wrong.
  4. solve_all() enriches an extract_qa() result dict in place.
"""

import json
import re
from pathlib import Path
from typing import Optional

import anthropic


MODEL = "claude-haiku-4-5-20251001"

_SOLVE_PROMPT = """\
You are a SAFe/LPM certification exam assistant. \
Using ONLY the provided source material excerpts, determine the correct answer(s).

SOURCE MATERIAL:
{context}

QUESTION: {question}

SELECTION TYPE: {selection_type}

OPTIONS:
{options}

Return ONLY valid JSON — no markdown fences, no extra text:
{{
  "answer": <string for single-select, e.g. "B"  —OR—  list for multi-select, e.g. ["A", "C"]>,
  "confidence": <integer 0-100, your certainty based on the material>,
  "why": "<one sentence from the source material explaining why the correct answer(s) are right>",
  "why_not": {{
    "<option label>": "<one sentence why this option is wrong>"
  }},
  "source": "<filename and page, e.g. SAFe_Explained_Ebook_2025.pdf p.12>"
}}

Notes:
- For SINGLE-SELECT: "answer" is a single label string; "why_not" covers every other option.
- For MULTI-SELECT: "answer" is a list of all correct labels; "why_not" covers only the incorrect options.
- If the source material does not clearly address the question, lower confidence accordingly.
- Use the option labels exactly as given (e.g. "A", "1", or the full option text)."""


class MaterialIndex:
    """Loads and indexes all PDF pages from a folder at startup for fast retrieval."""

    def __init__(self, folder: Path) -> None:
        self.pages: list[dict] = []  # {"text", "source", "page"}
        self._load(folder)

    def _load(self, folder: Path) -> None:
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError(
                "pypdf is required for solve mode.  Run:  pip install pypdf"
            )

        pdf_files = sorted(folder.glob("*.pdf"))
        md_files = sorted(folder.glob("*.md"))

        if not pdf_files and not md_files:
            print(f"[Solver] WARNING: no PDF or MD files found in {folder}")
            return

        print(f"[Solver] Pre-reading {len(pdf_files)} PDF(s) and {len(md_files)} MD file(s) — please wait ...")

        for pdf_path in pdf_files:
            try:
                reader = PdfReader(str(pdf_path))
                count = 0
                for page_num, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""
                    if text.strip():
                        self.pages.append(
                            {"text": text, "source": pdf_path.name, "page": page_num}
                        )
                        count += 1
                print(f"[Solver]   {pdf_path.name}  ({count} pages)")
            except Exception as exc:
                print(f"[Solver] WARNING: skipping {pdf_path.name}: {exc}")

        for md_path in md_files:
            try:
                text = md_path.read_text(encoding="utf-8")
                if text.strip():
                    self.pages.append(
                        {"text": text, "source": md_path.name, "page": 1}
                    )
                    print(f"[Solver]   {md_path.name}")
            except Exception as exc:
                print(f"[Solver] WARNING: skipping {md_path.name}: {exc}")

        print(
            f"[Solver] Ready — {len(self.pages)} entries indexed.\n"
        )

    @property
    def ready(self) -> bool:
        return len(self.pages) > 0

    def find_relevant(self, query: str, top_n: int = 12) -> list[dict]:
        """Return up to top_n pages ranked by 4+ letter keyword overlap with query."""
        query_words = set(re.findall(r"\b\w{4,}\b", query.lower()))
        if not query_words or not self.pages:
            return self.pages[:top_n]

        scored = sorted(
            self.pages,
            key=lambda p: len(query_words & set(re.findall(r"\b\w{4,}\b", p["text"].lower()))),
            reverse=True,
        )
        return scored[:top_n]


def solve_question(
    question: str,
    options: Optional[list[str]],
    material: MaterialIndex,
    multi_select: bool = False,
) -> dict:
    """Ask Claude to pick the correct answer(s) using pre-loaded source material.

    Returns a dict with keys: answer (str or list), confidence (int 0-100), why, why_not (dict), source.
    """
    query = question + (" " + " ".join(options) if options else "")
    relevant = material.find_relevant(query)

    context = "\n\n---\n\n".join(
        f"[{p['source']}, p.{p['page']}]\n{p['text'][:1800]}"
        for p in relevant
    )

    options_text = (
        "\n".join(f"  {opt}" for opt in options)
        if options
        else "(open question — provide the correct short answer)"
    )

    selection_type = (
        "MULTI-SELECT (checkboxes — one or more answers may be correct, return a list)"
        if multi_select
        else "SINGLE-SELECT (radio buttons — exactly one answer is correct, return a string)"
    )

    prompt = _SOLVE_PROMPT.format(
        context=context,
        question=question,
        options=options_text,
        selection_type=selection_type,
    )

    client = anthropic.Anthropic()
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.APIError as exc:
        return {
            "answer": None,
            "confidence": 0,
            "why": f"API error: {exc}",
            "why_not": {},
            "source": "",
        }

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"why": raw[:200]}

    result.setdefault("answer", [] if multi_select else None)
    result.setdefault("confidence", 0)
    result.setdefault("why", "")
    result.setdefault("why_not", {})
    result.setdefault("source", "")

    # Clamp confidence to 0-100
    try:
        result["confidence"] = max(0, min(100, int(result["confidence"])))
    except (TypeError, ValueError):
        result["confidence"] = 0

    # Normalise answer type — multi-select should always be a list
    if multi_select and isinstance(result["answer"], str):
        result["answer"] = [result["answer"]] if result["answer"] else []

    return result


def solve_all(data: dict, material: MaterialIndex) -> dict:
    """Enrich each Q&A entry in an extract_qa() result with solver fields.

    Adds to each item: solved_answer, solved_confidence, solved_why, solved_why_not, solved_source.
    Returns the same dict (mutated in place).
    """
    for item in data.get("questions_and_answers", []):
        sol = solve_question(
            item.get("question", ""),
            item.get("options"),
            material,
            multi_select=item.get("multi_select", False),
        )
        item["solved_answer"] = sol["answer"]
        item["solved_confidence"] = sol["confidence"]
        item["solved_why"] = sol["why"]
        item["solved_why_not"] = sol["why_not"]
        item["solved_source"] = sol["source"]
    return data
