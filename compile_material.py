"""
compile_material.py — Synthesise all safe-material PDFs into a structured safe-overview.md.

Usage:
  python compile_material.py
  python compile_material.py --material M:/screen-scraper/safe-material
  python compile_material.py --output   M:/screen-scraper/safe-material/safe-overview.md
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env", override=True)

import anthropic

MODEL = "claude-haiku-4-5-20251001"
MAX_CHUNK_CHARS = 80_000   # ~20k tokens per batch


def extract_pdf_text(folder: Path) -> str:
    """Extract all text from PDFs and MD files in the folder (excluding safe-overview.md)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERROR: pypdf is required. Run: pip install pypdf")
        sys.exit(1)

    chunks = []

    for pdf_path in sorted(folder.glob("*.pdf")):
        try:
            reader = PdfReader(str(pdf_path))
            pages_text = []
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    pages_text.append(f"[p.{page_num}] {text.strip()}")
            if pages_text:
                chunks.append(f"\n\n=== {pdf_path.name} ===\n" + "\n".join(pages_text))
                print(f"  Read {pdf_path.name} ({len(reader.pages)} pages)")
        except Exception as exc:
            print(f"  WARNING: skipping {pdf_path.name}: {exc}")

    for md_path in sorted(folder.glob("*.md")):
        if md_path.name.lower() == "safe-overview.md":
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
            if text.strip():
                chunks.append(f"\n\n=== {md_path.name} ===\n{text.strip()}")
                print(f"  Read {md_path.name}")
        except Exception as exc:
            print(f"  WARNING: skipping {md_path.name}: {exc}")

    return "\n".join(chunks)


SYNTHESIS_PROMPT = """\
You are a SAFe LPM knowledge compiler. Below is the full text extracted from all SAFe \
training material PDFs. Your task is to synthesise this into a single, structured \
Markdown reference document that is optimised for both human reading and keyword-based \
information retrieval.

IMPORTANT RULES:
- Use SAFe exam terminology alongside source material wording (e.g. "current Solutions \
  (Horizon 1)", "flow velocity = increased productivity metric")
- Be comprehensive — do not omit content
- Use tables wherever possible for structured data
- Include an "Also known as / Exam phrasing" column in every table where relevant

REQUIRED SECTIONS AND TABLE STRUCTURES:

# SAFe LPM Overview

## Key Concepts and Definitions
| Term / Abbreviation | Full name | Definition | Also known as / Exam phrasing |

## Horizons
| Horizon | Name | Focus | Investment type | Current/Emerging/Future | Also known as |

## Metrics and Measures
| Metric | What it measures | Applies to | Also called / Exam phrasing |

## Ceremonies and Events
| Ceremony / Event | Cadence | Purpose | Inputs | Key Activities | Outputs | Participants |

## Roles and Responsibilities
| Role | Short description | Key responsibilities | Works with |

## Teams and Structures
| Team / Structure | Purpose | Key ceremonies | Key inputs | Key outputs |

## Portfolio Kanban States
| State | Sub-states | Entry criteria | Exit criteria | Key activities |

## Lean Budget Guardrails
| Guardrail | Purpose | Key rule |

## Epic Lifecycle
| Phase | Description | Key activities | Decision point |

SOURCE MATERIAL:
{material}

Write ONLY the Markdown document — no preamble, no commentary."""


def synthesise(material_text: str, client: anthropic.Anthropic) -> str:
    """Send material to Claude and return the structured MD."""

    # If material fits in one call, do it directly
    if len(material_text) <= MAX_CHUNK_CHARS:
        prompt = SYNTHESIS_PROMPT.format(material=material_text)
        print(f"  Sending {len(material_text):,} chars to Claude ...")
        response = client.messages.create(
            model=MODEL,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    # Otherwise split into chunks and merge
    print(f"  Material too large ({len(material_text):,} chars) — processing in chunks ...")
    chunks = []
    start = 0
    while start < len(material_text):
        chunks.append(material_text[start:start + MAX_CHUNK_CHARS])
        start += MAX_CHUNK_CHARS

    partial_results = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"  Chunk {i}/{len(chunks)} ({len(chunk):,} chars) ...")
        prompt = SYNTHESIS_PROMPT.format(material=chunk)
        response = client.messages.create(
            model=MODEL,
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        partial_results.append(response.content[0].text)

    # Merge chunks — send partials back to Claude for consolidation
    print("  Merging chunks ...")
    merge_prompt = (
        "You are merging multiple partial SAFe LPM reference documents into one. "
        "Combine all tables, deduplicate rows, and produce a single clean Markdown document "
        "with the same section structure. Write ONLY the Markdown — no preamble.\n\n"
        + "\n\n---NEXT PART---\n\n".join(partial_results)
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": merge_prompt}],
    )
    return response.content[0].text


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile SAFe PDFs into a structured MD overview.")
    parser.add_argument("--material", default=str(Path(__file__).parent / "safe-material"),
                        help="Folder with SAFe PDF/MD source material")
    parser.add_argument("--output", default=None,
                        help="Output path (default: safe-material/safe-overview.md)")
    args = parser.parse_args()

    material_dir = Path(args.material)
    output_path  = Path(args.output) if args.output else material_dir / "safe-overview.md"

    if not material_dir.exists():
        print(f"ERROR: material folder not found: {material_dir}")
        sys.exit(1)

    print(f"[Compiler] Extracting text from {material_dir} ...")
    material_text = extract_pdf_text(material_dir)
    print(f"[Compiler] Total extracted: {len(material_text):,} chars")

    if not material_text.strip():
        print("[Compiler] ERROR: no text extracted.")
        sys.exit(1)

    client = anthropic.Anthropic()

    print("[Compiler] Synthesising structured overview ...")
    result = synthesise(material_text, client)

    output_path.write_text(result, encoding="utf-8")
    print(f"[Compiler] Written to {output_path}  ({len(result):,} chars)")


if __name__ == "__main__":
    main()
