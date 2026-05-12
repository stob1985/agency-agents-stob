# Profitable SaaS Niches for Bundled-OSS Hosted Products (2026)

**Research date:** May 12, 2026
**Model:** Bundle 2-5 popular open-source GitHub repos, integrate them into a vertical SaaS, host it for a monthly fee.
**Pricing logic:** Charge per seat or per workspace at ~10-30% of the equivalent commercial SaaS (Intercom, Vanta, Salesforce, ADP, etc.). Margin comes from running the open-source stack on commodity infra (Hetzner/OVH/Vultr) at 80-90% gross margin.

A note on licenses appears at the end. AGPL is included where dual-licensing or "Commons Clause" doesn't bar SaaS-resale; explicit warnings are noted in each niche.

---

## Ranking summary (by profit potential, highest first)

| # | Niche | Target ARPU | Moat (1-10) | TAM signal |
|---|-------|-------------|-------------|------------|
| 1 | AI Voice Receptionist for SMB service businesses | $299-$599/mo | 8 | Vapi/Retell are $50M+ ARR, huge underserved SMB |
| 2 | Compliance-as-a-Service (SOC2/ISO/HIPAA) for startups | $499-$1,499/mo | 9 | Vanta/Drata >$300M ARR combined |
| 3 | Vertical AI Customer Support for e-commerce/SaaS | $149-$799/mo | 7 | Chatwoot $25M+ ARR, Intercom $250M+ |
| 4 | Hosted "Internal AI Platform" for mid-market | $1,000-$5,000/mo | 8 | Dify/Flowise have huge enterprise demand |
| 5 | All-in-one practice management (legal/dental/clinic) | $199-$499/mo | 8 | Clio/Dentrix verticals are $100M+ ARR each |
| 6 | Bundled marketing stack for agencies (white-label) | $99-$499/mo per client | 7 | Agency reselling is a $50B+ market |
| 7 | DevOps platform for solo founders / small teams | $39-$199/mo | 6 | Railway $30M+, Render $50M+ ARR |
| 8 | Hosted e-commerce stack for B2B / DTC operators | $299-$1,499/mo | 7 | Shopify Plus is $20B+ market |
| 9 | Headless CMS + commerce for agencies | $149-$799/mo | 6 | Sanity, Strapi enterprise growth |
| 10 | SMB HR/Payroll/Time-tracking bundle (non-US) | $5-$12/employee/mo | 7 | Gusto/Rippling underserve <50 employee non-US SMBs |
| 11 | Observability-in-a-box for SMB engineering teams | $99-$499/mo | 5 | Datadog cost-avoidance is a real wedge |
| 12 | Open-source AI knowledge base for professional services | $99-$399/mo | 5 | Vector RAG for niche industries |

---

## 1. AI Voice Receptionist for SMB service businesses

**Target customer:** Plumbers, dentists, law firms, real estate teams, HVAC, auto shops, home services - any business that loses 30-50% of calls after hours. 8M+ US SMBs.

**Repos to bundle:**
- `livekit/agents` (Apache-2.0) - real-time voice agent framework: https://github.com/livekit/agents
- `pipecat-ai/pipecat` (BSD-2) - voice pipeline orchestration: https://github.com/pipecat-ai/pipecat
- `dograh-hq/dograh` (Apache-2.0) - drag-and-drop voice flow builder
- `chatwoot/chatwoot` (MIT - older, recently re-licensed; verify before launch) - conversation/CRM layer to log calls and follow up via SMS/email
- Twilio/Telnyx for SIP (commercial APIs, not bundled - passed through)

**Pricing:** $299/mo base + $0.15/min for usage; Pro at $599/mo with unlimited minutes up to 2,000. Target ARPU $450.

**Market & willingness to pay:** Vapi, Retell, Bland, Synthflow all hit $1M+ ARR in months selling to agencies who resell to SMBs. SMBs already pay $200-$800/mo for answering services (Ruby, AnswerConnect, PATLive). Replacing a human at $1,500/mo with a $400/mo AI is an obvious yes.

**Competition gap:** Vapi/Retell are dev tools - they sell APIs. Agencies build on top. The gap is a **turnkey vertical product** ("AI Receptionist for Dentists") with pre-built scripts, calendar integrations (Cal.com), and EHR-aware booking. No major incumbent owns the SMB vertical packaging yet.

**Why bundling works:** SMBs cannot wire LiveKit + Pipecat + Deepgram + ElevenLabs + Twilio + a CRM. They need a phone number and a dashboard. Integration cost alone is 40-80 dev hours - that's the moat.

