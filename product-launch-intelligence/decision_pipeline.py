"""
decision_pipeline.py — Decision Pack agent pipeline orchestrator
Runs 6 Claude agents in sequence, each receiving all previous outputs as context.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field

import anthropic

from scraper import ProductData


MODEL = "claude-sonnet-4-5"
MAX_TOKENS = 64000  # streaming; give agents plenty of room

DECISION_AGENTS_DIR = Path(__file__).parent / "agents" / "decision"

# Ordered list of (agent_key, display_name, system_prompt_file)
DECISION_AGENT_SEQUENCE = [
    ("feedback_synthesizer",   "Feedback Synthesizer",      "feedback_synthesizer.md"),
    ("paid_media_auditor",     "Paid Media Auditor",         "paid_media_auditor.md"),
    ("search_query_analyst",   "Search Query Analyst",       "search_query_analyst.md"),
    ("cross_border_specialist","Cross-Border Specialist",    "cross_border_specialist.md"),
    ("legal_compliance_checker","Legal & Compliance Checker","legal_compliance_checker.md"),
    ("reality_checker",        "Reality Checker",            "reality_checker.md"),
]


@dataclass
class DecisionAgentResult:
    key: str
    name: str
    output: str
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class DecisionPipelineResult:
    product: ProductData
    agent_results: list[DecisionAgentResult] = field(default_factory=list)

    def get_output(self, key: str) -> str:
        for r in self.agent_results:
            if r.key == key:
                return r.output
        return ""


def _load_decision_system_prompt(filename: str) -> str:
    """Load a decision agent system prompt from the agents/decision/ directory."""
    path = DECISION_AGENTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Decision agent system prompt not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def _build_user_message_for_decision_agent(
    agent_key: str,
    agent_name: str,
    product: ProductData,
    previous_results: list[DecisionAgentResult],
) -> str:
    """
    Build the user turn for a given decision agent.
    The first agent gets raw product data.
    Subsequent agents get a handoff header pointing to previous context in the conversation.
    """
    product_block = f"## Product Data\n\n{product.to_prompt_text()}"

    if agent_key == "feedback_synthesizer":
        return (
            f"{product_block}\n\n"
            "---\n\n"
            "**Business Context:** This analysis is prepared for a **dropshipping business**. "
            "All recommendations must be evaluated through a dropshipping lens: "
            "no inventory held, products sourced from AliExpress/CJ Dropshipping suppliers, "
            "margins must absorb supplier cost + shipping + platform fees without bulk pricing, "
            "and speed-to-market is a key advantage. "
            "Avoid recommendations that require custom manufacturing, large MOQs, or significant upfront capital.\n\n"
            "Please analyze this product and provide your full Feedback Synthesis report, "
            "focusing on competitor review gaps and unmet customer needs in this category."
        )

    # Build a short summary of what has already been produced
    prior_names = [r.name for r in previous_results]
    prior_summary = ", ".join(prior_names)

    return (
        f"The conversation above contains the full outputs from: **{prior_summary}**.\n\n"
        f"You are now the **{agent_name}**. "
        "Drawing on all prior analysis and the original product data, "
        "please produce your complete report as defined in your system prompt."
    )


def _stream_decision_agent(
    client: anthropic.Anthropic,
    system_prompt: str,
    messages: list[dict],
    agent_name: str,
    verbose: bool,
) -> tuple[str, int, int]:
    """
    Stream a single decision agent call. Returns (output_text, input_tokens, output_tokens).
    Uses streaming + get_final_message() to handle long outputs without timeout risk.
    """
    if verbose:
        print(f"\n{'─' * 60}")
        print(f"  Running: {agent_name}")
        print(f"{'─' * 60}\n")

    collected_text = []

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=messages,
        thinking={"type": "adaptive"},
    ) as stream:
        for event in stream:
            if (
                event.type == "content_block_delta"
                and hasattr(event.delta, "type")
                and event.delta.type == "text_delta"
            ):
                chunk = event.delta.text
                collected_text.append(chunk)
                if verbose:
                    print(chunk, end="", flush=True)

        final = stream.get_final_message()

    if verbose:
        print()  # newline after streaming

    # Extract full text from final message (handles thinking blocks correctly)
    full_text = "".join(collected_text)
    if not full_text:
        # Fallback: extract text blocks from final message content
        for block in final.content:
            if block.type == "text":
                full_text = block.text
                break

    input_tokens = final.usage.input_tokens if final.usage else 0
    output_tokens = final.usage.output_tokens if final.usage else 0

    return full_text, input_tokens, output_tokens


def run_decision_pipeline(product: ProductData, verbose: bool = True) -> DecisionPipelineResult:
    """
    Run all 6 decision agents in sequence.

    Message array structure (grows with each agent):
    - user: product data + agent 1 task
    - assistant: agent 1 output
    - user: agent 2 task (references prior context)
    - assistant: agent 2 output
    - ... and so on

    Each agent call passes the full accumulated messages array so every agent
    has complete context of all prior agents' outputs.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key."
        )

    client = anthropic.Anthropic(api_key=api_key)
    result = DecisionPipelineResult(product=product)

    # Shared conversation history — grows after each agent
    messages: list[dict] = []

    for agent_key, agent_name, prompt_file in DECISION_AGENT_SEQUENCE:
        system_prompt = _load_decision_system_prompt(prompt_file)

        # Build the next user message and append it
        user_msg = _build_user_message_for_decision_agent(
            agent_key, agent_name, product, result.agent_results
        )
        messages.append({"role": "user", "content": user_msg})

        # Stream this agent's response
        output_text, in_tok, out_tok = _stream_decision_agent(
            client=client,
            system_prompt=system_prompt,
            messages=messages,
            agent_name=agent_name,
            verbose=verbose,
        )

        # Append assistant response to the shared history
        messages.append({"role": "assistant", "content": output_text})

        agent_result = DecisionAgentResult(
            key=agent_key,
            name=agent_name,
            output=output_text,
            input_tokens=in_tok,
            output_tokens=out_tok,
        )
        result.agent_results.append(agent_result)

        if verbose:
            print(
                f"\n[{agent_name}] Complete — "
                f"{in_tok:,} input tokens / {out_tok:,} output tokens"
            )

    return result
