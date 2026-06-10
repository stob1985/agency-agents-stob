import { FearGreed as FG } from "@/lib/coingecko";

function color(v: number): string {
  if (v <= 25) return "#f4536e";
  if (v <= 45) return "#f5a623";
  if (v <= 60) return "#8b94a7";
  return "#21c77d";
}

export default function FearGreed({ fg }: { fg: FG | null }) {
  if (!fg) {
    return <div className="fg-wrap"><span style={{ color: "var(--text-dim)", fontSize: 13 }}>Sentiment feed unavailable.</span></div>;
  }
  const c = color(fg.value);
  return (
    <div className="fg-wrap">
      <div className="fg-gauge" style={{ border: `4px solid ${c}`, color: c }}>
        {fg.value}
      </div>
      <div className="fg-meta">
        <div className="cls">{fg.classification}</div>
        <div className="desc">
          Crypto Fear &amp; Greed index aggregates volatility, momentum, social and dominance data into a
          0–100 sentiment score.
        </div>
      </div>
    </div>
  );
}
