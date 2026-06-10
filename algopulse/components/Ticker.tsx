import { Coin, fmtUsd } from "@/lib/coingecko";

export default function Ticker({ coins }: { coins: Coin[] }) {
  return (
    <div className="ticker-wrap">
      <div className="ticker">
        {coins.map((c) => {
          const ch = c.price_change_percentage_24h ?? 0;
          const cls = ch > 0.05 ? "up" : ch < -0.05 ? "down" : "flat";
          return (
            <span className="tick" key={c.id}>
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={c.image} alt="" />
              <span className="sym">{c.symbol.toUpperCase()}</span>
              <span>{fmtUsd(c.current_price)}</span>
              <span className={cls}>
                {ch > 0 ? "+" : ""}
                {ch.toFixed(2)}%
              </span>
            </span>
          );
        })}
      </div>
    </div>
  );
}
