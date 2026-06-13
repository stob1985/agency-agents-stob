import { XMLParser } from "fast-xml-parser";
import { createHash } from "node:crypto";

// Public RSS feeds. We ingest and DERIVE structured data from them — we never
// redistribute the source articles, only our own labels/aggregations, which is
// what keeps the output a clean, sellable derived dataset.
export const FEEDS = [
  { source: "CoinDesk", url: "https://www.coindesk.com/arc/outboundfeeds/rss/" },
  { source: "Cointelegraph", url: "https://cointelegraph.com/rss" },
  { source: "The Defiant", url: "https://thedefiant.io/api/feed" },
  { source: "Decrypt", url: "https://decrypt.co/feed" },
  { source: "CryptoSlate", url: "https://cryptoslate.com/feed/" },
  { source: "Bitcoin Magazine", url: "https://bitcoinmagazine.com/feed" }
];

const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_" });

function stripHtml(s) {
  return String(s || "")
    .replace(/<[^>]*>/g, " ")
    .replace(/&[a-z]+;/gi, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function hashOf(title, url) {
  return createHash("sha1").update(`${title}::${url}`).digest("hex");
}

export async function fetchFeed(feed, { timeoutMs = 12000 } = {}) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(feed.url, {
      redirect: "follow",
      signal: ctrl.signal,
      headers: { "user-agent": "NarrativeDataEngine/0.1 (+research)" }
    });
    if (!res.ok) return [];
    const xml = await res.text();
    const doc = parser.parse(xml);
    const items = doc?.rss?.channel?.item || doc?.feed?.entry || [];
    const arr = Array.isArray(items) ? items : [items];
    return arr
      .map((it) => {
        const title = stripHtml(it.title?.["#text"] ?? it.title);
        let url = it.link?.["@_href"] ?? it.link ?? it.guid?.["#text"] ?? it.guid ?? "";
        if (typeof url === "object") url = url["#text"] || "";
        const summary = stripHtml(it.description ?? it.summary ?? it["content:encoded"] ?? "");
        const pub = it.pubDate ?? it.published ?? it.updated ?? new Date().toISOString();
        const publishedAt = new Date(pub);
        return {
          source: feed.source,
          title,
          url: String(url),
          summary: summary.slice(0, 600),
          published_at: isNaN(publishedAt) ? new Date().toISOString() : publishedAt.toISOString(),
          hash: hashOf(title, String(url))
        };
      })
      .filter((a) => a.title && a.url);
  } catch {
    return [];
  } finally {
    clearTimeout(t);
  }
}

export async function fetchAllFeeds() {
  const results = await Promise.all(FEEDS.map((f) => fetchFeed(f)));
  return results.flat();
}
