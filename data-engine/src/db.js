import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DB_PATH = process.env.DB_PATH || join(__dirname, "..", "data.db");

export const db = new DatabaseSync(DB_PATH);

db.exec(`
PRAGMA journal_mode = WAL;

-- Raw ingested articles, deduped by content hash.
CREATE TABLE IF NOT EXISTS articles (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  source      TEXT NOT NULL,
  url         TEXT NOT NULL,
  title       TEXT NOT NULL,
  summary     TEXT,
  published_at TEXT NOT NULL,      -- ISO8601 UTC
  fetched_at  TEXT NOT NULL,
  hash        TEXT NOT NULL UNIQUE
);

-- One extraction record per article (the agent/LLM output, normalized).
CREATE TABLE IF NOT EXISTS labels (
  article_id  INTEGER PRIMARY KEY REFERENCES articles(id),
  tokens      TEXT NOT NULL,       -- json array of tickers
  sentiment   REAL NOT NULL,       -- -1..1
  narratives  TEXT NOT NULL,       -- json array
  confidence  REAL NOT NULL,
  model       TEXT NOT NULL        -- 'claude-haiku-4-5' | 'rules-v1'
);

-- Per-token, per-hour materialized mentions (Product A: Narrative Heat Index).
CREATE TABLE IF NOT EXISTS heat (
  bucket_ts   TEXT NOT NULL,       -- ISO hour bucket
  token       TEXT NOT NULL,
  narrative   TEXT NOT NULL,       -- '' for token-only rows
  mentions    REAL NOT NULL,       -- tier-weighted
  raw_mentions INTEGER NOT NULL,
  avg_sentiment REAL NOT NULL,
  PRIMARY KEY (bucket_ts, token, narrative)
);

-- Concrete events (Product B: Token Event Feed).
CREATE TABLE IF NOT EXISTS events (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  article_id  INTEGER REFERENCES articles(id),
  token       TEXT,
  event_type  TEXT NOT NULL,
  event_date  TEXT,                -- ISO date if a future/specific date detected
  title       TEXT NOT NULL,
  url         TEXT NOT NULL,
  source      TEXT NOT NULL,
  confidence  REAL NOT NULL,
  detected_at TEXT NOT NULL,
  hash        TEXT NOT NULL UNIQUE
);

-- API keys = the billing boundary. plan gates history depth + endpoints.
CREATE TABLE IF NOT EXISTS api_keys (
  key         TEXT PRIMARY KEY,
  label       TEXT,
  plan        TEXT NOT NULL DEFAULT 'free',  -- free | pro | enterprise
  created_at  TEXT NOT NULL,
  calls       INTEGER NOT NULL DEFAULT 0,
  last_seen   TEXT
);

-- Webhook subscriptions for the event feed (pro+).
CREATE TABLE IF NOT EXISTS webhooks (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  key         TEXT NOT NULL REFERENCES api_keys(key),
  url         TEXT NOT NULL,
  event_type  TEXT,                -- null = all types
  token       TEXT,                -- null = all tokens
  created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_heat_token ON heat(token, bucket_ts);
CREATE INDEX IF NOT EXISTS idx_events_token ON events(token, detected_at);
CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type, detected_at);
`);

export function nowIso() {
  return new Date().toISOString();
}

// Floor an ISO timestamp to its hour bucket.
export function hourBucket(iso) {
  const d = new Date(iso);
  d.setUTCMinutes(0, 0, 0);
  return d.toISOString();
}
