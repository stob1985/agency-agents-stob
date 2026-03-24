#!/usr/bin/env python3
"""
main.py — Product Launch Intelligence Report Generator

Usage:
    python main.py <shopify_product_url> [--output-dir <path>] [--quiet] [--mode <mode>]

Examples:
    python main.py https://example.myshopify.com/products/my-product
    python main.py https://example.com/products/my-product --output-dir ./my-reports
    python main.py https://example.com/products/my-product --quiet
    python main.py https://example.com/products/my-product --mode decision
    python main.py https://example.com/products/my-product --mode full
"""

import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

from scraper import scrape_product
from pipeline import run_pipeline
from decision_pipeline import run_decision_pipeline
from report_builder import save_report, save_decision_report, save_full_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a product launch intelligence report from a Shopify URL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "url",
        help="The Shopify product URL to analyze.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to save the report (default: ./reports/).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress streaming output (only show progress lines).",
    )
    parser.add_argument(
        "--mode",
        choices=["launch", "decision", "full"],
        default="launch",
        help=(
            "Pipeline mode: "
            "'launch' runs the 5-agent launch pipeline (default), "
            "'decision' runs the 6-agent decision pack, "
            "'full' runs decision first then launch (11-agent report)."
        ),
    )
    return parser.parse_args()


def main() -> None:
    # Load .env file if present
    load_dotenv()

    args = parse_args()
    url = args.url.strip()
    verbose = not args.quiet
    mode = args.mode

    print(f"\n{'═' * 64}")
    print("  Product Launch Intelligence Report Generator")
    print(f"{'═' * 64}\n")
    print(f"  URL:  {url}")
    print(f"  Mode: {mode}\n")

    # ── Step 1: Scrape ────────────────────────────────────────────────────────
    print("[ 1/3 ] Scraping product data...")
    try:
        product = scrape_product(url)
    except Exception as e:
        print(f"\n  ERROR: Failed to scrape product data.\n  {e}", file=sys.stderr)
        sys.exit(1)

    print(f"         Title:  {product.title}")
    print(f"         Price:  {product.price}")
    print(f"         Vendor: {product.vendor}")
    print(f"         Reviews scraped: {len(product.reviews)}")

    decision_result = None
    launch_result = None

    # ── Step 2: Run pipeline(s) ───────────────────────────────────────────────
    if mode == "decision":
        print("\n[ 2/3 ] Running 6-agent Decision Pack pipeline...\n")
        try:
            decision_result = run_decision_pipeline(product, verbose=verbose)
        except EnvironmentError as e:
            print(f"\n  ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: Decision pipeline failed.\n  {e}", file=sys.stderr)
            sys.exit(1)

    elif mode == "launch":
        print("\n[ 2/3 ] Running 5-agent Launch Intelligence pipeline...\n")
        try:
            launch_result = run_pipeline(product, verbose=verbose)
        except EnvironmentError as e:
            print(f"\n  ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: Pipeline failed.\n  {e}", file=sys.stderr)
            sys.exit(1)

    elif mode == "full":
        print("\n[ 2/3 ] Running full 11-agent pipeline (Decision Pack → Launch Intelligence)...\n")
        print("  Phase 1 of 2: Decision Pack (6 agents)\n")
        try:
            decision_result = run_decision_pipeline(product, verbose=verbose)
        except EnvironmentError as e:
            print(f"\n  ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: Decision pipeline failed.\n  {e}", file=sys.stderr)
            sys.exit(1)

        print("\n  Phase 2 of 2: Launch Intelligence (5 agents)\n")
        try:
            launch_result = run_pipeline(product, verbose=verbose)
        except EnvironmentError as e:
            print(f"\n  ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"\n  ERROR: Launch pipeline failed.\n  {e}", file=sys.stderr)
            sys.exit(1)

    # ── Step 3: Save report ───────────────────────────────────────────────────
    print("\n[ 3/3 ] Building and saving report...")
    try:
        if mode == "decision":
            report_path = save_decision_report(decision_result, output_dir=args.output_dir)
            all_results = decision_result.agent_results
        elif mode == "launch":
            report_path = save_report(launch_result, output_dir=args.output_dir)
            all_results = launch_result.agent_results
        else:  # full
            report_path = save_full_report(decision_result, launch_result, output_dir=args.output_dir)
            all_results = decision_result.agent_results + launch_result.agent_results
    except Exception as e:
        print(f"\n  ERROR: Failed to save report.\n  {e}", file=sys.stderr)
        sys.exit(1)

    total_in = sum(r.input_tokens for r in all_results)
    total_out = sum(r.output_tokens for r in all_results)

    html_path = report_path.with_suffix(".html")

    print(f"\n{'═' * 64}")
    print("  Report complete!")
    print(f"{'═' * 64}")
    print(f"\n  Markdown: {report_path}")
    print(f"  HTML:     {html_path}")
    print(f"  Tokens:   {total_in + total_out:,} total ({total_in:,} in / {total_out:,} out)\n")


if __name__ == "__main__":
    main()
