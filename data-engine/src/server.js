import express from "express";
import { db, nowIso } from "./db.js";
import { PLANS, planFor, historyFloor } from "./plans.js";
import { NARRATIVES, EVENT_TYPES, TOKENS } from "./taxonomy.js";

const app = express();
app.use(express.json());

// ── Prepared statements ──────────────────────────────────────────────────────
const getKey = db.prepare(`SELECT * FROM api_keys WHERE key = ?`);
const touchKey = db.prepare(`UPDATE api_keys SET calls = calls + 1, last_seen = ? WHERE key = ?`);

// Simple in-memory rate limiter (per key, per minute).
const buckets = new Map();
function rateLimited(key, perMin) {
  const now = Date.now();
  const slot = Math.floor(now / 60000);
  const b = buckets.get(key);
  if (!b || b.slot !== slot) {
    buckets.set(key, { slot, count: 1 });
    return false;
  }
  b.count++;
  return b.count > perMin;
}

// ── Auth middleware ──────────────────────────────────────────────────────────
function auth(req, res, next) {
  const k = req.header("x-api-key") || req.query.api_key;
  if (!k) return res.status(401).json({ error: "missing API key", hint: "send X-API-Key header" });
  const row = getKey.get(k);
  if (!row) return res.status(403).json({ error: "invalid API key" });
  const plan = planFor(row);
  if (rateLimited(k, plan.ratePerMin)) {
    return res.status(429).json({ error: "rate limit exceeded", limit_per_min: plan.ratePerMin });
  }
  touchKey.run(nowIso(), k);
  req.apiKey = row;
  req.plan = plan;
  next();
}

// ── Product A: Narrative Heat Index ──────────────────────────────────────────

// Time-series of heat for a token and/or narrative.
app.get("/v1/heat", auth, (req, res) => {
  const token = (req.query.token || "").toUpperCase();
  const narrative = req.query.narrative || "";
  const floor = historyFloor(req.plan);
  const from = maxIso(req.query.from, floor);
  const to = req.query.to || nowIso();

  const rows = db
    .prepare(
      `SELECT bucket_ts, token, narrative, mentions, raw_mentions, avg_sentiment
       FROM heat
       WHERE bucket_ts >= ? AND bucket_ts <= ?
         AND (@token = '' OR token = @token)
         AND (@narrative = '' OR narrative = @narrative)
       ORDER BY bucket_ts ASC`
    )
    .all(from, to, { token, narrative });

  res.json({
    dataset: "narrative_heat_index",
    query: { token: token || null, narrative: narrative || null, from, to },
    plan: req.plan.name,
    points: rows.length,
    series: rows.map((r) => ({
      ts: r.bucket_ts,
      token: r.token || null,
      narrative: r.narrative || null,
      heat: round(r.mentions),
      mentions: r.raw_mentions,
      sentiment: round(r.avg_sentiment)
    }))
  });
});

// The money shot: what's hot right now. Ranked tokens + narratives over a window.
app.get("/v1/heat/top", auth, (req, res) => {
  const windowH = clampInt(req.query.window_hours, 1, req.plan.historyHours, 24);
  const since = maxIso(new Date(Date.now() - windowH * 3600 * 1000).toISOString(), historyFloor(req.plan));

  const tokens = db
    .prepare(
      `SELECT token, SUM(mentions) heat, SUM(raw_mentions) mentions,
              SUM(avg_sentiment*raw_mentions)/SUM(raw_mentions) sentiment
       FROM heat WHERE bucket_ts >= ? AND token != '' AND narrative = ''
       GROUP BY token ORDER BY heat DESC LIMIT 15`
    )
    .all(since);

  const narratives = db
    .prepare(
      `SELECT narrative, SUM(mentions) heat, SUM(raw_mentions) mentions,
              SUM(avg_sentiment*raw_mentions)/SUM(raw_mentions) sentiment
       FROM heat WHERE bucket_ts >= ? AND narrative != ''
       GROUP BY narrative ORDER BY heat DESC LIMIT 15`
    )
    .all(since);

  res.json({
    dataset: "narrative_heat_index/top",
    window_hours: windowH,
    since,
    top_tokens: tokens.map((r) => ({
      token: r.token, heat: round(r.heat), mentions: r.mentions, sentiment: round(r.sentiment)
    })),
    top_narratives: narratives.map((r) => ({
      narrative: r.narrative, heat: round(r.heat), mentions: r.mentions, sentiment: round(r.sentiment)
    }))
  });
});

