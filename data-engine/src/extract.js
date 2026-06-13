import {
  TOKENS,
  NARRATIVES,
  NARRATIVE_KEYWORDS,
  EVENT_TYPES,
  EVENT_KEYWORDS,
  POS_WORDS,
  NEG_WORDS
} from "./taxonomy.js";

// ── Extraction: article -> { tokens, sentiment, narratives, event, model } ──
// This is the "factory floor". The Claude path is the production extractor;
// the rules path is a deterministic fallback so the engine runs with zero keys
// and so the LLM output can always be validated against the same taxonomy.

const TICKERS = Object.keys(TOKENS);

// Build a lowercase alias -> ticker lookup for the rules extractor.
const ALIAS_MAP = (() => {
  const m = new Map();
  for (const [tic, { name, aliases }] of Object.entries(TOKENS)) {
    m.set(tic.toLowerCase(), tic);
    m.set(name.toLowerCase(), tic);
    for (const a of aliases) m.set(a.toLowerCase(), tic);
  }
  return m;
})();

function clamp(n, lo, hi) {
  return Math.max(lo, Math.min(hi, n));
}

// Keep only tickers we recognise; uppercase + dedupe.
function normalizeTokens(arr) {
  const out = new Set();
  for (const t of arr || []) {
    const up = String(t).toUpperCase().replace(/^\$/, "");
    if (TOKENS[up]) out.add(up);
  }
  return [...out];
}

function normalizeNarratives(arr) {
  const valid = new Set(NARRATIVES.map((n) => n.toLowerCase()));
  const out = new Set();
  for (const n of arr || []) {
    const key = String(n).trim();
    const match = NARRATIVES.find((v) => v.toLowerCase() === key.toLowerCase());
    if (match) out.add(match);
  }
  return [...out];
}

// ── Rules-based extractor (fallback / validation baseline) ───────────────────
export function extractRules(article) {
  const text = `${article.title}. ${article.summary}`.toLowerCase();

  const tokens = new Set();
  // Word-boundary ticker matches (e.g. " BTC ") and alias matches.
  for (const [alias, tic] of ALIAS_MAP) {
    if (alias.length <= 4) {
      const re = new RegExp(`(^|[^a-z0-9])${alias.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}([^a-z0-9]|$)`, "i");
      if (re.test(text)) tokens.add(tic);
    } else if (text.includes(alias)) {
      tokens.add(tic);
    }
  }

  let pos = 0;
  let neg = 0;
  for (const w of POS_WORDS) if (text.includes(w)) pos++;
  for (const w of NEG_WORDS) if (text.includes(w)) neg++;
  const sentiment = pos + neg === 0 ? 0 : clamp((pos - neg) / (pos + neg), -1, 1);

  const narratives = [];
  for (const [narr, kws] of Object.entries(NARRATIVE_KEYWORDS)) {
    if (kws.some((k) => text.includes(k))) narratives.push(narr);
  }

  let event = null;
  for (const [type, kws] of Object.entries(EVENT_KEYWORDS)) {
    if (kws.some((k) => text.includes(k))) {
      event = { type, token: [...tokens][0] || null, date: detectDate(text) };
      break;
    }
  }

  return {
    tokens: [...tokens],
    sentiment,
    narratives,
    event,
    confidence: tokens.size > 0 ? 0.55 : 0.3,
    model: "rules-v1"
  };
}

// Detect an explicit future-ish date like "June 20", "2026-06-20", "20 June".
function detectDate(text) {
  const iso = text.match(/\b(20\d{2})-(\d{2})-(\d{2})\b/);
  if (iso) return `${iso[1]}-${iso[2]}-${iso[3]}`;
  const months = ["january","february","march","april","may","june","july","august","september","october","november","december"];
  const md = text.match(/\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})\b/);
  if (md) {
    const mi = months.findIndex((m) => m.startsWith(md[1]));
    if (mi >= 0) {
      const y = new Date().getUTCFullYear();
      return `${y}-${String(mi + 1).padStart(2, "0")}-${String(md[2]).padStart(2, "0")}`;
    }
  }
  return null;
}

// ── Claude extractor (production path) ───────────────────────────────────────
const SYSTEM = `You are a crypto market data labeller. For the given news item, return STRICT JSON:
{"tokens":[TICKERS],"sentiment":-1..1,"narratives":[TAGS],"event":{"type":TYPE,"token":TICKER|null,"date":"YYYY-MM-DD"|null}|null}
Rules:
- tokens: only the crypto assets the item is actually ABOUT, as uppercase tickers. Empty array if none.
- sentiment: net sentiment toward those tokens, -1 (very bearish) to 1 (very bullish).
- narratives: subset of [${NARRATIVES.join(", ")}].
- event: a concrete, datable/notable event if present, type one of [${EVENT_TYPES.join(", ")}]; else null.
Output ONLY the JSON object, no prose.`;

export async function extractClaude(article, apiKey) {
  const model = process.env.EXTRACT_MODEL || "claude-haiku-4-5";
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01"
    },
    body: JSON.stringify({
      model,
      max_tokens: 300,
      system: SYSTEM,
      messages: [{ role: "user", content: `${article.title}\n\n${article.summary}` }]
    })
  });
  if (!res.ok) throw new Error(`anthropic ${res.status}`);
  const json = await res.json();
  const raw = json?.content?.[0]?.text || "";
  const match = raw.match(/\{[\s\S]*\}/);
  if (!match) throw new Error("no json");
  const parsed = JSON.parse(match[0]);

  const tokens = normalizeTokens(parsed.tokens);
  let event = null;
  if (parsed.event && EVENT_TYPES.includes(parsed.event.type)) {
    const evTok = parsed.event.token ? normalizeTokens([parsed.event.token])[0] || null : tokens[0] || null;
    event = { type: parsed.event.type, token: evTok, date: parsed.event.date || null };
  }
  return {
    tokens,
    sentiment: clamp(Number(parsed.sentiment) || 0, -1, 1),
    narratives: normalizeNarratives(parsed.narratives),
    event,
    confidence: 0.85,
    model
  };
}

// Dispatcher: Claude if a key is present, else rules. Never throws — degrades.
export async function extract(article) {
  const key = process.env.ANTHROPIC_API_KEY;
  if (key) {
    try {
      return await extractClaude(article, key);
    } catch {
      // fall through to deterministic path
    }
  }
  return extractRules(article);
}
