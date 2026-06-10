import { Coin, FearGreed, fmtBig, fmtUsd } from "./coingecko";
import { Signal } from "./signals";

export interface BriefInput {
  coins: Coin[];
  signals: Signal[];
  fearGreed: FearGreed | null;
}

/**
 * Generates the daily market brief. Uses the Claude API when
 * ANTHROPIC_API_KEY is set; otherwise falls back to a deterministic,
 * data-driven summary so the product works out of the box.
 * Every numeric claim in the AI path is grounded in the snapshot we pass in.
 */
export async function generateBrief(input: BriefInput): Promise<{ text: string; engine: "claude" | "rules" }> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (apiKey) {
    try {
      const text = await claudeBrief(apiKey, input);
      return { text, engine: "claude" };
    } catch {
      // fall through to deterministic brief
    }
  }
  return { text: rulesBrief(input), engine: "rules" };
}

function snapshot(input: BriefInput): string {
  const lines = input.coins.slice(0, 12).map((c) => {
    const ch24 = c.price_change_percentage_24h?.toFixed(2) ?? "n/a";
    const ch7d = c.price_change_percentage_7d_in_currency?.toFixed(2) ?? "n/a";
    return `${c.name} (${c.symbol.toUpperCase()}): price=${c.current_price}, 24h=${ch24}%, 7d=${ch7d}%, mcap=${c.market_cap}`;
  });
  const sig = input.signals
    .slice(0, 8)
    .map((s) => `${s.symbol}: ${s.direction} (${s.confidence}%) — ${s.reasons.join("; ")}`);
  const fg = input.fearGreed
    ? `Fear & Greed: ${input.fearGreed.value} (${input.fearGreed.classification})`
    : "Fear & Greed: unavailable";
  return `MARKET DATA:\n${lines.join("\n")}\n\nSIGNALS:\n${sig.join("\n")}\n\n${fg}`;
}

async function claudeBrief(apiKey: string, input: BriefInput): Promise<string> {
  const model = process.env.BRIEF_MODEL || "claude-sonnet-4-6";
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model,
      max_tokens: 700,
      system:
        "You are the research desk of a crypto intelligence platform. Write a tight daily market brief " +
        "(4 short sections: Market Pulse, Standouts, Signal Desk, Risk Note). Only use numbers present in " +
        "the provided data — never invent figures. No financial advice; analytical tone. Plain text, no markdown headers heavier than a single line.",
      messages: [{ role: "user", content: snapshot(input) }]
    })
  });
  if (!res.ok) throw new Error(`Anthropic ${res.status}`);
  const json = await res.json();
  const text = json?.content?.[0]?.text;
  if (typeof text !== "string") throw new Error("empty completion");
  return text;
}

function rulesBrief(input: BriefInput): string {
  const { coins, signals, fearGreed } = input;
  const btc = coins.find((c) => c.id === "bitcoin");
  const sorted = [...coins].sort(
    (a, b) => (b.price_change_percentage_24h ?? 0) - (a.price_change_percentage_24h ?? 0)
  );
  const top = sorted[0];
  const bottom = sorted[sorted.length - 1];
  const buys = signals.filter((s) => s.direction === "BUY");
  const sells = signals.filter((s) => s.direction === "SELL");
  const totalMcap = coins.reduce((a, c) => a + c.market_cap, 0);

  const parts: string[] = [];
  parts.push(
    `MARKET PULSE — Combined top-${coins.length} market cap stands at ${fmtBig(totalMcap)}.` +
      (btc
        ? ` Bitcoin trades at ${fmtUsd(btc.current_price)} (${(btc.price_change_percentage_24h ?? 0).toFixed(2)}% / 24h).`
        : "") +
      (fearGreed ? ` Sentiment gauge: ${fearGreed.value}/100 (${fearGreed.classification}).` : "")
  );
  if (top && bottom) {
    parts.push(
      `STANDOUTS — Best 24h performer: ${top.name} (${(top.price_change_percentage_24h ?? 0).toFixed(2)}%). ` +
        `Weakest: ${bottom.name} (${(bottom.price_change_percentage_24h ?? 0).toFixed(2)}%).`
    );
  }
  parts.push(
    `SIGNAL DESK — Engine flags ${buys.length} BUY and ${sells.length} SELL setups across the universe. ` +
      (buys[0]
        ? `Highest-conviction long: ${buys[0].name} (${buys[0].confidence}%) — ${buys[0].reasons[0]}.`
        : `No high-conviction longs right now.`) +
      (sells[0] ? ` Top short flag: ${sells[0].name} (${sells[0].confidence}%).` : "")
  );
  parts.push(
    `RISK NOTE — Signals are systematic, hourly-timeframe technical reads, not investment advice. ` +
      `Size positions assuming any single signal can fail.`
  );
  return parts.join("\n\n");
}
