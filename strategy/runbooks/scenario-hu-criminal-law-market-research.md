# 🏛️ Runbook: HU Criminal Law Market Research

> **Mode**: NEXUS-Sprint | **Duration**: 1-2 days | **Agents**: 10

---

## Scenario

A 5-person Hungarian law firm currently specializing in traffic law (közlekedési jog) wants to expand into new criminal law niches where Google Ads competition is low and demand is growing. This runbook orchestrates a comprehensive market research sprint that identifies the most promising entry points, quantifies opportunity size, and produces a 90-day execution plan ready for immediate implementation.

**Business objective**: Identify 3–5 underserved Hungarian criminal law market niches where the firm can achieve ROI-positive Google Ads campaigns within 90 days of entry.

**Example output**: `strategy/playbooks/hu-criminal-law-market-analysis.md`

---

## Agent Roster

### Research Core (Phase 0 — Parallel)
| Agent | Role | Maps To |
|-------|------|---------|
| Trend Researcher | Criminal law trend analysis, crime statistics, regulatory changes | `product/product-trend-researcher.md` |
| Search Query Analyst | Google Ads keyword research, CPC benchmarks, competition index | `paid-media/paid-media-search-query-analyst.md` |
| Paid Media Auditor | Competitor mapping, white space identification, pricing landscape | `paid-media/paid-media-auditor.md` |
| Legal Compliance Checker | Btk. amendments, EU directive implementation, new legal obligations | `specialized/specialized-legal-compliance-checker.md` |
| UX Researcher | Underserved target group identification, persona development | `design/design-ux-researcher.md` |

### Strategy (Phase 1 — Parallel)
| Agent | Role | Maps To |
|-------|------|---------|
| Pipeline Analyst | Google Ads ROI modeling per niche, CAC/LTV calculations, pricing strategy | `sales/sales-pipeline-analyst.md` |
| PPC Campaign Strategist | Full campaign structures, ad copy variants, landing page briefs | `paid-media/paid-media-ppc-campaign-strategist.md` |
| SEO Specialist | Content strategy, pillar pages, local SEO, E-E-A-T authority building | `marketing/marketing-seo-specialist.md` |
| Outbound Strategist | Partnership identification, referral network design, media outreach | `sales/sales-outbound-strategist.md` |

### Synthesis (Phase 2 — Sequential)
| Agent | Role | Maps To |
|-------|------|---------|
| Project Shepherd | Compile all outputs → ranked niche list → 90-day execution plan | `project-management/project-management-project-shepherd.md` |

---

## Execution Plan

### Phase 0 — Intelligence (Day 1, all parallel)

```
PARALLEL — Launch all 5 simultaneously:

├── Trend Researcher
│   ├── Input: KSH crime statistics 2020–2024, ORFK annual reports, Legfőbb Ügyészség data
│   ├── Task: Identify top 10 growing criminal law areas in Hungary
│   ├── Output: trend-research-output.md
│   └── Required fields: area name | YoY growth % | estimated case volume | regulatory tailwind
│
├── Search Query Analyst
│   ├── Input: Keyword groups (cybercrime, economic crime, drug offenses, juveniles, foreigners)
│   ├── Task: HU market keyword analysis — volume, CPC, competition index
│   ├── Output: keyword-research-output.md
│   └── Required fields: keyword | monthly searches | CPC (HUF) | competition (1–10) | niche score
│
├── Paid Media Auditor
│   ├── Input: Search: "büntetőjogi ügyvéd Budapest", all niche keyword groups
│   ├── Task: Map all criminal law advertisers; identify white spaces (<5 advertisers)
│   ├── Output: competitor-map-output.md
│   └── Required fields: firm name | URL | Google Ads presence | SEO strength | areas covered | reviews
│
├── Legal Compliance Checker
│   ├── Input: Btk. amendments 2020–2025, NIS2, AMLD6, EU harmonization pipeline
│   ├── Task: Identify legal changes creating new criminal defense demand
│   ├── Output: legal-analysis-output.md
│   └── Required fields: change | description | expected case volume increase | timing | priority
│
└── UX Researcher
    ├── Input: KSH demographics, ORFK foreign nationals data, juvenile crime statistics
    ├── Task: Define 5+ underserved target segments with persona cards
    ├── Output: target-group-output.md
    └── Required fields: segment | size/year | acquisition channel | price sensitivity | Google Ads reachability
```

**Phase 0 Quality Gate**: All 5 outputs present, each with required fields populated. No output passes with "data unavailable" for more than 20% of required fields.

---

### Phase 1 — Strategy (Day 2 morning, all parallel)

