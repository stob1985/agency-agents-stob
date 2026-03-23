"""
report_builder.py — Formats the pipeline output into a structured markdown report.
Handles launch reports, decision pack reports, and combined full reports.
"""

import re
from datetime import datetime, timezone
from pathlib import Path

from pipeline import PipelineResult
from decision_pipeline import DecisionPipelineResult


REPORTS_DIR = Path(__file__).parent / "reports"

SECTION_DIVIDER = "\n\n---\n\n"

AGENT_SECTION_HEADERS = {
    "trend_researcher":  "## 1. Trend Research",
    "ad_creative":       "## 2. Ad Creative Strategy",
    "ugc_writer":        "## 3. UGC Scripts & Content",
    "unit_economics":    "## 4. Unit Economics & Financial Model",
    "execution_planner": "## 5. Execution Plan & Launch Roadmap",
}

DECISION_AGENT_SECTION_HEADERS = {
    "feedback_synthesizer":    "## 1. Feedback Synthesis — Competitor Review Gaps",
    "paid_media_auditor":      "## 2. Paid Media Audit — Ad Spend & Creative Whitespace",
    "search_query_analyst":    "## 3. Search Query Analysis — Trends, Volume & Seasonality",
    "cross_border_specialist": "## 4. Cross-Border Sourcing — COGS & Margin Analysis",
    "legal_compliance_checker":"## 5. Legal & Compliance — Risk Assessment",
    "reality_checker":         "## 6. Reality Check — GO / NO-GO / PIVOT Verdict",
}

# In full mode, decision agents get a Part A prefix and launch agents get Part B
FULL_DECISION_SECTION_HEADERS = {
    "feedback_synthesizer":    "## A1. Feedback Synthesis — Competitor Review Gaps",
    "paid_media_auditor":      "## A2. Paid Media Audit — Ad Spend & Creative Whitespace",
    "search_query_analyst":    "## A3. Search Query Analysis — Trends, Volume & Seasonality",
    "cross_border_specialist": "## A4. Cross-Border Sourcing — COGS & Margin Analysis",
    "legal_compliance_checker":"## A5. Legal & Compliance — Risk Assessment",
    "reality_checker":         "## A6. Reality Check — GO / NO-GO / PIVOT Verdict",
}

FULL_LAUNCH_SECTION_HEADERS = {
    "trend_researcher":  "## B1. Trend Research",
    "ad_creative":       "## B2. Ad Creative Strategy",
    "ugc_writer":        "## B3. UGC Scripts & Content",
    "unit_economics":    "## B4. Unit Economics & Financial Model",
    "execution_planner": "## B5. Execution Plan & Launch Roadmap",
}


