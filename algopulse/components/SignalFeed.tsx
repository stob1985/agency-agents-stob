import Link from "next/link";
import { Signal } from "@/lib/signals";
import { fmtUsd } from "@/lib/coingecko";

function SignalRow({ s }: { s: Signal }) {
  return (
    <div className="sig">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={s.image} alt="" />
      <div className="body">
        <div className="row1">
          <span className="nm">
            {s.name} <span style={{ color: "var(--text-dim)", fontWeight: 500 }}>{s.symbol}</span>
          </span>
          <span className={`sig-badge ${s.direction}`}>{s.direction}</span>
          <span className="conf">
            {s.confidence}% conf · {fmtUsd(s.price)}
            {s.rsi14 !== null ? ` · RSI ${s.rsi14.toFixed(0)}` : ""}
          </span>
        </div>
        <div className="reason">{s.reasons.join(" · ")}</div>
      </div>
    </div>
  );
}

export default function SignalFeed({
  signals,
  limit
}: {
  signals: Signal[];
  limit: number;
}) {
  const visible = signals.slice(0, limit);
  const locked = signals.slice(limit);

  return (
    <div className="sig-list">
      {visible.map((s) => (
        <SignalRow key={s.coinId} s={s} />
      ))}
      {locked.length > 0 && (
        <div className="locked">
          {locked.slice(0, 3).map((s) => (
            <SignalRow key={s.coinId} s={s} />
          ))}
          <div className="lock-overlay">
            <strong>{locked.length} more signals on Pro</strong>
            <span>
              Unlock the full hourly signal feed, watchlist alerts and the daily AI brief tailored to your
              portfolio.
            </span>
            <Link href="/dashboard?plan=pro" className="btn btn-primary">
              Preview Pro view
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
