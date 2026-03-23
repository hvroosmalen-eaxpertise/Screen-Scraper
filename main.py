"""
main.py — Screen-Scraper entry point.

Usage:
  python main.py --mode once              # capture once and extract Q&A
  python main.py --mode hotkey            # listen for hotkey (requires admin)
  python main.py --mode hotkey --hotkey ctrl+grave --monitor 1
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Load .env BEFORE any os.getenv() calls — override=True ensures .env wins
# even if the variable is already set (empty) in the system environment
load_dotenv(override=True)


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
        "--monitor",
        type=int,
        default=1,
        help="Monitor index: 1=primary, 0=all combined (default: 1)",
    )
    args = parser.parse_args()

    check_api_key()

    if args.mode == "once":
        from scraper.capture import take_screenshot
        from scraper.extractor import extract_qa
        from scraper.output import save_result

        path = take_screenshot(monitor_index=args.monitor)
        data = extract_qa(path)
        save_result(data, path)

    elif args.mode == "hotkey":
        from scraper.hotkey import start_listener
        start_listener(hotkey=args.hotkey, monitor_index=args.monitor)


if __name__ == "__main__":
    main()