```
PARALLEL — Launch all 4 simultaneously after Phase 0 completes:
Reference inputs: trend-research-output.md, keyword-research-output.md,
                  competitor-map-output.md, legal-analysis-output.md,
                  target-group-output.md

├── Pipeline Analyst
│   ├── Task: ROI model for top 5 identified niches
│   ├── Formula: CPC / conversion rate = CAC; (avg fee - CAC) / CAC = ROI%
│   ├── Output: roi-model-output.md
│   └── Required: CAC | avg fee | monthly volume | ROAS | niche ranking by ROI
│
├── PPC Campaign Strategist
│   ├── Task: Full Google Ads campaign structure for top 3 niches
│   ├── Per niche: campaign name | 3+ ad groups | keywords per group | match types
│   │             negative keyword list | ad copy (3 variants/group) | daily budget (HUF)
│   ├── Output: ads-strategy-output.md
│   └── Required: ready-to-implement campaign structure + landing page brief per niche
│
├── SEO Specialist
│   ├── Task: Organic content strategy to complement paid campaigns
│   ├── Deliverables: pillar page list | blog post calendar (12 months) | local SEO checklist
│   │               Google Business Profile optimization | E-E-A-T authority plan
│   ├── Output: seo-content-output.md
│   └── Required: priority content list with target keywords and estimated traffic
│
└── Outbound Strategist
    ├── Task: Referral network and partnership strategy
    ├── Segments: civil lawyers | accountants/auditors | insurers | HR directors | bank compliance
    ├── Output: partnership-strategy-output.md
    └── Required: partner type | market size | approach strategy | ethical constraints | 90-day actions
```

**Phase 1 Quality Gate**: All 4 outputs present. ROI model covers ≥3 niches. Campaign structure is implementation-ready (not conceptual). Partnership list includes ≥3 priority segments with actionable next steps.

---

### Phase 2 — Synthesis (Day 2 afternoon, sequential)

```
Project Shepherd — reads all 9 previous outputs and produces:

├── TOP 5 niche ranking table (score: search volume + low competition + ROI + legal tailwind + ease of entry)
├── #1 niche detailed plan:
│   ├── Target group description
│   ├── Google Ads structure (copy+paste ready)
│   ├── Landing page brief
│   ├── 90-day week-by-week execution calendar
│   └── Revenue forecast (pessimistic / realistic / optimistic)
├── Quick wins (implementable tomorrow):
│   ├── Google Ads account changes
│   ├── Landing page fixes
│   └── SEO immediate actions
├── Risk register:
│   ├── Hungarian Bar Association advertising rules
│   ├── GDPR in criminal law context
│   └── Capacity constraints
└── KPI dashboard (lead targets: 3mo / 6mo / 12mo; ROAS threshold; conversion rate targets)

Output: final-synthesis.md → copy to strategy/playbooks/hu-criminal-law-market-analysis.md
```

---

## Research Metrics

| Metric | Target | Owner |
|--------|--------|-------|
| Niches analyzed | ≥ 10 identified, ≥ 5 scored | Trend Researcher |
| Keywords in database | ≥ 50 relevant keywords | Search Query Analyst |
| Competitors documented | ≥ 10 firms with full profiles | Paid Media Auditor |
| Legal changes catalogued | ≥ 8 Btk./EU changes | Legal Compliance Checker |
| Target segments defined | ≥ 5 with persona cards | UX Researcher |
| Niches with ROI model | ≥ 5 | Pipeline Analyst |
| Campaign-ready structures | ≥ 3 niches | PPC Campaign Strategist |
| Content pieces planned | ≥ 24 (2/month for 12mo) | SEO Specialist |
| Partner categories mapped | ≥ 5 with approach plans | Outbound Strategist |
| Final niche ranking | Top 5 scored and ranked | Project Shepherd |

---

## Output Artifacts

| Agent | Output File | Final Location |
|-------|-------------|----------------|
| Trend Researcher | `trend-research-output.md` | `strategy/playbooks/research/` |
| Search Query Analyst | `keyword-research-output.md` | `strategy/playbooks/research/` |
| Paid Media Auditor | `competitor-map-output.md` | `strategy/playbooks/research/` |
| Legal Compliance Checker | `legal-analysis-output.md` | `strategy/playbooks/research/` |
| UX Researcher | `target-group-output.md` | `strategy/playbooks/research/` |
| Pipeline Analyst | `roi-model-output.md` | `strategy/playbooks/strategy/` |
| PPC Campaign Strategist | `ads-strategy-output.md` | `strategy/playbooks/strategy/` |
| SEO Specialist | `seo-content-output.md` | `strategy/playbooks/strategy/` |
| Outbound Strategist | `partnership-strategy-output.md` | `strategy/playbooks/strategy/` |
| Project Shepherd | `final-synthesis.md` | `strategy/playbooks/` |

---

## Context for All Agents

Include this block at the top of every agent activation prompt:

```
CONTEXT: Hungarian criminal law firm market research sprint.

Client: 5-person Hungarian law firm (ügyvédi iroda)
Current specialization: Traffic law — közlekedési balesetek, ittas vezetés, szabálysértések
Current acquisition: Google Ads only
Goal: Identify new criminal law niches with low Google Ads competition, high demand growth,
      and Google Ads viability for expansion
Market: Hungary (HU), primary focus Budapest, secondary focus major regional cities
Language of output: Hungarian preferred; English acceptable for technical sections
Legal framework: Magyar Büntető Törvénykönyv (Btk.), EU directives as transposed into HU law
```

---

## Example Output

A completed run of this runbook produced the full market analysis available at:

**`strategy/playbooks/hu-criminal-law-market-analysis.md`**

Key findings from that run:
- **#1 niche**: Cybercrime (kiberbűncselekmények) — 61.5% YoY growth, <3 Google Ads competitors
- **#2 niche**: Corporate/executive defense — 282% growth in corruption cases 2022–2024
- **#3 niche**: Foreign nationals (EN/DE) — 255K foreigners in HU, 0 German-language criminal lawyers
- All three niches have <3 dedicated Google Ads advertisers as of Q1 2026
