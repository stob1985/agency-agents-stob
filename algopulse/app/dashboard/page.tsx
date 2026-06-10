import { getFearGreed, getMarkets, fmtBig } from "@/lib/coingecko";
import { computeSignals } from "@/lib/signals";
import { generateBrief } from "@/lib/brief";
import { getTier } from "@/lib/tiers";
import MarketTable from "@/components/MarketTable";
import SignalFeed from "@/components/SignalFeed";
import FearGreed from "@/components/FearGreed";

export const revalidate = 120;

export default async function Dashboard({
  searchParams
}: {
  searchParams: Promise<{ plan?: string }>;
}) {
  const { plan } = await searchParams;
  const tier = getTier(plan);

  let coins: Awaited<ReturnType<typeof getMarkets>> = [];
  let fg = null;
  try {
    [coins, fg] = await Promise.all([getMarkets(20), getFearGreed()]);
  } catch {
    // handled below
  }

  if (coins.length === 0) {
    return (
      <main className="container">
        <div className="dash-head">
          <h1>Dashboard</h1>
        </div>
        <div className="panel" style={{ padding: 28 }}>
          <p style={{ color: "var(--text-dim)", margin: 0 }}>
            Market data source is rate-limited right now — refresh in a minute. (The free CoinGecko tier
            allows a handful of requests per minute; set COINGECKO_API_KEY for production traffic.)
          </p>
        </div>
      </main>
    );
  }

  const signals = computeSignals(coins);
  const brief = await generateBrief({ coins, signals, fearGreed: fg });

  const totalMcap = coins.reduce((a, c) => a + c.market_cap, 0);
  const totalVol = coins.reduce((a, c) => a + c.total_volume, 0);
  const btc = coins.find((c) => c.id === "bitcoin");
  const btcDom = btc ? (btc.market_cap / totalMcap) * 100 : null;
  const buys = signals.filter((s) => s.direction === "BUY").length;
  const sells = signals.filter((s) => s.direction === "SELL").length;
  const avg24 =
    coins.reduce((a, c) => a + (c.price_change_percentage_24h ?? 0), 0) / coins.length;

  const signalLimit = tier.signalLimit === Infinity ? signals.length : tier.signalLimit;

  return (
    <main className="container">
      <div className="dash-head">
        <h1>Market Intelligence</h1>
        <span className="meta">
          <span className="plan-pill">{tier.name} plan</span>
          {"  ·  "}updated {new Date().toUTCString().slice(17, 25)} UTC · auto-refresh 2 min
        </span>
      </div>

      <div className="stat-row">
        <div className="stat">
          <div className="label">Top-20 market cap</div>
          <div className="value">{fmtBig(totalMcap)}</div>
          <div className={`delta ${avg24 >= 0 ? "up" : "down"}`}>
            {avg24 >= 0 ? "+" : ""}
            {avg24.toFixed(2)}% avg 24h
          </div>
        </div>
        <div className="stat">
          <div className="label">24h volume</div>
          <div className="value">{fmtBig(totalVol)}</div>
          <div className="delta flat">across top 20 assets</div>
        </div>
        <div className="stat">
          <div className="label">BTC dominance</div>
          <div className="value">{btcDom !== null ? btcDom.toFixed(1) + "%" : "—"}</div>
          <div className="delta flat">of tracked universe</div>
        </div>
        <div className="stat">
          <div className="label">Signal desk</div>
          <div className="value">
            <span className="up">{buys}▲</span> <span className="down">{sells}▼</span>
          </div>
          <div className="delta flat">{signals.length} assets scanned hourly</div>
        </div>
      </div>

      <div className="dash-grid">
        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
          <div className="panel">
            <div className="panel-head">
              <h2>Markets</h2>
              <span className="sub">7d hourly sparkline · CoinGecko</span>
            </div>
            <div style={{ overflowX: "auto" }}>
              <MarketTable coins={coins} />
            </div>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>
          <div className="panel">
            <div className="panel-head">
              <h2>Daily AI Brief</h2>
              <span className="sub">{brief.engine === "claude" ? "Claude research desk" : "rules engine"}</span>
            </div>
            <div className="brief-text">
              {brief.text}
              <span className="engine-tag">
                generated {new Date().toISOString().slice(0, 16).replace("T", " ")} UTC
              </span>
            </div>
          </div>

          <div className="panel">
            <div className="panel-head">
              <h2>Sentiment</h2>
              <span className="sub">alternative.me</span>
            </div>
            <FearGreed fg={fg} />
          </div>

          <div className="panel">
            <div className="panel-head">
              <h2>Signal Feed</h2>
              <span className="sub">hourly timeframe</span>
            </div>
            <SignalFeed signals={signals} limit={signalLimit} />
          </div>
        </div>
      </div>
    </main>
  );
}
