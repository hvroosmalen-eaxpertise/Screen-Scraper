"""
main.py — Screen-Scraper entry point.

Usage:
  python main.py                          # hotkey mode; auto-enables solver if safe-material/ has PDFs
  python main.py --mode once              # capture once and extract Q&A
  python main.py --no-solve               # disable solver even if safe-material/ exists
  python main.py --material path/to/pdfs  # use a different PDF folder
"""

import argparse
import os
import sys
from dotenv import load_dotenv

from scraper.paths import BASE_DIR

# Load .env BEFORE any os.getenv() calls — override=True ensures .env wins
# even if the variable is already set (empty) in the system environment
load_dotenv(BASE_DIR / ".env", override=True)


def prompt_for_api_key() -> None:
    """If no .env exists, ask the user for their API key and save it."""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        print("Welcome to Screen-Scraper!")
        print("No .env file found. Please enter your Anthropic API key.")
        print("(Get one at https://console.anthropic.com/settings/api-keys)\n")
        key = input("ANTHROPIC_API_KEY: ").strip()
        if key:
            env_path.write_text(f"ANTHROPIC_API_KEY={key}\n", encoding="utf-8")
            print(f"Saved to {env_path}\n")
            load_dotenv(env_path, override=True)


def check_api_key() -> None:
    """Exit with a clear message if ANTHROPIC_API_KEY is not set."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("Copy .env.example to .env and add your key.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Screen-Scraper: capture screenshot and extract Q&A with Claude Vision."
    )
    parser.add_argument(
        "--mode",
        choices=["once", "hotkey"],
        default="hotkey",
        help="Run once or listen for hotkey (default: hotkey)",
    )
    parser.add_argument(
        "--hotkey",
        default="ctrl+grave",
        help="Hotkey to trigger scrape in hotkey mode (default: ctrl+grave i.e. Ctrl+`)",
    )
    parser.add_argument(
        "--stop-hotkey",
        default="ctrl+q",
        help="Hotkey to stop the listener in hotkey mode (default: ctrl+q)",
    )
    parser.add_argument(
        "--monitor",
        type=int,
        default=1,
        help="Monitor index: 1=primary, 0=all combined (default: 1)",
    )
    parser.add_argument(
        "--no-solve",
        action="store_true",
        help="Disable SAFe/LPM answer solver even if safe-material/ folder exists",
    )
    parser.add_argument(
        "--material",
        default=None,
        help="Path to folder with source PDFs (default: safe-material/ next to main.py)",
    )
    args = parser.parse_args()

    prompt_for_api_key()
    check_api_key()

    # Auto-enable solver if safe-material/ has PDFs, unless --no-solve is set
    from pathlib import Path
    material = None
    if not args.no_solve:
        if args.material:
            material_dir = Path(args.material)
        elif getattr(sys, "frozen", False):
            # PyInstaller 6+: data files are in _MEIPASS (_internal/ for folder builds)
            material_dir = Path(sys._MEIPASS) / "safe-material"
        else:
            material_dir = BASE_DIR / "safe-material"
        if material_dir.is_dir() and any(material_dir.glob("*.pdf")):
            from scraper.safe_lpm_solver import MaterialIndex
            material = MaterialIndex(material_dir)
            print("=" * 45)
            print("  SAFe/LPM Solver ready. Starting exam mode.")
            print(f"  Press [{args.hotkey}] to capture a question.")
            print(f"  Press [{args.stop_hotkey}] to stop.")
            print("=" * 45 + "\n")

    if args.mode == "once":
        from scraper.capture import take_screenshot
        from scraper.extractor import extract_qa
        from scraper.output import save_result

        path = take_screenshot(monitor_index=args.monitor)
        data = extract_qa(path)
        if material is not None:
            from scraper.safe_lpm_solver import solve_all
            solve_all(data, material)
        save_result(data, path)

    elif args.mode == "hotkey":
        from scraper.hotkey import start_listener
        start_listener(
            hotkey=args.hotkey,
            stop_hotkey=args.stop_hotkey,
            monitor_index=args.monitor,
            material=material,
        )


if __name__ == "__main__":
    main()