**Difficulty / moat: 8/10.** Real-time voice is hard to operate reliably. Latency, barge-in, transfer-to-human, CRM hooks. But once running, churn is low because the agent is embedded in operations.

---

## 2. Compliance-as-a-Service (SOC2 / ISO 27001 / HIPAA) for startups

**Target customer:** Seed-to-Series-B startups (500-5,000 employees) trying to land enterprise deals that require SOC2. Currently pay Vanta/Drata/Secureframe $15K-$50K/year.

**Repos to bundle:**
- `getprobo/probo` (Apache-2.0) - open-source SOC2/GDPR/ISO27001 platform: https://github.com/getprobo/probo
- `trycompai/comp` (MPL-2.0) - Comp AI compliance platform: https://github.com/trycompai/comp
- `wazuh/wazuh` (GPL-2.0 - server-side use is fine for SaaS resale, but agents installed on customer endpoints stay GPL) - SIEM + endpoint compliance evidence collection
- `documenso/documenso` (AGPL with commercial license available - **buy commercial license**) - signed policies, vendor agreements
- `n8n-io/n8n` (Sustainable Use License - check terms; AGPL-style restrictions for resale)

**Pricing:** Starter $499/mo (single framework, <25 employees), Growth $999/mo (SOC2 + ISO), Enterprise $1,499-$2,500/mo with auditor coordination.

**Market & willingness to pay:** Vanta hit $220M+ ARR by 2024, Drata >$100M ARR. SOC2 unlocks enterprise revenue worth millions per customer, so $1K/mo is rounding error. ~50,000 US startups need SOC2 annually. Easy 1-2% capture = $25-50M ARR.

**Competition gap:** Vanta/Drata price-anchor at $15K-25K minimum. There's a "good enough for the deal" tier at $5-10K/year that nobody serves well. Probo and Comp AI explicitly target this gap.

**Why bundling works:** Compliance evidence collection spans device management, cloud config scanning, HR onboarding, policy signing, vendor reviews, and audit packaging. Stitching Wazuh + Probo + Documenso + a policy library is a week of integration work for a buyer who has zero security background.

**Difficulty / moat: 9/10.** Auditor partnerships are the real moat. Once a CPA firm trusts your evidence format, you become the recommended choice. Compliance customers churn at <5%/yr because re-implementing is painful.

---

## 3. Vertical AI Customer Support for e-commerce & SaaS

**Target customer:** Shopify/WooCommerce stores doing $1M-$50M GMV; SaaS startups with 10-200 employees. Pay Intercom/Zendesk/Gorgias $200-$2,000/mo.

**Repos to bundle:**
- `chatwoot/chatwoot` (MIT historically, now SSL/MIT hybrid - check) - omni-channel inbox: https://github.com/chatwoot/chatwoot
- `langgenius/dify` (open license with anti-competitive clause - **read carefully; not pure AGPL but restricts resale as "multi-tenant SaaS"**) or `FlowiseAI/Flowise` (Apache-2.0) for the AI agent layer
- `papermark-io/papermark` or `documenso/documenso` (commercial license) for shared docs
- `mautic/mautic` (GPL-3) - drip campaigns for ticket follow-up (run server-side, no AGPL trap)
- `meilisearch/meilisearch` (MIT) for product/knowledge-base search

**Pricing:** Starter $149/mo (1 inbox, 2 seats), Growth $399/mo (5 seats + AI Copilot), Pro $799/mo (unlimited + Shopify-specific automations).

**Note:** Dify uses a restrictive license that disallows offering Dify itself as a managed multi-tenant SaaS. Use Flowise (Apache-2.0) or Langflow (MIT) instead for the agent backend if you want to resell.

**Market & willingness to pay:** Gorgias ($300M+ ARR) proves e-comm support is a winner. Intercom AI starts at $300/mo+. Chatwoot Cloud already does this but is generic - a Shopify-specific bundle with pre-trained order-status, refund, WISMO flows commands a premium.

**Competition gap:** Chatwoot is generic. Gorgias is closed-source and expensive. The wedge is a vertical-specific (Shopify/Klaviyo/Recharge integrations baked in) hosted Chatwoot + Flowise combo. Chatwoot's own cloud doesn't bundle ESP and outbound automation.

**Difficulty / moat: 7/10.** Switching cost is moderate - migration of macros, agent training, integrations. Vertical templates (e.g., 50 pre-built ecommerce flows) are the moat.

