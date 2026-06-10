import { Coin, fmtBig, fmtUsd } from "@/lib/coingecko";
import Sparkline from "./Sparkline";
import WatchButton from "./WatchButton";

function Pct({ v }: { v: number | null }) {
  if (v === null || v === undefined) return <span className="flat">—</span>;
  const cls = v > 0.05 ? "up" : v < -0.05 ? "down" : "flat";
  return (
    <span className={cls}>
      {v > 0 ? "+" : ""}
      {v.toFixed(2)}%
    </span>
  );
}

export default function MarketTable({ coins }: { coins: Coin[] }) {
  return (
    <table className="mkt">
      <thead>
        <tr>
          <th>Asset</th>
          <th>Price</th>
          <th>24h</th>
          <th>7d</th>
          <th>Market cap</th>
          <th>Last 7 days</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {coins.map((c) => (
          <tr key={c.id}>
            <td>
              <span className="coin-cell">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={c.image} alt="" />
                <span>
                  <span className="nm">{c.name}</span>{" "}
                  <span className="sy">{c.symbol.toUpperCase()}</span>
                </span>
              </span>
            </td>
            <td>{fmtUsd(c.current_price)}</td>
            <td>
              <Pct v={c.price_change_percentage_24h} />
            </td>
            <td>
              <Pct v={c.price_change_percentage_7d_in_currency} />
            </td>
            <td>{fmtBig(c.market_cap)}</td>
            <td>{c.sparkline_in_7d ? <Sparkline data={c.sparkline_in_7d.price} /> : null}</td>
            <td>
              <WatchButton coinId={c.id} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
