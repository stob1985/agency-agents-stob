export type Plan = "free" | "pro" | "whale";

export interface Tier {
  id: Plan;
  name: string;
  priceUsd: number;
  tagline: string;
  features: string[];
  /** How many signal cards are unlocked on the dashboard. */
  signalLimit: number;
  /** Stripe price id env var — wire up in checkout. */
  stripePriceEnv?: string;
}

export const TIERS: Tier[] = [
  {
    id: "free",
    name: "Scout",
    priceUsd: 0,
    tagline: "Get a feel for the engine",
    features: [
      "Live market overview (top 20)",
      "3 unlocked signals per day",
      "Weekly AI market brief",
      "Fear & Greed gauge"
    ],
    signalLimit: 3
  },
  {
    id: "pro",
    name: "Pro",
    priceUsd: 29,
    tagline: "For active investors",
    features: [
      "All signals, refreshed hourly",
      "Daily personalized AI brief on your watchlist",
      "RSI / SMA-cross / MACD breakdown per asset",
      "Email + Telegram alerts",
      "Full signal history & accuracy stats"
    ],
    signalLimit: Infinity,
    stripePriceEnv: "STRIPE_PRICE_PRO"
  },
  {
    id: "whale",
    name: "Whale",
    priceUsd: 99,
    tagline: "Institutional-grade research",
    features: [
      "Everything in Pro",
      "On-demand AI deep-dive reports (10/month)",
      "Portfolio risk & correlation report",
      "On-chain whale-movement digests",
      "Priority data refresh & API access"
    ],
    signalLimit: Infinity,
    stripePriceEnv: "STRIPE_PRICE_WHALE"
  }
];

export function getTier(plan: string | undefined): Tier {
  return TIERS.find((t) => t.id === plan) ?? TIERS[0];
}
