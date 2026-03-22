#!/usr/bin/env python3
"""
main.py — Product Launch Intelligence Report Generator

Usage:
    python main.py <shopify_product_url> [--output-dir <path>] [--quiet]

Examples:
    python main.py https://example.myshopify.com/products/my-product
    python main.py https://example.com/products/my-product --output-dir ./my-reports
    python main.py https://example.com/products/my-product --quiet
"""

import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

from scraper import scrape_product
from pipeline import run_pipeline
from report_builder import save_report


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
    return parser.parse_args()


def main() -> None:
    # Load .env file if present
    load_dotenv()

    args = parse_args()
    url = args.url.strip()
    verbose = not args.quiet

    print(f"\n{'═' * 64}")
    print("  Product Launch Intelligence Report Generator")
    print(f"{'═' * 64}\n")
    print(f"  URL: {url}\n")

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

    # ── Step 2: Run pipeline ──────────────────────────────────────────────────
    print("\n[ 2/3 ] Running 5-agent intelligence pipeline...\n")
    try:
        result = run_pipeline(product, verbose=verbose)
    except EnvironmentError as e:
        print(f"\n  ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n  ERROR: Pipeline failed.\n  {e}", file=sys.stderr)
        sys.exit(1)

    # ── Step 3: Save report ───────────────────────────────────────────────────
    print("\n[ 3/3 ] Building and saving report...")
    try:
        report_path = save_report(result, output_dir=args.output_dir)
    except Exception as e:
        print(f"\n  ERROR: Failed to save report.\n  {e}", file=sys.stderr)
        sys.exit(1)

    total_in = sum(r.input_tokens for r in result.agent_results)
    total_out = sum(r.output_tokens for r in result.agent_results)

    print(f"\n{'═' * 64}")
    print("  Report complete!")
    print(f"{'═' * 64}")
    print(f"\n  Saved to: {report_path}")
    print(f"  Tokens:   {total_in + total_out:,} total ({total_in:,} in / {total_out:,} out)\n")


if __name__ == "__main__":
    main()