---

## 4. Hosted Internal AI Platform for mid-market companies

**Target customer:** 200-2,000-person companies that want a private ChatGPT + RAG with their data, but can't deploy Glean ($60K+/yr) or Microsoft Copilot for compliance reasons. Insurance, financial services, healthcare, manufacturing, government contractors.

**Repos to bundle:**
- `FlowiseAI/Flowise` (Apache-2.0) or `langflow-ai/langflow` (MIT) - visual agent builder
- `open-webui/open-webui` (BSD-3 historically; recent license tightening - **verify before commercial resale**) - chat UI
- `qdrant/qdrant` (Apache-2.0) or `weaviate/weaviate` (BSD-3) - vector store
- `unclecode/crawl4ai` (Apache-2.0) - data ingestion
- `microsoft/markitdown` (MIT) - document conversion
- `lobehub/lobe-chat` (MIT/Apache - check) for branded chat client

**Pricing:** Team $1,000/mo (50 seats), Business $2,500/mo (250 seats + SSO), Enterprise $5,000+/mo (private VPC, on-prem option, HIPAA BAA).

**Market & willingness to pay:** Glean is at $250M+ ARR; Mendable, Vectara, Writer all >$50M ARR. Mid-market alternative-to-Glean has clear demand at half the price. Single enterprise can be worth $60K/yr.

**Competition gap:** Glean is enterprise-only; OpenAI Enterprise is generic. The 200-2,000 employee company wants something in between with deployment optionality (cloud or on-prem). Hosted Flowise + Open WebUI + Qdrant with SSO and audit logs is exactly that.

**Why bundling works:** Customers don't want LangChain. They want a chat box + admin panel + "feed it our wiki". The orchestration of vector store + ingestion + UI + auth is 100+ hours of work.

**Difficulty / moat: 8/10.** Selling is the moat - mid-market sales cycles are 60-90 days. Once embedded with SSO + permissions, switching is painful.

---

## 5. All-in-one practice management for legal / dental / clinics

**Target customer:** Solo and 2-10 person law firms, dental offices, physiotherapy clinics, vet clinics. Currently pay Clio ($99-$149/user/mo), Dentrix ($300+/user), or use a paper-and-Excel mess.

**Repos to bundle (per vertical):**
- `calcom/cal.com` (AGPL - **needs enterprise license for unmodified resale** at scale; small teams OK) - scheduling: https://github.com/calcom/cal.com
- `frappe/erpnext` + `frappe/hrms` (GPL-3) - invoicing, payroll, HR
- `documenso/documenso` (AGPL + commercial license) - e-signature for engagement letters
- `papermark-io/papermark` (AGPL) - secure client portal
- `chatwoot/chatwoot` - client messaging
- For legal: `paperless-ngx/paperless-ngx` (GPL-3) - document/matter management
- For clinics: `OpenEMR/openemr` (GPL-3) - EHR (HIPAA-relevant)
- For dental: `OpenDental` (open source, GPL)

**Pricing:** $199/mo for solo, $99/user/mo team plan, capped at $499/mo for 10 users.

**Market & willingness to pay:** Clio is $200M+ ARR with ~150K firms. Solo practitioners are price-sensitive but locked in. There are ~450K US lawyers in firms <10. Capture 1,000 firms at $300/mo = $3.6M ARR.

**Competition gap:** Clio is expensive and bloated. OpenEMR is unusable without an integrator. The gap is a **vertical-trim hosted bundle** with onboarding included.

**Why bundling works:** A dentist will never deploy OpenEMR + ERPNext + Cal.com themselves. They want one login, one bill, one phone number to call.

**Difficulty / moat: 8/10.** Vertical sales (legal trade shows, dental conferences) plus high switching cost. Compliance (HIPAA BAA, state bar rules) is a moat against generic competitors.

---

## 6. Bundled marketing stack for agencies (white-label)

**Target customer:** Digital marketing agencies serving 10-200 SMB clients. Currently pay HubSpot/ActiveCampaign/Klaviyo per-client and mark up. Want white-label to own the relationship.

**Repos to bundle:**
- `mautic/mautic` (GPL-3) - marketing automation: https://github.com/mautic/mautic
- `knadh/listmonk` (AGPL-3 - server-side OK for SaaS) - newsletter engine: https://github.com/knadh/listmonk
- `PostHog/posthog` (MIT for core; some features under "PostHog License" that restricts SaaS resale - **verify before bundling**) - product analytics
- `plausible/analytics` (AGPL - commercial license needed for resale) or `umami-software/umami` (MIT, recommended) - web analytics
- `formbricks/formbricks` (AGPL + commercial) - surveys/forms
- `n8n-io/n8n` (Sustainable Use License - restricted from resale; consider `Activepieces/activepieces` MIT instead) - automation