// ── Product B: Token Event Feed ──────────────────────────────────────────────
app.get("/v1/events", auth, (req, res) => {
  if (!req.plan.eventsAccess) return res.status(402).json({ error: "events require a paid plan" });
  const type = req.query.type || "";
  const token = (req.query.token || "").toUpperCase();
  const floor = historyFloor(req.plan);
  const since = maxIso(req.query.since, floor);
  const limit = clampInt(req.query.limit, 1, 200, 50);

  const rows = db
    .prepare(
      `SELECT token, event_type, event_date, title, url, source, confidence, detected_at
       FROM events
       WHERE detected_at >= @since
         AND (@type = '' OR event_type = @type)
         AND (@token = '' OR token = @token)
       ORDER BY detected_at DESC LIMIT @limit`
    )
    .all({ since, type, token, limit });

  res.json({
    dataset: "token_event_feed",
    query: { type: type || null, token: token || null, since },
    count: rows.length,
    events: rows
  });
});

// ── Webhooks (pro+): register a URL to receive new events ────────────────────
app.post("/v1/webhooks", auth, (req, res) => {
  if (!req.plan.webhooks) return res.status(402).json({ error: "webhooks require Pro or Enterprise" });
  const { url, event_type = null, token = null } = req.body || {};
  if (!url || !/^https?:\/\//.test(url)) return res.status(400).json({ error: "valid url required" });
  if (event_type && !EVENT_TYPES.includes(event_type)) return res.status(400).json({ error: "unknown event_type" });
  const r = db
    .prepare(`INSERT INTO webhooks (key,url,event_type,token,created_at) VALUES (?,?,?,?,?)`)
    .run(req.apiKey.key, url, event_type, token ? String(token).toUpperCase() : null, nowIso());
  res.status(201).json({ id: r.lastInsertRowid, url, event_type, token });
});

// ── CSV export (pro+): bulk pull for offline/quant use ───────────────────────
app.get("/v1/export.csv", auth, (req, res) => {
  if (!req.plan.csvExport) return res.status(402).json({ error: "CSV export requires a paid plan" });
  const dataset = req.query.dataset === "events" ? "events" : "heat";
  const floor = historyFloor(req.plan);
  res.setHeader("content-type", "text/csv");
  res.setHeader("content-disposition", `attachment; filename="${dataset}.csv"`);

  if (dataset === "events") {
    const rows = db
      .prepare(`SELECT detected_at,token,event_type,event_date,source,confidence,title,url FROM events WHERE detected_at >= ? ORDER BY detected_at DESC`)
      .all(floor);
    res.write("detected_at,token,event_type,event_date,source,confidence,title,url\n");
    for (const r of rows) res.write(csvRow([r.detected_at, r.token, r.event_type, r.event_date, r.source, r.confidence, r.title, r.url]));
  } else {
    const rows = db
      .prepare(`SELECT bucket_ts,token,narrative,mentions,raw_mentions,avg_sentiment FROM heat WHERE bucket_ts >= ? ORDER BY bucket_ts DESC`)
      .all(floor);
    res.write("bucket_ts,token,narrative,heat,mentions,sentiment\n");
    for (const r of rows) res.write(csvRow([r.bucket_ts, r.token, r.narrative, round(r.mentions), r.raw_mentions, round(r.avg_sentiment)]));
  }
  res.end();
});

// ── Usage / meta ─────────────────────────────────────────────────────────────
app.get("/v1/usage", auth, (req, res) => {
  res.json({
    plan: req.plan.name,
    calls: req.apiKey.calls,
    limits: { history_hours: req.plan.historyHours, rate_per_min: req.plan.ratePerMin, webhooks: req.plan.webhooks }
  });
});

app.get("/v1/meta", (_req, res) => {
  res.json({ tokens: Object.keys(TOKENS), narratives: NARRATIVES, event_types: EVENT_TYPES });
});

app.get("/health", (_req, res) => res.json({ ok: true }));

// ── Landing / docs ───────────────────────────────────────────────────────────
app.get("/", (_req, res) => {
  const stats = db.prepare(`SELECT
    (SELECT COUNT(*) FROM articles) articles,
    (SELECT COUNT(*) FROM labels) labels,
    (SELECT COUNT(*) FROM events) events,
    (SELECT COUNT(DISTINCT token) FROM heat WHERE token != '') tokens`).get();
  res.type("html").send(docsHtml(stats));
});

// ── helpers ──────────────────────────────────────────────────────────────────
function round(n) { return Math.round(Number(n) * 1000) / 1000; }
function clampInt(v, lo, hi, dflt) {
  const n = parseInt(v, 10);
  return isNaN(n) ? dflt : Math.max(lo, Math.min(hi, n));
}
function maxIso(a, b) {
  if (!a) return b;
  return a > b ? a : b;
}
function csvRow(cols) {
  return cols.map((c) => {
    const s = c === null || c === undefined ? "" : String(c);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  }).join(",") + "\n";
}

function docsHtml(stats) {
  return `<!doctype html><html><head><meta charset="utf-8"><title>Narrative Data Engine API</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font:15px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;background:#0a0c12;color:#e6e9f0;margin:0}
.wrap{max-width:860px;margin:0 auto;padding:48px 24px}
h1{font-size:30px;margin:0 0 6px} .sub{color:#8b94a7;margin:0 0 28px}
.grad{background:linear-gradient(135deg,#4f7cff,#7c5cff);-webkit-background-clip:text;background-clip:text;color:transparent}
.stats{display:flex;gap:14px;flex-wrap:wrap;margin:0 0 34px}
.stat{background:#11151e;border:1px solid #1c2330;border-radius:10px;padding:12px 18px}
.stat b{font-size:22px;display:block;font-family:ui-monospace,monospace} .stat span{color:#8b94a7;font-size:12px}
.ep{background:#11151e;border:1px solid #1c2330;border-radius:10px;padding:14px 18px;margin:0 0 12px}
.ep code{font-family:ui-monospace,monospace;color:#7fd1ff} .m{color:#21c77d;font-weight:700}
.ep p{margin:6px 0 0;color:#8b94a7;font-size:13.5px}
.tier{display:inline-block;font-size:11px;color:#f5a623;border:1px solid #3a2f17;border-radius:6px;padding:1px 7px;margin-left:6px}
h2{font-size:16px;margin:28px 0 12px;color:#cdd3df}
pre{background:#11151e;border:1px solid #1c2330;border-radius:10px;padding:14px;overflow:auto;font-size:12.5px}
table{border-collapse:collapse;width:100%;font-size:13px} td,th{border:1px solid #1c2330;padding:7px 10px;text-align:left}
</style></head><body><div class="wrap">
<h1>Narrative <span class="grad">Data Engine</span></h1>
<p class="sub">Agent-labelled crypto intelligence, sold as an API. Two products, one pipeline.</p>
<div class="stats">
<div class="stat"><b>${stats.articles}</b><span>articles ingested</span></div>
<div class="stat"><b>${stats.labels}</b><span>agent labels</span></div>
<div class="stat"><b>${stats.tokens}</b><span>tokens tracked</span></div>
<div class="stat"><b>${stats.events}</b><span>events detected</span></div>
</div>
<h2>Product A — Narrative Heat Index</h2>
<div class="ep"><span class="m">GET</span> <code>/v1/heat/top?window_hours=24</code><p>Ranked hottest tokens &amp; narratives right now — the headline endpoint.</p></div>
<div class="ep"><span class="m">GET</span> <code>/v1/heat?token=BTC&amp;narrative=ETF&amp;from=&amp;to=</code><p>Hourly heat + sentiment time-series for a token and/or narrative.</p></div>
<h2>Product B — Token Event Feed</h2>
<div class="ep"><span class="m">GET</span> <code>/v1/events?type=unlock&amp;token=ARB&amp;limit=50</code><p>Structured, sourced events: listings, unlocks, mainnets, hacks, ETF filings…</p></div>
<div class="ep"><span class="m">POST</span> <code>/v1/webhooks</code> <span class="tier">PRO</span><p>Register a URL to receive new matching events. Body: {url,event_type?,token?}.</p></div>
<h2>Bulk &amp; meta</h2>
<div class="ep"><span class="m">GET</span> <code>/v1/export.csv?dataset=heat|events</code> <span class="tier">PRO</span><p>Bulk CSV pull for quant/offline use.</p></div>
<div class="ep"><span class="m">GET</span> <code>/v1/meta</code> · <code>/v1/usage</code><p>Taxonomy (tokens/narratives/event types) and your key usage.</p></div>
<h2>Auth &amp; plans</h2>
<p class="sub">Send <code>X-API-Key</code> on every call. Plans gate history depth, rate and bulk/webhook access.</p>
<table><tr><th>Plan</th><th>Price/mo</th><th>History</th><th>Rate</th><th>Webhooks</th><th>CSV</th></tr>
${Object.values(PLANS).map(p=>`<tr><td>${p.name}</td><td>$${p.priceUsd}</td><td>${Math.round(p.historyHours/24)}d</td><td>${p.ratePerMin}/min</td><td>${p.webhooks?"✓":"—"}</td><td>${p.csvExport?"✓":"—"}</td></tr>`).join("")}
</table>
<pre>curl -H "X-API-Key: pk_demo_pro" http://localhost:${process.env.PORT||8787}/v1/heat/top</pre>
</div></body></html>`;
}

const PORT = process.env.PORT || 8787;
app.listen(PORT, () => console.log(`Narrative Data Engine API on http://localhost:${PORT}`));
