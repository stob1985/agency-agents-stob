import Link from "next/link";
import Ticker from "@/components/Ticker";
import { getMarkets } from "@/lib/coingecko";
import { TIERS } from "@/lib/tiers";

export const revalidate = 120;

export default async function Landing() {
  let coins: Awaited<ReturnType<typeof getMarkets>> = [];
  try {
    coins = await getMarkets(15);
  } catch {
    // ticker degrades gracefully when the data source is rate-limited
  }

  return (
    <main>
      <section className="hero container">
        <div className="pill">
          <span className="dot" /> Signal engine live — refreshed hourly
        </div>
        <h1>
          Institutional-grade crypto research,
          <br />
          <span className="grad">run entirely by AI agents.</span>
        </h1>
        <p className="sub">
          AlgoPulse fuses live market data, on-chain feeds and a systematic signal engine with AI research
          briefs — delivered on your dashboard and inbox, tuned to your watchlist.
        </p>
        <div className="hero-cta">
          <Link href="/dashboard" className="btn btn-primary">
            Open live dashboard
          </Link>
          <Link href="#pricing" className="btn">
            See pricing
          </Link>
        </div>
      </section>

      {coins.length > 0 && <Ticker coins={coins} />}

      <section className="section container" id="features">
        <h2>One engine. Three layers of edge.</h2>
        <p className="lead">Every layer is an MCP-connected agent — data in, decisions out, no manual research desk.</p>
        <div className="grid3">
          <div className="card">
            <span className="icon">📡</span>
            <h3>Live multi-source data</h3>
            <p>
              Prices, volume and market structure for 15k+ assets via CoinGecko, exchange order-flow via CCXT,
              on-chain DEX liquidity via GeckoTerminal — streamed through MCP servers, not scraped PDFs.
            </p>
          </div>
          <div className="card">
            <span className="icon">⚡</span>
            <h3>Systematic signal engine</h3>
            <p>
              Hourly RSI, SMA-cross and MACD reads on every tracked asset, scored into BUY / SELL / NEUTRAL
              calls with explicit, auditable reasoning — no black box, every signal shows its work.
            </p>
          </div>
          <div className="card">
            <span className="icon">🧠</span>
            <h3>AI research briefs</h3>
            <p>
              A Claude-powered research desk turns the day&apos;s data into a four-part brief — Market Pulse,
              Standouts, Signal Desk, Risk Note — grounded strictly in sourced numbers.
            </p>
          </div>
        </div>
      </section>

      <section className="section container" id="pricing">
        <h2>Pricing</h2>
        <p className="lead">Start free. Upgrade when the signals pay for themselves.</p>
        <div className="grid3">
          {TIERS.map((t) => (
            <div key={t.id} className={`card price-card ${t.id === "pro" ? "featured" : ""}`}>
              {t.id === "pro" && <span className="badge">MOST POPULAR</span>}
              <h3>{t.name}</h3>
              <div className="price">
                ${t.priceUsd}
                <span>/mo</span>
              </div>
              <div className="tagline">{t.tagline}</div>
              <ul className="feat-list">
                {t.features.map((f) => (
                  <li key={f}>{f}</li>
                ))}
              </ul>
              <Link
                href={t.id === "free" ? "/dashboard" : `/dashboard?plan=${t.id}`}
                className={`btn ${t.id === "pro" ? "btn-primary" : ""}`}
                style={{ textAlign: "center" }}
              >
                {t.id === "free" ? "Start free" : `Preview ${t.name}`}
              </Link>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