**Pricing:** $99/mo per client workspace, agency seats $499/mo for 10 workspaces, $999/mo for unlimited.

**Market & willingness to pay:** GoHighLevel hit $200M+ ARR doing exactly this on closed-source rails. There's room for an "open-source GoHighLevel" with no per-contact pricing.

**Competition gap:** GoHighLevel is closed and expensive at scale (per-contact creep). Vendasta, Buffer-for-Agencies exist but lack the automation depth.

**Why bundling works:** Agencies need white-label + sub-account isolation + billing per client. Self-hosting 6 OSS tools and adding white-label is 200+ hours.

**Difficulty / moat: 7/10.** Agency relationships are sticky. GoHighLevel's success proves the wedge. Avoid n8n's resale restriction; use Activepieces.

---

## 7. DevOps platform for solo founders / small teams

**Target customer:** Indie hackers, 1-10 person startups. Pay Vercel + PlanetScale + Upstash + Resend ($150-$500/mo combined) and want consolidation.

**Repos to bundle:**
- `coollabsio/coolify` (Apache-2.0) - core PaaS: https://github.com/coollabsio/coolify
- `dokploy/dokploy` (Apache-2.0) - alternative orchestrator
- `supabase/supabase` (Apache-2.0) - DB + auth + storage
- `appwrite/appwrite` (BSD-3) - BaaS
- `pocketbase/pocketbase` (MIT) - lightweight backend
- `posthog/posthog` (verify license terms) or `umami-software/umami` (MIT) - analytics
- `meilisearch/meilisearch` (MIT) - search

**Pricing:** Hobby $39/mo (1 project, 2GB DB), Pro $99/mo (unlimited projects, 50GB DB), Team $199/mo.

**Market & willingness to pay:** Railway ($30M+ ARR), Render ($50M+ ARR), Fly.io ($30M+) prove the wedge. Coolify Cloud is already growing. Sevalla, Easypanel, Hostinger Horizons all entering.

**Competition gap:** Heavy competition, but each player picks a niche (Railway = devs, Render = teams, Fly = global edge). A bundle aimed specifically at "1-3 person SaaS bootstrappers" with built-in auth, DB, analytics, and Stripe billing is differentiated.

**Difficulty / moat: 6/10.** Crowded space, but small teams have stickiness once data and DNS are migrated. Lower margin (price-sensitive customers) than B2B niches above.

---

## 8. Hosted e-commerce stack for B2B / DTC brands

**Target customer:** $1M-$50M GMV brands outgrowing Shopify, B2B wholesalers needing custom pricing/quotes, Shopify Plus alternatives.

**Repos to bundle:**
- `medusajs/medusa` (MIT) - commerce engine: https://github.com/medusajs/medusa
- `saleor/saleor` (BSD-3) - alternative engine
- `vendure-ecommerce/vendure` (MIT/GPL-3 commercial dual) - alternative
- `strapi/strapi` (MIT for community) - headless CMS for content/blog
- `payloadcms/payload` (MIT - now owned by Figma) - admin CMS
- `mautic/mautic` - marketing automation
- `chatwoot/chatwoot` - support

**Pricing:** Starter $299/mo (1 store, $250K GMV), Pro $799/mo (3 stores, $5M GMV), Plus $1,499+/mo with custom development.

**Market & willingness to pay:** Shopify Plus starts at $2,500/mo. BigCommerce Enterprise similar. Brands paying these prices for closed software are an open door for a 50% cheaper, customizable alternative. Medusa Cloud's traction is evidence.

**Competition gap:** Medusa Cloud exists but is dev-focused. Saleor Cloud is enterprise. The gap: managed Medusa + storefront + marketing automation + support inbox bundled for non-technical operators.

**Difficulty / moat: 7/10.** GMV-linked pricing makes high-ACV customers very valuable. Switching cost (catalog, customer DB, integrations) is severe once embedded.

---

## 9. Headless CMS + commerce bundle for agencies

**Target customer:** Web/marketing agencies building sites for $5K-$100K projects. Need a stack they can host and resell.

