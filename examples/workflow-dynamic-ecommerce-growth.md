# Dynamic Workflow: Data-Driven E-Commerce Growth Engine

> A **dynamic** multi-agent workflow that doesn't follow a fixed script — it reads live
> signals from connected tools (Trendtruck, Shopify, Higgsfield, Meta Ads, Google Drive)
> and **re-routes itself** based on what the data says at each gate.

## What Makes It "Dynamic"

Unlike the linear examples in this folder (where step N always hands off to step N+1),
this workflow has **decision gates**. At each gate the active agent inspects real metrics
and chooses the next branch:

- A product that isn't trending **loops back** to research instead of moving to launch.
- A creative that the virality predictor scores low **regenerates** before any ad spend.
- An ad set below target ROAS **scales down or kills itself**; one above target **scales up**.

The workflow only advances when the data earns it.

## Connected Tools (live in this session)

| Tool (MCP) | Used for |
|------------|----------|
| **Trendtruck** | Find winning products, scan competitor ads, daily trend radar |
| **Shopify** | Create/update products, collections, inventory, run analytics |
| **Higgsfield** | Generate ad images/videos, predict virality before spend |
| **Meta Ads** | Build campaigns/ad sets/ads, pull insights, scale or pause |
| **Google Drive** | Archive briefs, creatives, and performance reports |

## Agent Team

| Agent | Role in this workflow |
|-------|----------------------|
| Product Trend Researcher | Source demand signals, validate the product |
| Cross-Border E-Commerce | Stand up the Shopify offer + pricing |
| Paid Media Creative Strategist | Brief and direct the creative |
| Paid Social Strategist | Structure and launch the Meta campaign |
| Paid Media Auditor | Read insights, decide scale / cut / iterate |
| Growth Hacker | Own the loop, set the thresholds, call the pivots |

---

## The Workflow

```
                        ┌─────────────────────────────┐
                        │  GATE 0: Trend Radar (daily) │
                        └──────────────┬──────────────┘
                                       ▼
        ┌──────────────────────  GATE 1: Product Validation  ──────────────────────┐
        │ trending?  ── no ──▶ loop back to research / pick next product            │
        │     │ yes                                                                  │
        ▼     ▼                                                                      │
   GATE 2: Offer Live on Shopify                                                     │
        │                                                                            │
        ▼                                                                            │
   GATE 3: Creative + Virality Score ── score < 7 ──▶ regenerate (back to GATE 3)    │
        │ score ≥ 7                                                                  │
        ▼                                                                            │
   GATE 4: Launch Meta Campaign (small budget)                                       │
        │                                                                            │
        ▼                                                                            │
   GATE 5: 72h Performance Read ──┬── ROAS < 1.0 ──▶ KILL, return to GATE 1 ─────────┘
                                  ├── 1.0 ≤ ROAS < target ──▶ iterate creative (GATE 3)
                                  └── ROAS ≥ target ──▶ SCALE (duplicate + raise budget)
```

### GATE 0 — Daily Trend Radar (the dynamic trigger)

Run this on a schedule. It's what makes the workflow start itself.

```
Activate Product Trend Researcher.

Pull today's trend radar and surface 3-5 candidate products with rising demand.
Use Trendtruck: daily_radar, find_winning_products, and search_ads to confirm
competitors are actively spending behind each candidate.

For each candidate output:
1. Product + angle
2. Evidence of demand (trend direction, ad volume, advertiser count)
3. A 0-10 "go" score

Only candidates scoring ≥ 7 pass to GATE 1.
```

**Dynamic rule:** No candidate ≥ 7 → stop. Don't force a launch on a flat market.

### GATE 1 — Product Validation

```
Activate Product Trend Researcher.

Take the top candidate from the radar: [paste].
Deep-dive with Trendtruck: brief_competitor on the top 2 advertisers,
scan_ad on their best-performing creative, and find_similar_shops.

Decide:
- Is the demand durable or a 1-week spike?
- What angle is under-served?

Return GO (advance to GATE 2) or NO-GO (loop back to GATE 0, next candidate).
```

### GATE 2 — Stand Up the Offer (Shopify)

```
Activate Cross-Border E-Commerce.

Validated product + winning angle: [paste].
Using Shopify: create-product with the chosen angle in title/description,
set pricing for target margin, add it to a campaign collection, and set inventory.

Return the product URL and the exact margin math — the ad budget at GATE 4
will be sized from this.
```

### GATE 3 — Creative + Virality Gate (Higgsfield)

```
Activate Paid Media Creative Strategist.

Product page: [paste]. Under-served angle: [paste].
Brief and generate 3 creative variants with Higgsfield (generate_image /
generate_video). Then run virality_predictor on each.

Dynamic rule:
- Any variant scoring ≥ 7 → it advances to GATE 4.
- All variants < 7 → regenerate with a sharper hook (stay at GATE 3).
- Never spend on a sub-7 creative.

Archive the winning creative + brief to Google Drive (create_file).
```

### GATE 4 — Launch (Meta Ads, small budget)

```
Activate Paid Social Strategist.

Winning creative(s): [paste]. Target margin from GATE 2: [paste].
Build in Meta Ads:
- create_campaign (objective: sales/conversions)
- create_adset sized to ~2-3x product cost/day as the test budget
- bulk_upload_ad_videos / upload_ad_image, then create_ad_creative + create_ad
- Use search_interests / estimate_audience_size to set targeting

Launch and report the campaign/ad set IDs. Set a 72h read checkpoint at GATE 5.
```

### GATE 5 — Performance Read + Self-Routing (the core loop)

```
Activate Paid Media Auditor.

Pull get_insights for the ad set over the last 72h (spend, ROAS, CPA, CTR).
Cross-check against Shopify run-analytics-query for true orders/revenue.

Route based on ROAS vs. the target from GATE 2:
- ROAS ≥ target  → SCALE: duplicate_adset + bulk_update_adsets to raise budget,
                   broaden audience. Stay in the loop, re-read in 72h.
- 1.0 ≤ ROAS < target → ITERATE: back to GATE 3 for a fresh creative angle,
                   keep the proven audience.
- ROAS < 1.0    → KILL: bulk_update_ads to pause, return to GATE 1 / next product.

Write a one-page decision log to Google Drive every cycle.
```

---

## Wiring It as a Recurring Job

The "daily radar → validate → launch → optimize" loop is meant to run unattended.
Two options:

- **Manual:** run GATE 0 each morning, follow the branches the data picks.
- **Automated:** schedule GATE 0 (e.g. `/loop 24h` or a cron-style trigger) so the
  workflow wakes itself, and let GATE 5's 72h checkpoints re-enter the loop.

## Key Patterns

1. **Data gates, not fixed steps** — every advance is conditional on a live metric.
2. **Feedback loops** — losing creatives and products route *backward*, not forward.
3. **Spend protection** — virality + ROAS thresholds gate money out of bad creatives.
4. **Single source of truth** — Shopify analytics reconciles Meta's reported numbers.
5. **Durable memory** — Google Drive holds every brief, creative, and decision log so
   the next cycle starts smarter than the last.

## Tips

- Set the ROAS target once at GATE 2 from real margin — every downstream branch reads it.
- Keep the GATE 5 cadence tight (72h) early, then widen it as a winner stabilizes.
- Paste full agent outputs between gates — the agents don't share memory.
- When in doubt, the dynamic default is **back, not forward**: re-validate before you scale.
