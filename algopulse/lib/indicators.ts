/** Technical indicators computed over a price series (oldest → newest). */

export function sma(values: number[], period: number): number | null {
  if (values.length < period) return null;
  const slice = values.slice(-period);
  return slice.reduce((a, b) => a + b, 0) / period;
}

export function ema(values: number[], period: number): number | null {
  if (values.length < period) return null;
  const k = 2 / (period + 1);
  let e = values.slice(0, period).reduce((a, b) => a + b, 0) / period;
  for (let i = period; i < values.length; i++) {
    e = values[i] * k + e * (1 - k);
  }
  return e;
}

/** Wilder's RSI. */
export function rsi(values: number[], period = 14): number | null {
  if (values.length < period + 1) return null;
  let gain = 0;
  let loss = 0;
  for (let i = 1; i <= period; i++) {
    const diff = values[i] - values[i - 1];
    if (diff >= 0) gain += diff;
    else loss -= diff;
  }
  let avgGain = gain / period;
  let avgLoss = loss / period;
  for (let i = period + 1; i < values.length; i++) {
    const diff = values[i] - values[i - 1];
    avgGain = (avgGain * (period - 1) + Math.max(diff, 0)) / period;
    avgLoss = (avgLoss * (period - 1) + Math.max(-diff, 0)) / period;
  }
  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - 100 / (1 + rs);
}

export interface Macd {
  macd: number;
  signal: number;
  histogram: number;
}

export function macd(values: number[]): Macd | null {
  if (values.length < 35) return null;
  const fastK = 2 / 13;
  const slowK = 2 / 27;
  const sigK = 2 / 10;
  let fast = values.slice(0, 12).reduce((a, b) => a + b, 0) / 12;
  let slow = values.slice(0, 26).reduce((a, b) => a + b, 0) / 26;
  const macdSeries: number[] = [];
  for (let i = 12; i < values.length; i++) {
    fast = values[i] * fastK + fast * (1 - fastK);
    if (i >= 26) {
      slow = values[i] * slowK + slow * (1 - slowK);
      macdSeries.push(fast - slow);
    }
  }
  if (macdSeries.length < 9) return null;
  let sig = macdSeries.slice(0, 9).reduce((a, b) => a + b, 0) / 9;
  for (let i = 9; i < macdSeries.length; i++) {
    sig = macdSeries[i] * sigK + sig * (1 - sigK);
  }
  const m = macdSeries[macdSeries.length - 1];
  return { macd: m, signal: sig, histogram: m - sig };
}

/** Detects whether the short SMA crossed the long SMA within the last `lookback` bars. */
export function smaCross(
  values: number[],
  short: number,
  long: number,
  lookback = 6
): "golden" | "death" | null {
  if (values.length < long + lookback) return null;
  for (let back = 0; back < lookback; back++) {
    const now = values.slice(0, values.length - back);
    const prev = values.slice(0, values.length - back - 1);
    const sNow = sma(now, short);
    const lNow = sma(now, long);
    const sPrev = sma(prev, short);
    const lPrev = sma(prev, long);
    if (sNow === null || lNow === null || sPrev === null || lPrev === null) continue;
    if (sPrev <= lPrev && sNow > lNow) return "golden";
    if (sPrev >= lPrev && sNow < lNow) return "death";
  }
  return null;
}
