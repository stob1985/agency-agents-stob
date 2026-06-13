import { db, nowIso, hourBucket } from "./db.js";
import { fetchAllFeeds } from "./sources.js";
import { extract } from "./extract.js";
import { SOURCE_TIER } from "./taxonomy.js";
import { createHash } from "node:crypto";

// The pipeline: fetch feeds -> dedupe articles -> label each (agent) ->
// fan out into the two sellable products (heat time-series + event feed).

const insArticle = db.prepare(
  `INSERT OR IGNORE INTO articles (source,url,title,summary,published_at,fetched_at,hash)
   VALUES (?,?,?,?,?,?,?)`
);
const getArticleByHash = db.prepare(`SELECT id FROM articles WHERE hash = ?`);
const hasLabel = db.prepare(`SELECT article_id FROM labels WHERE article_id = ?`);
const insLabel = db.prepare(
  `INSERT OR REPLACE INTO labels (article_id,tokens,sentiment,narratives,confidence,model)
   VALUES (?,?,?,?,?,?)`
);
const upsertHeat = db.prepare(`
  INSERT INTO heat (bucket_ts,token,narrative,mentions,raw_mentions,avg_sentiment)
  VALUES (@bucket,@token,@narrative,@mentions,1,@sentiment)
  ON CONFLICT(bucket_ts,token,narrative) DO UPDATE SET
    avg_sentiment = (avg_sentiment*raw_mentions + @sentiment) / (raw_mentions+1),
    mentions = mentions + @mentions,
    raw_mentions = raw_mentions + 1
`);
const insEvent = db.prepare(
  `INSERT OR IGNORE INTO events (article_id,token,event_type,event_date,title,url,source,confidence,detected_at,hash)
   VALUES (?,?,?,?,?,?,?,?,?,?)`
);

function applyLabelToProducts(article, label) {
  const bucket = hourBucket(article.published_at);
  const weight = SOURCE_TIER[article.source] ?? 0.5;

  // Product A — heat: one row per token (narrative='') plus token×narrative rows.
  for (const token of label.tokens) {
    upsertHeat.run({ bucket, token, narrative: "", mentions: weight, sentiment: label.sentiment });
    for (const narr of label.narratives) {
      upsertHeat.run({ bucket, token, narrative: narr, mentions: weight, sentiment: label.sentiment });
    }
  }
  // Also track narrative-level heat even when no token is named (token='').
  if (label.tokens.length === 0) {
    for (const narr of label.narratives) {
      upsertHeat.run({ bucket, token: "", narrative: narr, mentions: weight, sentiment: label.sentiment });
    }
  }

  // Product B — events.
  if (label.event) {
    const evHash = createHash("sha1")
      .update(`${label.event.type}:${label.event.token}:${article.hash}`)
      .digest("hex");
    insEvent.run(
      article.id,
      label.event.token,
      label.event.type,
      label.event.date,
      article.title,
      article.url,
      article.source,
      label.confidence,
      nowIso(),
      evHash
    );
  }
}

export async function runIngest({ verbose = true } = {}) {
  const t0 = Date.now();
  const items = await fetchAllFeeds();
  if (verbose) console.log(`fetched ${items.length} items from feeds`);

  let newArticles = 0;
  let labelled = 0;

  for (const item of items) {
    const r = insArticle.run(
      item.source, item.url, item.title, item.summary,
      item.published_at, nowIso(), item.hash
    );
    const row = getArticleByHash.get(item.hash);
    if (!row) continue;
    const articleId = row.id;
    if (r.changes > 0) newArticles++;

    // Only label once per article (idempotent re-runs).
    if (hasLabel.get(articleId)) continue;

    const article = { ...item, id: articleId };
    const label = await extract(article);
    insLabel.run(
      articleId,
      JSON.stringify(label.tokens),
      label.sentiment,
      JSON.stringify(label.narratives),
      label.confidence,
      label.model
    );
    applyLabelToProducts(article, label);
    labelled++;
  }

  const dt = ((Date.now() - t0) / 1000).toFixed(1);
  if (verbose) {
    const model = process.env.ANTHROPIC_API_KEY ? "claude" : "rules";
    console.log(`ingest done in ${dt}s — ${newArticles} new articles, ${labelled} newly labelled (${model})`);
  }
  return { fetched: items.length, newArticles, labelled };
}

// Run directly: `npm run ingest`
if (import.meta.url === `file://${process.argv[1]}`) {
  runIngest().then(() => process.exit(0));
}
