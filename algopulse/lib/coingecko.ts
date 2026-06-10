const BASE = "https://api.coingecko.com/api/v3";

export interface Coin {
  id: string;
  symbol: string;
  name: string;
  image: string;
  current_price: number;
  market_cap: number;
  market_cap_rank: number;
  total_volume: number;
  price_change_percentage_24h: number | null;
  price_change_percentage_7d_in_currency: number | null;
  sparkline_in_7d: { price: number[] } | null;
}

function headers(): HeadersInit {
  const key = process.env.COINGECKO_API_KEY;
  return key ? { "x-cg-demo-api-key": key } : {};
}

/**
 * Top coins by market cap with 7d hourly sparkline (~168 points per coin).
 * One call feeds the ticker, the market table and the signal engine.
 */
export async function getMarkets(perPage = 20): Promise<Coin[]> {
  const url =
    `${BASE}/coins/markets?vs_currency=usd&order=market_cap_desc` +
    `&per_page=${perPage}&page=1&sparkline=true` +
    `&price_change_percentage=24h,7d`;
  const res = await fetch(url, { headers: headers(), next: { revalidate: 120 } });
  if (!res.ok) throw new Error(`CoinGecko ${res.status}`);
  return res.json();
}

export interface FearGreed {
  value: number;
  classification: string;
  timestamp: string;
}

export async function getFearGreed(): Promise<FearGreed | null> {
  try {
    const res = await fetch("https://api.alternative.me/fng/?limit=1", {
      next: { revalidate: 3600 }
    });
    if (!res.ok) return null;
    const json = await res.json();
    const d = json?.data?.[0];
    if (!d) return null;
    return {
      value: Number(d.value),
      classification: d.value_classification,
      timestamp: d.timestamp
    };
  } catch {
    return null;
  }
}

export function fmtUsd(n: number): string {
  if (n >= 1) {
    return n.toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: n >= 1000 ? 0 : 2
    });
  }
  return "$" + n.toPrecision(3);
}

export function fmtBig(n: number): string {
  if (n >= 1e12) return "$" + (n / 1e12).toFixed(2) + "T";
  if (n >= 1e9) return "$" + (n / 1e9).toFixed(1) + "B";
  if (n >= 1e6) return "$" + (n / 1e6).toFixed(1) + "M";
  return fmtUsd(n);
}
