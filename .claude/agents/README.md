# Beauty E-Com Research Subagent Set

Curated subagents for a **content-driven, high-margin beauty e-commerce**
workflow (face/lip serum & lip oil niche). Dropped into `.claude/agents/`,
so Claude Code activates them automatically — no toggle needed.

Just describe a task and Claude routes to the matching agent, or invoke one
explicitly (e.g. "use the Trend Researcher to...").

## What's installed & why

| Agent | Use it for |
|-------|-----------|
| `product-trend-researcher.md` | Spotting emerging beauty trends, market sizing, competitive scans |
| `testing-reality-checker.md` | The "Margin + Sourcing Reality" gut check — defaults to skeptical, kills generic white-label ideas |
| `supply-chain-strategist.md` | Sourcing, COGS/margin math, logistics for small/light SKUs (lip oil) |
| `marketing-tiktok-strategist.md` | TikTok distribution — the main organic engine for this niche |
| `marketing-instagram-curator.md` | Reels / before-after / "shelfie" content |
| `marketing-content-creator.md` | Content engine: hooks, scripts, captions |
| `marketing-growth-hacker.md` | CAC-free organic growth loops |
| `marketing-social-media-strategist.md` | Cross-channel social plan |
| `marketing-cross-border-ecommerce.md` | Store ops, international shipping/positioning |
| `paid-media-creative-strategist.md` | Meta ad hooks & creative angles (glass skin / glow narratives) |

## Adding more

Copy any `.md` from this repo's category folders (e.g. `marketing/`,
`paid-media/`, `specialized/`) into this directory and it's live on next run.
