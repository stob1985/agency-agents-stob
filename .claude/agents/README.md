# Beauty Research Subagent Pack

Custom research subagents for **content-driven, high-margin beauty e-commerce**
product research. Dropped into `.claude/agents/`, so Claude Code activates them
automatically — no toggle needed. Describe a task and Claude routes to the right
agent, or invoke one by name ("use Meta Ads Beauty Winners to...").

## The 4 core agents (the named pack)

| Agent | What it does | Live data |
|-------|--------------|-----------|
| `amazon-beauty-winners.md` | Demand discovery — best-seller momentum, review velocity, price bands, ranked by the 4-criteria rubric | WebSearch/WebFetch (no native Amazon API); cross-checks TrendTrack |
| `tiktok-etsy-beauty-trends.md` | Early trend detection from TikTok culture + Etsy indie/giftable demand | WebSearch/WebFetch (no native TikTok/Etsy API); cross-checks TrendTrack ads |
| `meta-ads-beauty-winners.md` | Reverse-engineers Meta ads that are *scaling now* — hooks, angles, formats | **TrendTrack `search_ads` + Meta Ads connector (live)** |
| `margin-sourcing-reality.md` | Skeptical gatekeeper — COGS/margin/CAC, sourcing, compliance. Defaults to "NOT YET" | WebSearch + TrendTrack price signals |

### The shared 4-criteria rubric
Every product candidate is scored 1–5 on: **content-driven**, **high margin
(~70–85%)**, **easy distribution** (small/light/leak-proof), and
**differentiation** (sharp pain-point angle vs. generic white-label = death).

### Recommended workflow
1. **TikTok + Etsy Beauty Trends** → what's rising (timing).
2. **Amazon Beauty Winners** → confirm real demand + price bands.
3. **Meta Ads Beauty Winners** → proof it's monetizable + steal the hooks.
4. **Margin + Sourcing Reality** → final gate before you commit a hero product.

## Supporting agents (copied from this repo's catalog)
`product-trend-researcher`, `testing-reality-checker`, `supply-chain-strategist`,
`marketing-tiktok-strategist`, `marketing-instagram-curator`,
`marketing-content-creator`, `marketing-growth-hacker`,
`marketing-social-media-strategist`, `marketing-cross-border-ecommerce`,
`paid-media-creative-strategist`.

## ⚠️ Honest limits
- The 4 core agents are **custom-built here** (they were not in the repo catalog).
- **Live connectors:** TrendTrack (Shopify shops + Meta ads) and the Meta Ads
  connector give real/estimated signals. There is **no live Amazon or Etsy API** —
  those agents rely on web search and say so. TrendTrack reach/spend are modeled
  estimates, not billed figures.

## Adding more
Copy any `.md` from this repo's category folders (`marketing/`, `paid-media/`,
`specialized/`, etc.) into this directory — it's live on the next run.
