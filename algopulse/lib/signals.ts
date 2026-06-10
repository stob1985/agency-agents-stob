import { Coin } from "./coingecko";
import { rsi, sma, macd, smaCross } from "./indicators";

export type Direction = "BUY" | "SELL" | "NEUTRAL";

export interface Signal {
  coinId: string;
  symbol: string;
  name: string;
  image: string;
  price: number;
  direction: Direction;
  /** 0–100 */
  confidence: number;
  rsi14: number | null;
  trend: "up" | "down" | "flat";
  reasons: string[];
}

/**
 * Rule-based signal engine over the 7d hourly series CoinGecko ships with
 * each market row. Hourly bars → RSI(14)/SMA(20,50)/MACD on hourly timeframe.
 */
export function computeSignal(coin: Coin): Signal | null {
  const series = coin.sparkline_in_7d?.price;
  if (!series || series.length < 60) return null;

  const r = rsi(series, 14);
  const s20 = sma(series, 20);
  const s50 = sma(series, 50);
  const m = macd(series);
  const cross = smaCross(series, 20, 50, 6);
  const last = series[series.length - 1];
  const ch24 = coin.price_change_percentage_24h ?? 0;
  const ch7d = coin.price_change_percentage_7d_in_currency ?? 0;

  let score = 0;
  const reasons: string[] = [];

  if (r !== null) {
    if (r <= 30) {
      score += 2;
      reasons.push(`RSI(14) at ${r.toFixed(0)} — oversold on the hourly timeframe`);
    } else if (r >= 70) {
      score -= 2;
      reasons.push(`RSI(14) at ${r.toFixed(0)} — overbought on the hourly timeframe`);
    }
  }

  if (cross === "golden") {
    score += 2;
    reasons.push("SMA20 crossed above SMA50 within the last 6 hours (golden cross)");
  } else if (cross === "death") {
    score -= 2;
    reasons.push("SMA20 crossed below SMA50 within the last 6 hours (death cross)");
  } else if (s20 !== null && s50 !== null) {
    if (s20 > s50) {
      score += 1;
      reasons.push("Short-term trend above long-term trend (SMA20 > SMA50)");
    } else if (s20 < s50) {
      score -= 1;
      reasons.push("Short-term trend below long-term trend (SMA20 < SMA50)");
    }
  }

  if (m !== null) {
    const rel = m.histogram / last;
    if (rel > 0.0005) {
      score += 1;
      reasons.push("MACD histogram positive — momentum building");
    } else if (rel < -0.0005) {
      score -= 1;
      reasons.push("MACD histogram negative — momentum fading");
    }
  }

  if (ch24 <= -8) {
    score += 1;
    reasons.push(`Down ${ch24.toFixed(1)}% in 24h — mean-reversion setup`);
  } else if (ch24 >= 10) {
    score -= 1;
    reasons.push(`Up ${ch24.toFixed(1)}% in 24h — extended move, chase risk`);
  }

  const direction: Direction = score >= 2 ? "BUY" : score <= -2 ? "SELL" : "NEUTRAL";
  const confidence = Math.min(95, 40 + Math.abs(score) * 12);
  const trend: Signal["trend"] = ch7d > 1.5 ? "up" : ch7d < -1.5 ? "down" : "flat";

  if (reasons.length === 0) {
    reasons.push("No strong technical setup — ranging conditions");
  }

  return {
    coinId: coin.id,
    symbol: coin.symbol.toUpperCase(),
    name: coin.name,
    image: coin.image,
    price: coin.current_price,
    direction,
    confidence,
    rsi14: r,
    trend,
    reasons
  };
}

export function computeSignals(coins: Coin[]): Signal[] {
  return coins
    .map(computeSignal)
    .filter((s): s is Signal => s !== null)
    .sort((a, b) => {
      const w = (s: Signal) => (s.direction === "NEUTRAL" ? 0 : s.confidence);
      return w(b) - w(a);
    });
}
