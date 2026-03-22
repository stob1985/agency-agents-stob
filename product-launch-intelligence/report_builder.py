"""
report_builder.py — Formats the pipeline output into a structured markdown report.
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from pipeline import PipelineResult


REPORTS_DIR = Path(__file__).parent / "reports"

SECTION_DIVIDER = "\n\n---\n\n"

AGENT_SECTION_HEADERS = {
    "trend_researcher":  "## 1. Trend Research",
    "ad_creative":       "## 2. Ad Creative Strategy",
    "ugc_writer":        "## 3. UGC Scripts & Content",
    "unit_economics":    "## 4. Unit Economics & Financial Model",
    "execution_planner": "## 5. Execution Plan & Launch Roadmap",
}


def _slugify(text: str) -> str:
    """Convert text to a URL/filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text[:60]


def _build_report_header(result: PipelineResult) -> str:
    product = result.product
    now = datetime.now(tz=timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    total_input = sum(r.input_tokens for r in result.agent_results)
    total_output = sum(r.output_tokens for r in result.agent_results)

    lines = [
        f"# Product Launch Intelligence Report",
        f"### {product.title}",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Product** | {product.title} |",
        f"| **Vendor** | {product.vendor} |",
        f"| **Price** | {product.price} |",
        f"| **URL** | [{product.url}]({product.url}) |",
        f"| **Report Generated** | {now} |",
        f"| **Total Tokens Used** | {total_input + total_output:,} ({total_input:,} input / {total_output:,} output) |",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
        "1. [Trend Research](#1-trend-research)",
        "2. [Ad Creative Strategy](#2-ad-creative-strategy)",
        "3. [UGC Scripts & Content](#3-ugc-scripts--content)",
        "4. [Unit Economics & Financial Model](#4-unit-economics--financial-model)",
        "5. [Execution Plan & Launch Roadmap](#5-execution-plan--launch-roadmap)",
        "6. [Raw Product Data](#6-raw-product-data)",
        "7. [Pipeline Metadata](#7-pipeline-metadata)",
    ]
    return "\n".join(lines)


def _build_product_data_section(result: PipelineResult) -> str:
    product = result.product
    lines = [
        "## 6. Raw Product Data",
        "",
        "```",
        product.to_prompt_text(),
        "```",
    ]
    return "\n".join(lines)


def _build_metadata_section(result: PipelineResult) -> str:
    lines = [
        "## 7. Pipeline Metadata",
        "",
        "| Agent | Input Tokens | Output Tokens | Total |",
        "|-------|-------------|---------------|-------|",
    ]
    total_in = total_out = 0
    for r in result.agent_results:
        total = r.input_tokens + r.output_tokens
        lines.append(
            f"| {r.name} | {r.input_tokens:,} | {r.output_tokens:,} | {total:,} |"
        )
        total_in += r.input_tokens
        total_out += r.output_tokens

    grand_total = total_in + total_out
    lines += [
        f"| **TOTAL** | **{total_in:,}** | **{total_out:,}** | **{grand_total:,}** |",
        "",
        f"*Model: `claude-opus-4-6` with adaptive thinking*",
    ]
    return "\n".join(lines)


def build_report(result: PipelineResult) -> str:
    """
    Assemble the full markdown report from all agent outputs.
    Returns the complete report as a string.
    """
    sections = [_build_report_header(result)]

    for agent_result in result.agent_results:
        header = AGENT_SECTION_HEADERS.get(agent_result.key, f"## {agent_result.name}")
        token_note = (
            f"*{agent_result.input_tokens:,} input tokens / "
            f"{agent_result.output_tokens:,} output tokens*"
        )
        section = "\n\n".join([header, token_note, agent_result.output])
        sections.append(section)

    sections.append(_build_product_data_section(result))
    sections.append(_build_metadata_section(result))

    return SECTION_DIVIDER.join(sections)


def save_report(result: PipelineResult, output_dir: Path | None = None) -> Path:
    """
    Save the markdown report to a file and return the file path.

    File naming: reports/<slug>_<timestamp>.md
    """
    out_dir = output_dir or REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(result.product.title)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_{timestamp}.md"
    filepath = out_dir / filename

    report_text = build_report(result)
    filepath.write_text(report_text, encoding="utf-8")

    return filepath