**Repos to bundle:**
- `payloadcms/payload` (MIT) - admin CMS
- `directus/directus` (BSL → BSD after time) - data layer
- `strapi/strapi` (MIT community)
- `umami-software/umami` (MIT) - analytics
- `formbricks/formbricks` (AGPL+commercial) - forms
- `medusajs/medusa` (MIT) when commerce is needed

**Pricing:** $149/mo per client site (CMS only), $499/mo with commerce, agency unlimited at $1,999/mo.

**Market & willingness to pay:** Sanity, Contentful, Webflow all have agency programs that drive most of their revenue. WP Engine doing >$200M ARR mostly through agencies.

**Difficulty / moat: 6/10.** Easier to build than #1-#5 but less defensible; agencies can switch with moderate pain. Margin comes from volume.

---

## 10. SMB HR / Payroll / Time-tracking bundle (non-US markets)

**Target customer:** 5-50 employee SMBs in markets where Gusto/Rippling don't operate well (LATAM, SE Asia, MENA, Eastern Europe, Africa).

**Repos to bundle:**
- `frappe/hrms` (GPL-3) - HR + payroll: https://github.com/frappe/hrms
- `frappe/erpnext` (GPL-3) - accounting integration
- `orangehrm/orangehrm` (AGPL-3 - check resale terms; commercial license sold by OrangeHRM) - alternative HR
- `kimai/kimai` (AGPL) - time tracking, alternative `mautic/mautic` is unrelated
- `akaunting/akaunting` (calls home for license - **may block self-hosted SaaS resale**)
- `calcom/cal.com` - leave/PTO scheduling

**Pricing:** $5/employee/mo basic, $12/employee/mo full payroll + tax filing assistance. Target ARPU $200-$400/mo per company.

**Market & willingness to pay:** Gusto charges $40/employee/mo. Brazilian/Mexican/Indian SMBs cannot afford that, but can afford $5-10. Frappe HR has 20K+ deployments already.

**Competition gap:** Local players (Pleo, Personio in EU) are well-funded but exclude LATAM/Africa. ERPNext partners exist but don't run hosted multi-tenant SaaS.

**Difficulty / moat: 7/10.** Payroll = local tax compliance per country, which is a moat but also a barrier. Pick 1-2 countries to start (Mexico, Brazil).

---

## 11. Observability-in-a-box for SMB engineering teams

**Target customer:** 10-100 person engineering teams paying Datadog/New Relic $5K-$50K/mo who want to cut bills 70%.

**Repos to bundle:**
- `SigNoz/signoz` (MIT) - APM + traces + logs: https://github.com/SigNoz/signoz
- `grafana/grafana` (AGPL since 2021 - **commercial AGPL trap for SaaS resellers**; alternative: `grafana/grafana` v7.x older Apache fork or stick with SigNoz native UI)
- `louislam/uptime-kuma` (MIT) - uptime: https://github.com/louislam/uptime-kuma
- `getsentry/sentry` (FSL → Apache after time; **check FSL non-compete for SaaS resale**) - error tracking. Alternative: `GlitchTip/glitchtip` (MIT, Sentry-protocol compatible)
- `OneUptime/oneuptime` (MIT) - status page

**Pricing:** Starter $99/mo (5 services, 30 day retention), Team $299/mo (unlimited, 90 day), Pro $499/mo (full retention + SSO).

**Market & willingness to pay:** Datadog bill rage is a known phenomenon. Teams will eagerly halve a $20K bill. But this is a crowded space with Better Stack, Axiom, Highlight competing.

**Difficulty / moat: 5/10.** Lower moat because data is portable (OTel). Differentiation comes from generous limits and good defaults.

---

## 12. Open-source AI knowledge base for professional services

**Target customer:** Accounting firms, law boutiques, consulting practices wanting their own ChatGPT trained on engagement letters, client docs, and internal precedents.

**Repos to bundle:**
- `langflow-ai/langflow` (MIT) - RAG builder: https://github.com/langflow-ai/langflow
- `FlowiseAI/Flowise` (Apache-2.0) - alternative
- `qdrant/qdrant` (Apache-2.0) - vector DB
- `open-webui/open-webui` (verify current license) - chat UI; alternative `lobehub/lobe-chat`
- `unclecode/crawl4ai` (Apache-2.0) - doc ingestion
- `nextcloud/server` (AGPL - sold commercially by Nextcloud GmbH; **buy enterprise license to resell**) - file storage

**Pricing:** $99/mo (5 users, 10GB), $299/mo (25 users, 100GB), $399/mo (50 users, SSO).