def _slugify(text: str) -> str:
    """Convert text to a URL/filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text[:60]


# ── Launch Report ─────────────────────────────────────────────────────────────

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


def _build_product_data_section(result: PipelineResult, section_num: int = 6) -> str:
    product = result.product
    lines = [
        f"## {section_num}. Raw Product Data",
        "",
        "```",
        product.to_prompt_text(),
        "```",
    ]
    return "\n".join(lines)


def _build_metadata_section(result: PipelineResult, section_num: int = 7) -> str:
    lines = [
        f"## {section_num}. Pipeline Metadata",
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
    Assemble the full markdown launch report from all agent outputs.
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
    Save the launch pipeline markdown report to a file and return the file path.

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


# ── Decision Report ───────────────────────────────────────────────────────────

def _build_decision_report_header(result: DecisionPipelineResult) -> str:
    product = result.product
    now = datetime.now(tz=timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    total_input = sum(r.input_tokens for r in result.agent_results)
    total_output = sum(r.output_tokens for r in result.agent_results)

    lines = [
        f"# Decision Pack Report",
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
        "1. [Feedback Synthesis — Competitor Review Gaps](#1-feedback-synthesis--competitor-review-gaps)",
        "2. [Paid Media Audit — Ad Spend & Creative Whitespace](#2-paid-media-audit--ad-spend--creative-whitespace)",
        "3. [Search Query Analysis — Trends, Volume & Seasonality](#3-search-query-analysis--trends-volume--seasonality)",
        "4. [Cross-Border Sourcing — COGS & Margin Analysis](#4-cross-border-sourcing--cogs--margin-analysis)",
        "5. [Legal & Compliance — Risk Assessment](#5-legal--compliance--risk-assessment)",
        "6. [Reality Check — GO / NO-GO / PIVOT Verdict](#6-reality-check--go--no-go--pivot-verdict)",
        "7. [Raw Product Data](#7-raw-product-data)",
        "8. [Pipeline Metadata](#8-pipeline-metadata)",
    ]
    return "\n".join(lines)


def _build_decision_product_data_section(result: DecisionPipelineResult) -> str:
    product = result.product
    lines = [
        "## 7. Raw Product Data",
        "",
        "```",
        product.to_prompt_text(),
        "```",
    ]
    return "\n".join(lines)


def _build_decision_metadata_section(result: DecisionPipelineResult) -> str:
    lines = [
        "## 8. Pipeline Metadata",
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


def build_decision_report(result: DecisionPipelineResult) -> str:
    """
    Assemble the full markdown Decision Pack report from all agent outputs.
    Returns the complete report as a string.
    """
    sections = [_build_decision_report_header(result)]

    for agent_result in result.agent_results:
        header = DECISION_AGENT_SECTION_HEADERS.get(agent_result.key, f"## {agent_result.name}")
        token_note = (
            f"*{agent_result.input_tokens:,} input tokens / "
            f"{agent_result.output_tokens:,} output tokens*"
        )
        section = "\n\n".join([header, token_note, agent_result.output])
        sections.append(section)

    sections.append(_build_decision_product_data_section(result))
    sections.append(_build_decision_metadata_section(result))

    return SECTION_DIVIDER.join(sections)


def save_decision_report(result: DecisionPipelineResult, output_dir: Path | None = None) -> Path:
    """
    Save the Decision Pack markdown report to a file and return the file path.

    File naming: reports/<slug>_decision_<timestamp>.md
    """
    out_dir = output_dir or REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(result.product.title)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_decision_{timestamp}.md"
    filepath = out_dir / filename

    report_text = build_decision_report(result)
    filepath.write_text(report_text, encoding="utf-8")

    return filepath


# ── Full Combined Report ──────────────────────────────────────────────────────

def _build_full_report_header(
    decision_result: DecisionPipelineResult,
    launch_result: PipelineResult,
) -> str:
    product = decision_result.product
    now = datetime.now(tz=timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
    all_results = decision_result.agent_results + launch_result.agent_results
    total_input = sum(r.input_tokens for r in all_results)
    total_output = sum(r.output_tokens for r in all_results)

    lines = [
        f"# Full Product Intelligence Report",
        f"### {product.title}",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Product** | {product.title} |",
        f"| **Vendor** | {product.vendor} |",
        f"| **Price** | {product.price} |",
        f"| **URL** | [{product.url}]({product.url}) |",
        f"| **Report Generated** | {now} |",
        f"| **Agents Run** | 11 (6 Decision Pack + 5 Launch Intelligence) |",
        f"| **Total Tokens Used** | {total_input + total_output:,} ({total_input:,} input / {total_output:,} output) |",
        "",
        "---",
        "",
        "## Table of Contents",
        "",
        "### Part A — Decision Pack",
        "",
        "- [A1. Feedback Synthesis — Competitor Review Gaps](#a1-feedback-synthesis--competitor-review-gaps)",
        "- [A2. Paid Media Audit — Ad Spend & Creative Whitespace](#a2-paid-media-audit--ad-spend--creative-whitespace)",
        "- [A3. Search Query Analysis — Trends, Volume & Seasonality](#a3-search-query-analysis--trends-volume--seasonality)",
        "- [A4. Cross-Border Sourcing — COGS & Margin Analysis](#a4-cross-border-sourcing--cogs--margin-analysis)",
        "- [A5. Legal & Compliance — Risk Assessment](#a5-legal--compliance--risk-assessment)",
        "- [A6. Reality Check — GO / NO-GO / PIVOT Verdict](#a6-reality-check--go--no-go--pivot-verdict)",
        "",
        "### Part B — Launch Intelligence",
        "",
        "- [B1. Trend Research](#b1-trend-research)",
        "- [B2. Ad Creative Strategy](#b2-ad-creative-strategy)",
        "- [B3. UGC Scripts & Content](#b3-ugc-scripts--content)",
        "- [B4. Unit Economics & Financial Model](#b4-unit-economics--financial-model)",
        "- [B5. Execution Plan & Launch Roadmap](#b5-execution-plan--launch-roadmap)",
        "",
        "### Appendices",
        "",
        "- [Raw Product Data](#raw-product-data)",
        "- [Pipeline Metadata](#pipeline-metadata)",
    ]
    return "\n".join(lines)


def _build_full_metadata_section(
    decision_result: DecisionPipelineResult,
    launch_result: PipelineResult,
) -> str:
    lines = [
        "## Pipeline Metadata",
        "",
        "### Part A — Decision Pack",
        "",
        "| Agent | Input Tokens | Output Tokens | Total |",
        "|-------|-------------|---------------|-------|",
    ]
    d_in = d_out = 0
    for r in decision_result.agent_results:
        total = r.input_tokens + r.output_tokens
        lines.append(f"| {r.name} | {r.input_tokens:,} | {r.output_tokens:,} | {total:,} |")
        d_in += r.input_tokens
        d_out += r.output_tokens

    lines += [
        f"| **Decision Subtotal** | **{d_in:,}** | **{d_out:,}** | **{d_in + d_out:,}** |",
        "",
        "### Part B — Launch Intelligence",
        "",
        "| Agent | Input Tokens | Output Tokens | Total |",
        "|-------|-------------|---------------|-------|",
    ]
    l_in = l_out = 0
    for r in launch_result.agent_results:
        total = r.input_tokens + r.output_tokens
        lines.append(f"| {r.name} | {r.input_tokens:,} | {r.output_tokens:,} | {total:,} |")
        l_in += r.input_tokens
        l_out += r.output_tokens

    grand_in = d_in + l_in
    grand_out = d_out + l_out
    lines += [
        f"| **Launch Subtotal** | **{l_in:,}** | **{l_out:,}** | **{l_in + l_out:,}** |",
        "",
        f"| **GRAND TOTAL** | **{grand_in:,}** | **{grand_out:,}** | **{grand_in + grand_out:,}** |",
        "",
        f"*Model: `claude-opus-4-6` with adaptive thinking*",
    ]
    return "\n".join(lines)


def build_full_report(
    decision_result: DecisionPipelineResult,
    launch_result: PipelineResult,
) -> str:
    """
    Assemble the combined 11-agent report (Decision Pack + Launch Intelligence).
    Returns the complete report as a string.
    """
    sections = [_build_full_report_header(decision_result, launch_result)]

    # Part A — Decision Pack
    sections.append("# Part A — Decision Pack")
    for agent_result in decision_result.agent_results:
        header = FULL_DECISION_SECTION_HEADERS.get(agent_result.key, f"## {agent_result.name}")
        token_note = (
            f"*{agent_result.input_tokens:,} input tokens / "
            f"{agent_result.output_tokens:,} output tokens*"
        )
        section = "\n\n".join([header, token_note, agent_result.output])
        sections.append(section)

    # Part B — Launch Intelligence
    sections.append("# Part B — Launch Intelligence")
    for agent_result in launch_result.agent_results:
        header = FULL_LAUNCH_SECTION_HEADERS.get(agent_result.key, f"## {agent_result.name}")
        token_note = (
            f"*{agent_result.input_tokens:,} input tokens / "
            f"{agent_result.output_tokens:,} output tokens*"
        )
        section = "\n\n".join([header, token_note, agent_result.output])
        sections.append(section)

    # Appendices
    product = decision_result.product
    raw_data_section = "\n".join([
        "## Raw Product Data",
        "",
        "```",
        product.to_prompt_text(),
        "```",
    ])
    sections.append(raw_data_section)
    sections.append(_build_full_metadata_section(decision_result, launch_result))

    return SECTION_DIVIDER.join(sections)


def save_full_report(
    decision_result: DecisionPipelineResult,
    launch_result: PipelineResult,
    output_dir: Path | None = None,
) -> Path:
    """
    Save the combined full report to a file and return the file path.

    File naming: reports/<slug>_full_<timestamp>.md
    """
    out_dir = output_dir or REPORTS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(decision_result.product.title)
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{slug}_full_{timestamp}.md"
    filepath = out_dir / filename

    report_text = build_full_report(decision_result, launch_result)
    filepath.write_text(report_text, encoding="utf-8")

    return filepath
