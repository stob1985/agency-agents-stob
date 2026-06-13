// Plans are the product packaging. The same data, gated three ways — this is
// how a single dataset becomes a tiered, recurring-revenue API business.
export const PLANS = {
  free: {
    name: "Free",
    priceUsd: 0,
    historyHours: 24, // can only query the last 24h of heat/events
    ratePerMin: 30,
    webhooks: false,
    csvExport: false,
    eventsAccess: true
  },
  pro: {
    name: "Pro",
    priceUsd: 199,
    historyHours: 24 * 90, // 90 days
    ratePerMin: 300,
    webhooks: true,
    csvExport: true,
    eventsAccess: true
  },
  enterprise: {
    name: "Enterprise",
    priceUsd: 999,
    historyHours: 24 * 365 * 5, // effectively full history
    ratePerMin: 3000,
    webhooks: true,
    csvExport: true,
    eventsAccess: true
  }
};

export function planFor(key) {
  return PLANS[key?.plan] || PLANS.free;
}

// Earliest timestamp this plan may query.
export function historyFloor(plan) {
  return new Date(Date.now() - plan.historyHours * 3600 * 1000).toISOString();
}