**Market & willingness to pay:** Accountants/lawyers will pay $100-$300/user/mo for vertical AI (Spellbook, Hebbia evidence). Bundled at lower price for solo+small teams is wedge.

**Difficulty / moat: 5/10.** Lower because RAG + chat is rapidly commoditizing. Differentiate via vertical templates and audit trails.

---

## License cheat-sheet (CRITICAL for this business model)

| License | OK for hosted SaaS resale? | Notes |
|---------|---------------------------|-------|
| MIT, Apache-2.0, BSD | YES | Always safe. Prefer these. |
| MPL-2.0 | YES | File-level copyleft only. |
| AGPL-3.0 | Maybe | Must publish source of any modifications you ship to users. Many vendors sell a commercial license to avoid this. **Pure unmodified AGPL hosted as SaaS is legal, but if you patch it you must publish patches.** |
| GPL-3.0 / GPL-2.0 | YES for SaaS | SaaS Loophole - hosting is not distribution. Safe unless you ship a client binary. |
| SSPL (Mongo) | NO | Explicitly bans hosted resale. |
| BUSL / Sustainable Use (n8n) | NO for resale | Restricts hosting as a service to competitors. |
| FSL (Sentry, others) | NO for 2-4 years | Non-compete clause blocks hosted resale of similar service until license converts to Apache. |
| Dify's open-source license | NO for multi-tenant SaaS | Explicit clause disallows multi-tenant resale. |

**Rule of thumb for this business:** Prefer MIT/Apache stacks (Medusa, LiveKit, Pipecat, Flowise, Langflow, Qdrant, Cal.com self-host below 3 users, Coolify, Activepieces). Treat AGPL projects (Mautic, Plausible, Documenso, Grafana >7.x, Cal.com, Nextcloud) as "buy a commercial license or contribute changes back."

---

## Cross-cutting recommendations

1. **Pick the boring vertical first.** Compliance, legal, dental, payroll - higher ACV, lower competition than dev tools.
2. **Avoid Dify and n8n as reseller backbones** despite their popularity. Their licenses block SaaS resale. Use Flowise/Langflow and Activepieces instead.
3. **The hosting margin is not the moat.** Vertical templates, onboarding services, and compliance partnerships are. Plan to spend 40% of revenue on go-to-market for B2B.
4. **Start with #1, #2, #5, or #6.** Highest profit-per-customer with clearest pain points.
5. **Steal Supabase's playbook:** ship the OSS, run the hosted version, charge for managed + premium features (SSO, audit logs, dedicated IPs, white-label).

---

## Sources

- [GitHub Trending - Daily](https://github.com/trending)
- [GitHub Trending - Monthly](https://github.com/trending?since=monthly)
- [awesome-foss-alternatives (sfermigier)](https://github.com/sfermigier/awesome-foss-alternatives)
- [awesome-oss-alternatives (Runa Capital)](https://github.com/RunaCapital/awesome-oss-alternatives)
- [openalternative.co](https://openalternative.co/)
- [opensaas.directory](https://opensaas.directory/)
- [Supabase revenue (Sacra)](https://sacra.com/c/supabase/)
- [Chatwoot pricing](https://www.chatwoot.com/pricing/self-hosted-plans/)
- [Vapi alternatives - Dograh blog](https://blog.dograh.com/free-alternatives-to-vapi-4-oss-options-in-2026/)
- [Probo - open source SOC2](https://github.com/getprobo/probo)
- [Comp AI launch](https://www.helpnetsecurity.com/2026/04/07/comp-ai-open-source-compliance-platform/)
- [Frappe HRMS](https://github.com/frappe/hrms)
- [Medusa](https://medusajs.com/)
- [Saleor](https://saleor.io/)
- [Open Core Ventures - AGPL analysis](https://www.opencoreventures.com/blog/agpl-license-is-a-non-starter-for-most-companies)
- [Coolify](https://coolify.io/)
- [Indie Hackers - OSS portfolio at $2.8M ARR](https://www.indiehackers.com/post/tech/building-a-2-8m-arr-open-source-portfolio-MEiwnqxp2Eab8Ut9qZvO)
- [SigNoz](https://signoz.io/)
- [Cal.com open source review](https://cal.com/blog/open-source-calendar-booking-systems-a-comprehensive-review)
- [Dify open-source platform](https://github.com/langgenius/dify)
- [Flowise AI](https://flowiseai.com/)
- [Langflow](https://github.com/langflow-ai/langflow)
