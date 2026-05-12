# Mély piackutatás: Két SaaS niche open-source bundle-ből

**Készült:** 2026. május 12.
**Cél:** Magyar alapító számára konkrét, akcióképes elemzés két nichre, amelyek open-source GitHub repok bundleolásával építhetők SaaS-ként.

---

# NICHE 1 — AI Voice Receptionist KKV szolgáltatóknak ($299–599/hó)

## 1. Mit építünk pontosan

**Termék.** Egy "AI Front Desk" SaaS, amely 24/7 fogadja az SMB szolgáltatók (fogorvosok, vízvezeték-szerelők, ügyvédi irodák, ingatlanügynökök, HVAC-cégek, fodrász/szépségszalonok) telefonhívásait. Az AI agent angolul (és magyarul, németül, spanyolul) válaszol, kvalifikálja a hívót, időpontot foglal a meglévő naptárba (Google Calendar, Calendly, Cal.com, vagy iparági CRM-be — pl. Dentrix, ServiceTitan, Clio), SMS visszaigazolást küld, és a beszélgetéseket egy közös inboxba szinkronizálja, ahol az emberi munkatárs is válaszolhat. A vertikálisan testreszabott "playbook" (pl. "Sürgős fogfájás triage", "Vízvesztés sürgősségi protokoll") az, ami megkülönbözteti egy general-purpose Vapi-tól.

**Probléma, akit megfizet.** SMB szolgáltatóknál a hívások 37–62%-a megválaszolatlan munkaidőn kívül és csúcsidőben ([getaira.io](https://www.getaira.io/blog/missed-business-calls-statistics), [pcnanswers.com](https://pcnanswers.com/missed-call-revenue-study/)); egy szerelő/HVAC cég évi $45–120K bevételt veszít elszalasztott hívásokon ([callbirdai.com](https://www.callbirdai.com/blog-contractors-lose-money-missed-calls)). Egy átlagos fogászati páciens 10 év LTV-je $15K, egy HVAC ügyfélé $12K — egyetlen elszalasztott hívás 4 számjegyű veszteség. A vevő a 1–10 alkalmazottas üzlettulajdonos, aki nem akar $1,600+/hó Ruby-t fizetni, és Smith.ai $95 + per-call modelljénél is jobb fix árat akar.

**Repó bundle és architektúra.**

```
┌───────────────────────────────────────────────────────────────┐
│  TWILIO / TELNYX  (PSTN/SIP trunking — vendor)                │
└──────────────┬────────────────────────────────────────────────┘
               │ SIP/WebRTC
┌──────────────▼────────────────────────────────────────────────┐
│  livekit/agents  (Apache 2.0) — realtime media + WebRTC       │
│  + livekit/livekit server self-hosted                         │
└──────────────┬────────────────────────────────────────────────┘
               │ audio frames
┌──────────────▼────────────────────────────────────────────────┐
│  pipecat-ai/pipecat (BSD-2) — STT→LLM→TTS pipeline, VAD,     │
│  turn-taking, interruption handling                          │
│  Plugins: Deepgram/Whisper STT, OpenAI/Anthropic LLM,         │
│  ElevenLabs/Cartesia TTS                                      │
└──────────────┬────────────────────────────────────────────────┘
               │ structured events
┌──────────────▼────────────────────────────────────────────────┐
│  dograh-hq/dograh (BSD-2) — drag-and-drop workflow builder    │
│  iparág-specifikus playbookkal (booking, intake, triage)      │
└──────────────┬────────────────────────────────────────────────┘
               │ webhook / chat events
┌──────────────▼────────────────────────────────────────────────┐
│  chatwoot/chatwoot (Community MIT) — egységes inbox,         │
│  SMS/WhatsApp/email follow-up, ügynöki "takeover"            │
└───────────────────────────────────────────────────────────────┘
```

A LiveKit ad ipari minőségű WebRTC-t és telefonintegrációt, a Pipecat a media pipeline-t (STT→LLM→TTS, smart-turn detektálás), a Dograh a vertikális workflow buildert no-code felületen, a Chatwoot az ügyfél-szervizoló réteget (mert egy AI receptionist 0 érték follow-up nélkül).

**Licencanalízis (KRITIKUS).**
- `livekit/agents` — **Apache 2.0** ✅ kereskedelmi SaaS OK ([github.com/livekit/agents](https://github.com/livekit/agents))
- `pipecat-ai/pipecat` — **BSD 2-Clause** ✅ teljesen permissive ([github.com/pipecat-ai/pipecat](https://github.com/pipecat-ai/pipecat))
- `dograh-hq/dograh` — **BSD 2-Clause** ✅ ([github.com/dograh-hq/dograh](https://github.com/dograh-hq/dograh))
- `chatwoot/chatwoot` — **MIT (Community)** ✅ DE: a Chatwoot TOS kifejezetten tiltja a "SaaS klónt vagy direkt rebrand-et" ([chatwoot.com/terms-of-service](https://www.chatwoot.com/terms-of-service/), [restack.io chatwoot license](https://www.restack.io/docs/chatwoot-knowledge-chatwoot-license-info)). **Kockázat:** ha a termék fő value prop-ja a Chatwoot inbox, jogi szürke zóna. Megoldás: a Chatwoot embedded modul, nem a "core product"; alternatíva [Twenty CRM (AGPL)] vagy saját egyszerű inbox.
- **Csapdák:** semmilyen AGPL repo. Tiszta kombináció.

## 2. Miért most

- **Voice AI költséggörbe összeomlott:** 2024 elején $0.30–0.50/min volt egy teljes voice stack; 2026-ban Cartesia Sonic, Deepgram Nova-3 és olcsóbb LLM-ek miatt $0.05–0.10/min ([retellai.com voice agent pricing](https://www.retellai.com/blog/ai-voice-agent-pricing-full-cost-breakdown-platform-comparison-roi-analysis)).
- **Latency küszöb átlépve:** A 2025-ös smart-turn detection és streaming TTS együtt <800ms first-token latency-t adnak — ez az a pont, ahol egy SMB vevő már nem ismeri fel, hogy AI-val beszél.
- **Piacméret robban:** AI voice agents market $2.54B (2025) → $35.24B (2033), 39% CAGR ([grandviewresearch.com](https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report)). Voice AI funding 8×-ra nőtt 2024-2025-ben ([pymnts.com](https://www.pymnts.com/artificial-intelligence-2/2025/voice-ai-funding-surges-8x-as-businesses-humanize-chatbots/)).
- **Tailwind 1:** A munkaerőhiány az USA szolgáltató szektorban krónikus — egy receptionist $35K–55K/év, plusz benefits és pótlás. AI ROI <2 hónap.
- **Tailwind 2:** Air.ai-t az FTC kitiltotta deceptive claims miatt 2026 márciusában ([ftc.gov Air AI](https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-sues-stop-air-ai-using-deceptive-claims-about-business-growth-earnings-potential-refund)) — egy iparági nagy "rossz fiú" eltűnt, "honest, working AI receptionist" pozícionálás most különösen erős.
- **Tailwind 3:** Vapi/Retell ($50M ARR 2025, [retellai.com pricing](https://www.retellai.com/blog/ai-voice-agent-pricing-full-cost-breakdown-platform-comparison-roi-analysis)) developer-platform — túl bonyolult egy fogorvosnak. A "vertikális GTM réteg fölöttük" most óriási rés.
- **2 éve ez nem ment volna:** GPT-3.5 latency >3s, TTS kevés hangja $0.30/1K char, és nem volt Pipecat/LiveKit-szintű OSS pipeline. 2026-ban solo founder összerakja 3 hét alatt.

## 3. Piacméret és ARPU

**TAM/SAM/SOM.**
- **TAM:** Global AI voice agents = $3.51B (2026) → $35B (2033) ([grandviewresearch.com](https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report)). Conversational AI $17.97B (2026) ([fortunebusinessinsights.com](https://www.fortunebusinessinsights.com/conversational-ai-market-109850)).
- **SAM (US SMB szolgáltató szegmens):** 36.2M US SMB ([sba.gov](https://advocacy.sba.gov/2025/06/30/new-advocacy-report-shows-the-number-of-small-businesses-in-the-u-s-exceeds-36-million/)). Releváns vertikálisok: 127K plumber ([ibisworld.com](https://www.ibisworld.com/united-states/number-of-businesses/plumbers/1946/)), ~200K dentist office, ~440K law firm, ~120K HVAC contractor, ~80K real estate brokerage, ~85K salon. **Összesen ~1.05M target üzlet.** Ha 40% telefon-intenzív és appointment-driven: **SAM ≈ 420K vállalkozás × $5K/év ARPU = $2.1B/év**.
- **SOM (3-5 év):** 0.5%-os penetráció = 2,100 vevő × $4,800 ARPU = **$10M ARR**.

**ARPU tiers.**
| Csomag | Ár | Tartalmaz | Cél vevő |
|--------|------|-----------|---------|
| Starter | $299/hó | 500 perc, 1 lokáció, alap playbook | Solo dentist, single shop |
| Growth | $499/hó | 2,000 perc, 3 lokáció, CRM integráció, SMS automation | 5–15 fős cég |
| Pro | $899/hó | 8,000 perc, white-label option, prioritás support | Multi-location, kis lánc |
| Enterprise | $1,999+/hó | Egyedi playbook, SOC2 BAA, SLA | DSO, regionális szolgáltató |

Effektív blended ARPU: **$450/hó ($5,400/év)**.

**Útvonal a mérföldkövekhez.**
- **$100K MRR** = 222 vevő @ $450. Reális 12–18 hónap alatt egy fókuszált vertikális (pl. dental + plumber) GTM-mel.
- **$1M ARR** = 185 vevő @ $5,400. ~14–20 hónap.
- **$10M ARR** = 1,850 vevő, kell partner channel (PMS-integrációk, agency reseller).

## 4. Konkurenciaelemzés

| Cég | Ár | ARR/Funding | Erősségek | Gyengeségek | Wedge |
|-----|------|---------|-----------|-------------|-------|
| **Vapi** | $0.05/perc + add-ons (effective $0.30/perc), $500/hó startup ([vapi.ai/pricing](https://vapi.ai/pricing)) | $20M Series A Bessemer, 100K+ dev ([vapi.ai/blog](https://vapi.ai/blog/vapi-secures-20m-to-start-the-voice-revolution-2)) | Developer szeretik, gazdag SDK | DIY, nincs white-label, nem SMB-knek ([trillet.ai](https://www.trillet.ai/blogs/vapi-alternative-for-agencies)) | Vapi alatt vagyunk: vertikális, "kész terméket" árulunk fogorvosnak |
| **Retell AI** | $0.07–0.31/perc ([retellai.com/pricing](https://www.retellai.com/pricing)) | $50M ARR 2025 ([retellai.com pricing breakdown](https://www.retellai.com/blog/ai-voice-agent-pricing-full-cost-breakdown-platform-comparison-roi-analysis)) | Hyper-realistic voice, jó dev DX | Per-minute, kevés vertikális template | Fix ár, iparág-specifikus playbook |
| **Bland AI** | $0.09/perc outbound, $0.04 inbound, Build $299+/hó ([bland.ai/pricing](https://www.bland.ai/pricing)) | $40M Series B Jan 2025 ([cloudtalk.io](https://www.cloudtalk.io/blog/bland-ai-pricing/)) | Skálázható, enterprise outbound | Add-on költségek megszaladnak, min. $150K/év ROI | "Honest pricing", no surprise fees |
| **Synthflow** | $375/hó (2K perc), Agency $1,250/hó (6K perc) ([synthflow.ai pricing](https://synthflow.ai/blog/voice-ai-cost)) | $7M funding, 45M+ hívás ([synthflow.ai](https://synthflow.ai/)) | Flat ár, agency-friendly | Generic templates, gyengébb integráció | Mélyebb iparág-specifikus integráció (Dentrix, ServiceTitan, Clio) |
| **Goodcall** | $59/$99/$199 per agent/hó ([goodcall.com/pricing](https://www.goodcall.com/pricing)) | Google spin-out, ~$4M seed | Ingyenes tier, SMB UX | Limitált funkciók $199 alatt, "100 unique customers" cap | Több perc, mélyebb integráció, premium support |
| **Air.ai** | Nincs (FTC tiltás) | FTC settlement, $18M judgment ([ftc.gov](https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-sues-stop-air-ai-using-deceptive-claims-about-business-growth-earnings-potential-refund)) | — | Megszűnt | "Honest competitor" pozícionálás |
| **Smith.ai** | $95–$1,125+/hó AI + hibrid ([smith.ai/pricing](https://smith.ai/pricing/ai-receptionist)) | Bootstrapped, ~$30M est. ARR | Hibrid (AI+ember), brand bizalom | Per-call modell, drága magasabb tier-en | Fix flat-rate, kiszámítható |
| **Ruby Receptionists** | $235–$1,640/hó human ([ruby.com](https://www.ruby.com/plans-and-pricing/)) | Bootstrapped, est. $100M ARR | Premium ügyvédi brand | Csak emberi, drága | 5× olcsóbb, 24/7 |
| **AnswerConnect** | $325/hó + $1.95–2.25/min overage | Legacy answering service | 24/7 emberi | Régi UX, drága overage | Modern stack, no overage |
| **PolyAI** | $150K+/év enterprise ([myaifrontdesk.com](https://www.myaifrontdesk.com/blogs/unveiling-the-top-white-label-ai-voice-agent-solutions-for-your-business-253c4)) | $50M+ funding | Enterprise minőség | Nem SMB-knek | Lefelé támadunk, SMB-friendly UX |
| **Rosie (home services)** | n.a. | Niche player | ServiceTitan integráció, vertikális | Csak home services | Több vertikális, mélyebb integrációk |
| **My AI Front Desk** | $65–$995/hó | Bootstrapped | White-label reseller program | Generic, gyengébb dialog quality | Pipecat 1.0 minőség |

**Wedge összegezve:** A Vapi/Retell/Bland túl alacsony szinten van (developer), a Smith.ai/Ruby túl drága és/vagy emberi, a Goodcall/Synthflow generikus. Hely van egy **vertikális, kész-csomag, fix-ár megoldásnak ($299–599) amely előre konfigurált playbookkal + PMS-integrációval érkezik**.

## 5. Go-to-market stratégia

**Első 10 vevő honnan jön.**
1. **5 vevő hideg outbound-ből** egy szűk vertikálisra (pl. boutique dental practice US Sun Belt-en, 2–5 fő). Apollo.io-ról szűrt list, személyes Loom video minden hívás elemzéssel ("hallgattam meg, hogyan veszik fel a telefont, itt 3 elveszett ügyfél a múlt héten").
2. **3 vevő Facebook/Reddit közösségekből:** r/Dentistry, r/smallbusiness, r/Plumbing, Dental Town fórum, plumber/HVAC Facebook csoportok. Nem hirdetni, hanem segíteni és case study-t megosztani.
3. **2 vevő agency partnertől:** kapcsolatfelvétel local SEO / Google Ads ügynökségekkel, akik már szolgálnak HVAC/dental klienseket — adunk nekik 30% recurring revshare-t.

**Pricing & packaging.**
- $299/$499/$899/$1,999 tier (lásd fent).
- **14 napos free trial** (NEM "demo only" — a kapcsolat csak akkor működik, ha a vevő látja saját telefonszámán). Stripe trial, no credit card kötelező az első 7 napra.
- **Annual contract 20% kedvezmény** + 2 hónap ingyen onboarding.
- **Setup fee elhagyva** (verseny: Vapi/Retell setup ingyen) — de "white-glove onboarding" $499 egyszeri, opcionális.

**Disztribúciós csatornák rangsorolva (12 hónap, hatékonyság sorrendben).**
1. **Vertikális kontent + organikus SEO:** "AI receptionist for dentists" típusú SEO oldalak. ROI 6–12 hónap múlva, de a kompetitorok (Synthflow/Retell) erre építenek ARR-jüket.
2. **Hideg email outbound** (Apollo + Instantly): vertikális × geo szegmentáció, hangfelvétellel a saját számukról. Heti 500 cég → 2% reply → 0.5% close.
3. **Agency partnerprogram:** local digital marketing ügynökségek (kb. 35,000 az USA-ban). Reseller dashboard + revshare. **Ez a $1M ARR-ig vezető csatorna.**
4. **Iparági szoftver marketplace-ek:** Dentrix Marketplace, ServiceTitan Marketplace, Clio App Directory, Cal.com extensions, GoHighLevel marketplace.
5. **Iparági konferenciák/trade shows:** Greater New York Dental Meeting (~46K résztvevő), HVAC Excellence, ABA TECHSHOW. Tabletop $5–15K + travel.
6. **Paid: Google Ads "ai receptionist for [vertical]" + Meta retargeting.** Egyelőre drága ($150 CPL), kerülendő $50K MRR alatt.
7. **YouTube vertikális tutorialok** ("How I set up an AI receptionist for my plumbing business in 12 minutes").
8. **Product Hunt launch** csak az MVP után 2-3 hónappal — nem ideális ICP, de brand-érték.

**Konkrét outbound script (fogorvosnak).**

> Subject: Hívtam Önöket, 4. csengetés után átment az üzenetrögzítőre
>
> Dr. [Név],
>
> Tegnap 14:32-kor felhívtam a [Praxis Név]-et, 4 csengetés után üzenetrögzítő volt. Megpróbáltam időpontot foglalni új pácienseként — egy átlagos páciens 10 éves LTV-je ~$15K, és Önök ezt eldobták.
>
> 30 másodperces Loom-ot készítettem, hogyan veszi fel az AI receptionistünk a hívást, foglal időpontot a Dentrix-be, és küld SMS visszaigazolást: [link]
>
> $299/hó, 14 nap free trial, törlés bármikor. Megéri?
>
> — [Név]

**0–12 hónapos roadmap.**
- **M1–M2:** MVP build (lásd 6. fejezet), 5 alpha tester ingyen (dental + plumber).
- **M3–M4:** Első fizető 10 vevő, $299 tier, hideg outbound + Loom.
- **M5–M6:** SEO oldalak indítása (8–10 vertikális landing), G2/Capterra listing, $5K MRR.
- **M7–M9:** Agency partnerprogram launch, white-label dashboard, $20K MRR.
- **M10–M12:** Első iparági konferencia (HVAC vagy dental), Dentrix marketplace beadás, $50–100K MRR.

## 6. MVP architektúra

**Mit építünk először (minimum viable bundle).**

```
[Twilio number] → [LiveKit SIP gateway] → [Pipecat pipeline:
    Deepgram Nova-3 STT
    → GPT-4o-mini (function calling)
    → Cartesia Sonic TTS]
→ [Cal.com API booking webhook] → [SMS confirmation via Twilio]
→ [Chatwoot inbox sync]
```

Csak **EGY vertikális** (dental) az MVP-ben, 1 playbook ("new patient intake + appointment booking"), Cal.com integráció (mert Dentrix integráció >2 hónap egyedül). 2. vertikális 3. hónapban (plumber).

**Hosting/infra.**
- LiveKit server: Fly.io vagy AWS EC2 c6i.xlarge (~$150/hó induláshoz).
- Pipecat workers: Fly.io Machines / Modal.com (per-call serverless, ~$0.02/min infra).
- Adatbázis: Supabase (Postgres + auth + storage), $25/hó induláshoz.
- Frontend dashboard: Next.js + Vercel, $20/hó.
- Telefónia: Twilio Voice + Programmable SMS, $1/szám/hó + $0.0085/perc.
- Voice stack költség: ~$0.08–0.12/perc all-in (Deepgram $0.0043/perc + GPT-4o-mini ~$0.02 + Cartesia $0.025/perc + LiveKit $0).
- **Gross margin @ $299 (500 perc):** Bevétel $299, COGS ~$50 + $30 infra = 73% margin.

**Becsült build time.**
- **Solo founder, full-stack:** 6–8 hét MVP-ig (élő hívás → naptárfoglalás → SMS).
- **2 fős csapat (BE + FE):** 4–5 hét.
- Mi miatt nem 2 hét? PSTN/SIP debug, hang minőség tuning, hallucinációkezelés, függőségi hibák ezeknek a frameworkoknek.

**Build vs. buy döntések.**
| Komponens | Döntés | Miért |
|-----------|--------|-------|
| WebRTC media | **Buy (LiveKit Cloud)** induláshoz, később self-host | A self-hosted SIP-debug elveszi 4 hetet |
| STT | **Buy (Deepgram)** | Whisper self-hosted = 2× latency, nem éri meg |
| LLM | **Buy (OpenAI/Anthropic)** | Self-hosted Llama costos és lassú SMB volumen-nél |
| TTS | **Buy (Cartesia/ElevenLabs)** | Open TTS minősége még nem versenyképes |
| Workflow builder | **Build on Dograh** | Ez a USP |
| Inbox | **Embed Chatwoot self-hosted** | OSS, gyors, kerüljük a Chatwoot SaaS-resale TOS-t |
| CRM integráció | **Build (Cal.com → Dentrix később)** | Minden vertikálisnál kritikus differenciátor |
| Billing | **Buy (Stripe)** | Standard |

## 7. Kockázatok és moat

**Top 5 kockázat rangsorolva.**

1. **OpenAI/Anthropic API price hike vagy availability gap.** Voice-on per-perc költségek 50%-ban LLM-ek. Mitigáció: multi-provider routing (Anthropic + OpenAI + Groq), és Llama 3.3 self-host edge-case-ekre.
2. **Vapi/Retell elindít vertikális SMB terméket.** Valószínűség: közepes (Retell már listázza "industry templates"-eket). Mitigáció: gyors moat-építés integrációkban (Dentrix, ServiceTitan, Clio) és márka-bizalmon.
3. **AI hallucinated booking/időpont egy fogorvosi rendelőben → reputációs károk.** Egyetlen viral tweet meg tudja ölni a brandet. Mitigáció: minden booking confirmation human-in-the-loop tier-1-en, "guardrails" Pipecat-ban, audit log mindenhez.
4. **Chatwoot TOS letiltja a SaaS-resale-t.** Mitigáció: a Chatwoot legyen embedded helper modul, nem a "core product"; backup: saját inbox 3 hét alatt.
5. **Air.ai-szerű FTC/AG figyelem AI-claims-en.** Mitigáció: extrém konzervatív marketing copy, no "10× revenue guarantee", money-back garancia transzparensen kezelt.

**Moat építés.**
- **Iparág-specifikus playbookok:** 50+ "skill template" (sürgősségi triage, biztosítási kérdezősködés, intake form) — más voice platform ezt nem tudja gyorsan replikálni.
- **PMS/iparági CRM integrációk:** Dentrix, Open Dental, ServiceTitan, Housecall Pro, Clio, MyCase, AdvocateHub. **Minden integráció 2–6 hét + iparági kapcsolat.** Ez a strukturális moat.
- **Hangminta dataset:** millió perces hívások a saját vertikálisokban → finetune-olt turn-detection és intent classifier. Switching cost ↑.
- **Brand:** "honest AI receptionist", Air.ai post-FTC légkörben prémium pozíció.

**Failure modes hasonló cégeknél.**
- **Air.ai** — over-promise, FTC ban, brand-leégés.
- **Voiceflow** (chatbot) — fontolt vertikális, generic maradt, agency-knek került, alacsony ARR/customer.
- **Drift** — túl gyorsan moved upmarket, elveszítette SMB ICP-t.

## 8. Első 90 nap akcióterv

**Hét 1–2: Validáció + infra.**
- 30 cold call dentist + plumber: "mit fizetnél egy AI-nak, aki felveszi a telefonod?"
- LiveKit Cloud account, Twilio account, Deepgram + Cartesia + OpenAI API.
- GitHub repo: pipecat skeleton, single test call működik.

**Hét 3–4: MVP v0.1.**
- Egy működő hívási flow: hívás fogadás → névfelvétel → Cal.com booking → SMS.
- Egyetlen "dental new patient" playbook hardkódolva.
- Dashboard: hívásnaplók, transcript view (Next.js + Supabase).

**Hét 5–6: Alpha test.**
- 5 ingyenes alpha (3 dental + 2 plumber). Naponta hallgatjuk a hívásokat, javítjuk a promptot.
- Pricing landing page (Carrd vagy Webflow), $299/$499/$899 tier.

**Hét 7–8: Első fizetők.**
- Stripe Checkout, 14 napos trial.
- Hideg outbound launch: 200 cég/hét Apollo + Instantly + Loom video.
- Cél: 3 fizető vevő ($900 MRR) hét 8 végére.

**Hét 9–10: Második vertikális + Chatwoot integráció.**
- HVAC vagy law firm playbook addolása.
- Chatwoot self-hosted embed: ügynöki "takeover", SMS follow-up.

**Hét 11–12: Repeatable GTM.**
- 10 fizető vevő = ~$3,500 MRR.
- Első 3 SEO oldal indítása ("AI receptionist for dentists" stb.).
- 5 agency partner kapcsolatfelvétel, partnerprogram MVP-je.

**90. nap KPI:** 10 fizető vevő, $3–5K MRR, 2 vertikális playbook, 1 PMS-integráció (Cal.com), 3 SEO oldal, agency program v0.

---

# NICHE 2 — Compliance-as-a-Service startupoknak (SOC2/ISO/HIPAA) ($499–1,499/hó)

## 1. Mit építünk pontosan

**Termék.** "Compliance OS" Series A/B SaaS startupoknak (10–100 fő), amely végigvezet az első SOC 2 Type 1 → Type 2 → ISO 27001 → HIPAA úton. Egy platform fogja össze: (a) policy/control management, (b) automated evidence collection (AWS/GCP/GitHub/Okta/JumpCloud/Slack integráció), (c) belső biztonsági monitoring (SIEM/XDR a Wazuh-ból), és (d) az audit-folyamat dokumentumait digitális aláírással (Documenso). A wedge: **transzparens fix ár, full code-ownership opció** (white-label self-host), és **mély security monitoring** beépítve (a Vanta/Drata csak GRC, nem SIEM).

**Probléma, akit megfizet.**
- 83% enterprise vevő SOC 2-t követel SaaS vendoroktól ([techfundingnews.com](https://techfundingnews.com/10-best-soc-2-compliance-tools-for-scaling-companies-in-2025/), Vanta survey 2025).
- 67% startup szerint a SOC 2 közvetlenül zárt deal-eket; medián deal mérete $120K ([techfundingnews.com](https://techfundingnews.com/10-best-soc-2-compliance-tools-for-scaling-companies-in-2025/)).
- Vanta drága ($15K–20K+/év Series A startupnak ([sacra.com/c/vanta](https://sacra.com/c/vanta/) — ARPU $17–19K)), és csak GRC — külön SIEM (Datadog, Splunk) még $20K+/év.
- Series A-B startup CTO-k akik az első audithez ($25–50K első év, [drata.com cost](https://drata.com/learn/soc-2/cost), [secureframe.com cost](https://secureframe.com/hub/soc-2/audit-cost)) keresnek olcsóbb, transzparensebb, self-hostable alternatívát. Healthcare startupok HIPAA BAA-val.

**Repó bundle és architektúra.**

```
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND (saját Next.js dashboard)                          │
│  - Control library, evidence viewer, audit prep             │
└──────────┬──────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│ getprobo/probo  (MIT) — control framework, vendor mgmt,    │
│ policy templates, risk register                            │
│ + trycompai/comp  (AGPLv3 — CSAK BACKEND!) — 580+ integráció │
│ evidence collection, device agent                          │
└──────────┬──────────────────────────────────────────────────┘
           │ events / log forwarding
┌──────────▼──────────────────────────────────────────────────┐
│ wazuh/wazuh  (GPLv2) — SIEM/XDR, file integrity,           │
│ endpoint monitoring, threat detection, log analysis        │
│ → evidence input a Probo control-okhoz                     │
└──────────┬──────────────────────────────────────────────────┘
           │ audit artifacts → sign
┌──────────▼──────────────────────────────────────────────────┐
│ documenso/documenso  (AGPLv3 Community — KOCKÁZAT!)        │
│ vagy DocuSeal (MIT) — auditor MSAa, BAA, security policy    │
│ aláírás                                                    │
└─────────────────────────────────────────────────────────────┘
```

**Licencanalízis (NAGYON KRITIKUS — itt vannak AGPL csapdák).**

- `getprobo/probo` — **MIT** ✅ ([github.com/getprobo/probo](https://github.com/getprobo/probo))
- `trycompai/comp` — **AGPLv3 + Enterprise license**. ⚠️ AGPL = a network use disclosure. SaaS-resale jogi szürke zóna — Comp AI maga is "open core" modellt fut ([helpnetsecurity.com Comp AI](https://www.helpnetsecurity.com/2026/04/07/comp-ai-open-source-compliance-platform/), [trycomp.ai](https://www.trycomp.ai/)). **Lehetőség 1:** AGPLv3 alatt forkolunk és open-source-oljuk a kódunkat (jogi probléma: forrás-disclosure kötelező SaaS-en is). **Lehetőség 2:** Megveszünk egy commercial licencet a Comp AI-tól (várható $20–50K/év, jogtanácsadóval tisztázni). **Lehetőség 3:** Saját evidence collector írása (3–4 hónap, kerüljük AGPL-t). **Ajánlás: Lehetőség 2 induláshoz, párhuzamosan saját replacementet építeni.**
- `wazuh/wazuh` — **GPLv2** ⚠️. GPL nem AGPL — SaaS-ben futtatható forrásdisclosure nélkül (csak ha a binárist disztribuáljuk vevőnek, akkor disclosure-köteles). ✅ Saját Wazuh manager-t self-host-olunk, az ügyfél kap egy multi-tenant viewert. Wazuh maga commercial managed cloudot is árul, nincs feature gating ([opentechhub.io](https://www.opentechhub.io/wazuh/)).
- `documenso/documenso` — **AGPLv3 Community + Enterprise EE** ⚠️. ([docs.documenso.com licenses](https://docs.documenso.com/users/licenses)). Ugyanaz a probléma, mint Comp AI-nál. **Ajánlás: DocuSeal (MIT) replacement** vagy Documenso enterprise license ($2–10K/év).

**Összesítve:** A bundle 2 AGPL repo-val "non-starter" sok B2B vevőnek ([opencoreventures.com AGPL](https://www.opencoreventures.com/blog/agpl-license-is-a-non-starter-for-most-companies)). **Konkrét lépés MVP-hez: cseréljük Documenso-t DocuSeal-re (MIT), és tárgyaljunk Comp AI-jal kereskedelmi licencről vagy építsünk saját evidence collectort.** Tiszta licencbe így a stack: Probo (MIT) + saját evidence collector + Wazuh self-hosted (GPLv2 OK SaaS-re) + DocuSeal (MIT).

## 2. Miért most

- **SOC 2 mandate robbant:** 83% enterprise vevő SOC 2-t követel; csak 7%-ának van <$1M funding startupnak ([techfundingnews.com](https://techfundingnews.com/10-best-soc-2-compliance-tools-for-scaling-companies-in-2025/)). Hatalmas penetration gap.
- **Vanta árazás felfelé csúszott:** Vanta ARPU $19K/customer (April 2026), a $5K/év Sprinto-szegmenset nyitva hagyják ([sacra.com vanta](https://sacra.com/c/vanta/)).
- **AI compliance robbant a piacon:** EU AI Act August 2, 2026-i deadline ([hklaw.com EU AI Act](https://www.hklaw.com/en/insights/publications/2026/04/us-companies-face-eu-ai-acts-possible-august-2026-compliance-deadline)); új compliance framework (ISO 42001), és a Vanta/Drata csak most kezdi beépíteni.
- **OSS compliance momentum:** Comp AI ($1,200+ GitHub stars), Probo (YC X25 batch, 70 customer pár hónap alatt ([ycombinator.com/companies/probo](https://www.ycombinator.com/companies/probo))) bizonyítják a market validitást.
- **Healthcare digitalizáció:** HIPAA compliance software piac $3.65B (2025) → $9.64B (2035), 10.2% CAGR ([expertmarketresearch.com](https://www.expertmarketresearch.com/reports/healthcare-compliance-software-market)).
- **Tailwind a self-hostable iránti igény:** AI startupok és európai cégek (GDPR + Data Sovereignty) egyre több self-host opciót akarnak.
- **2 éve nem ment volna:** Probo, Comp AI nem léteztek, AI-driven evidence parsing (control mapping) most ért el production minőségbe.

## 3. Piacméret és ARPU

**TAM/SAM/SOM.**
- **TAM:** Compliance automation = $2.8B (2025), ebből SOC 2 tools $850M, várhatóan $2.7B (2028) ([techfundingnews.com](https://techfundingnews.com/10-best-soc-2-compliance-tools-for-scaling-companies-in-2025/)). Global GRC TAM $50–100B.
- **SAM (Series A–B SaaS startup + small healthcare):** ~12K US startup raised Series A/B 2024-2025 + ~3K telehealth/healthcare startup + ~25K Európai SaaS. ICP-számolva ~30K cég × $9K ARPU = **$270M SAM**.
- **SOM (3-5 év):** 1% piacrész = 300 vevő × $9K = **$2.7M ARR**. 3% = $8.1M ARR.

**ARPU tiers.**
| Csomag | Ár | Tartalmaz | Cél vevő |
|--------|------|-----------|---------|
| Starter | $499/hó ($5,988/év) | SOC 2 Type 1, 1 framework, alap evidence | Pre-Series A, 5–15 fő |
| Growth | $999/hó ($11,988/év) | SOC 2 Type 2 + ISO 27001, Wazuh SIEM, 25 integráció | Series A, 15–50 fő |
| Pro | $1,499/hó ($17,988/év) | + HIPAA + GDPR, mély SIEM, BAA | Series A–B, healthcare |
| Enterprise | $2,500+/hó | Egyedi framework (FedRAMP, PCI), self-hosted | Series B+, regulated |

Blended ARPU: **$900/hó ($10,800/év)** — direkt a Vanta $19K alá, Sprinto $5–8K-val versenyez ([brightdefense.com](https://www.brightdefense.com/resources/secureframe-vs-sprinto/)).

**Útvonal.**
- **$100K MRR** = 111 vevő. 18–24 hónap (B2B sales-vezérelt).
- **$1M ARR** = 93 vevő. 24–30 hónap.
- **$10M ARR** = 925 vevő. 4–5 év, kell sales team + auditor partnerprogram.

**Összehasonlító benchmark:** Drata $1 → $100M ARR 3.5 év alatt ([drata.com fy25-momentum](https://drata.com/blog/announcing-fy25-momentum)), Vanta $0 → $300M 5 év alatt ([vanta.com 300M](https://www.vanta.com/resources/vanta-crosses-300m-in-arr-as-growth-accelerates)). Egy OSS-alapú, niche kihívó realistically $10M ARR 4 évre, exit lehetséges (Tugboat Logic → OneTrust akvizíció).

## 4. Konkurenciaelemzés

| Cég | Ár | ARR/Funding | Erősségek | Gyengeségek | Wedge |
|-----|------|---------|-----------|-------------|-------|
| **Vanta** | $7–25K/év ARPU $19K ([sacra.com](https://sacra.com/c/vanta/)) | $300M ARR (Apr 2026), $4.15B val ([siliconangle.com](https://siliconangle.com/2025/07/23/compliance-startup-vanta-valued-4-15b-new-150m-round/)) | Brand, ecosystem, 16K customer | Drágul, GRC-only (nincs SIEM), closed | 50% olcsóbb, beépített SIEM, self-host opció |
| **Drata** | $7.5–15K/év | $100M ARR (Jan 2025) ([drata.com](https://drata.com/blog/announcing-fy25-momentum)), $328M raised, $2B val | UX, audit support | Hasonló pozícionálás Vanta-hoz | Niche-down: AI startup + healthcare HIPAA fókusz |
| **Secureframe** | $7.5K+/év ([sprinto.com](https://sprinto.com/blog/secureframe-pricing/)) | $56M funding, est. $40M ARR | Mid-market advisor, framework szélesség | Vanta árnyékában | Self-host + transzparens ár |
| **Sprinto** | $5–8K/év startup ([sprinto.com](https://sprinto.com/blog/secureframe-pricing/)) | $32M raised | Olcsó, gyors deployment | India-based support, gyengébb US sales | Mély SIEM (Wazuh) integráció |
| **Thoropass** | ~$10–20K/év | $98M funding | Platform + audit one-stop | Drágább, audit-as-a-service nem mindenkinek kell | Modular, audit-only ki-be |
| **Tugboat Logic** | $5–10K bundle in OneTrust | OneTrust acquired 2021 | Enterprise reach | Nem startup-friendly post-acquisition ([sprinto.com](https://sprinto.com/blog/tugboat-logic-review/)) | Modern, startup-focus |
| **Strike Graph** | $10–15K/év | $15M raised | Mid-market | Limited differentiator | Self-host + SIEM |
| **Hyperproof** | $20K+/év enterprise | $40M+ raised | Enterprise GRC depth | Túl enterprise SMB-nek | SMB simplicity |
| **AuditBoard** | $50K+/év enterprise | $11B exit (Hg 2024) | Audit + ESG | Enterprise only | Lower in the market |
| **Scrut** | $5–10K/év | $20M+ funded | India-based, gyors | Limited US presence | US + EU GDPR fókusz |
| **Comp AI** (OSS) | OSS + commercial | YC, 1,200+ stars | OSS, AI-native | Még nem stabil enterprise | "Comp AI hosted by experts" |
| **Probo** (OSS) | OSS + done-for-you | YC X25, 70 customer | OSS, MIT, founder-friendly | Kis méret, kapacitás | Komplementer integráció |

**Wedge összegezve:** A Vanta/Drata középmező túl drága Series A-nak, az olcsó OSS opciók (Comp AI, Probo) nem teljes csomagok. **Pozíció: "Vanta features, Sprinto pricing, with built-in SIEM and self-host option for paranoid AI startups."**

## 5. Go-to-market stratégia

**Első 10 vevő honnan jön.**
1. **3 vevő YC/Techstars hálózatból:** kapcsolat YC alumni Slack csoportokon, Techstars founders, On Deck — direkt warm intro YC W26/S26 batch-en levő, SOC 2-t most kezdő cégekhez.
2. **3 vevő hideg outbound-ból Series A-B startupokra:** Crunchbase + LinkedIn Sales Nav lista, CTO/Security lead, "SOC 2 readiness audit" ingyenes pitch.
3. **2 vevő auditor partnerből:** kapcsolat 5–10 boutique CPA/auditor cég (Prescient, A-LIGN, BARR) — adunk nekik 20% revshare és előminősített leadek.
4. **2 vevő content/SEO-ból:** vertikális blog ("SOC 2 for AI startups", "HIPAA for telehealth MVP") — Comp AI bizonyította, hogy az OSS-friendly content jól skálázódik.

**Pricing & packaging.**
- $499/$999/$1,499/$2,500+ tier.
- **Demo + 30 napos paid pilot** (NEM ingyenes trial — compliance vevő komoly döntés, free trial nem konvertál B2B SaaS-ben Series A szegmensben).
- **Annual contract default, 15% kedvezmény.**
- **Onboarding: $2,500 white-glove** (Vanta $3K+) — beépítjük az első frameworkbe.
- **Auditor partnerprogram:** 20% recurring revshare.

**Disztribúciós csatornák rangsorolva.**
1. **Auditor partnerprogram** (eredet: Vanta GTM playbook, [thegtmnewsletter.substack.com](https://thegtmnewsletter.substack.com/p/deconstructing-vantas-gtm-a-journey)). A SOC 2 auditor a "vendor of trust" — 100 boutique CPA cég US-ban, mindegyik 50–200 startupot szolgál.
2. **Content SEO** (Comp AI playbook): 50+ vertikális landing oldal ("SOC 2 for [vertical]"), "compliance for AI startups", "HIPAA for telehealth MVP". Long-tail SEO konverzál B2B-ben.
3. **YC/Techstars/Accelerator partnerprogramok:** YC Bookface, Techstars perks, OnDeck deals. Vanta YC perk értéke $7K — versenyezni érdemes $5K perkkel.
4. **VC partnerprogramok:** Sequoia Arc, a16z portco companies, 500 Startups portfolio perks. Adni 50% discount portco-knak. (VC-k szeretik, ha portfolioikban olcsó tooling van.)
5. **Hideg outbound:** Apollo + Clay + Smartlead, Series A/B CTO/CISO célzottan.
6. **Iparági Slack/Discord:** SecOps Slack, AICPA member network, CISO Forum, Latitud (latam startup).
7. **Konferenciák:** RSA Conference, SaaStr Annual, BSides, HIMSS (healthcare).
8. **Paid:** LinkedIn Ads (CTO targeting), Google Ads "SOC 2 compliance software" — drága ($300+ CPL) de magas LTV.

**Outbound script (Series A CTO).**

> Subject: 30 napos SOC 2 readiness, 60%-kal olcsóbban mint a Vanta
>
> Hi [Név],
>
> Láttam, hogy a [Cég] most zárta a Series A-t [Investor]-tól — gratulálok. Ha még nem indult el a SOC 2, valószínűleg most kezdtek nyomulni az első enterprise deal-ek.
>
> Mi a [Cég] OSS-alapú, self-hostable compliance platformot építünk Series A startupoknak: SOC 2 Type 2 + ISO 27001 + beépített Wazuh SIEM (amiért külön $20K/évet fizettek volna Datadog-nak), $999/hó. Kódbázis nálatok marad, ha akarjátok self-host.
>
> 15 perces demo? [Calendly link]
>
> — [Név]

**0–12 hónapos roadmap.**
- **M1–M3:** MVP build (Probo fork + saját evidence collector + Wazuh + DocuSeal), 3 design partner ingyen (YC alumni network).
- **M4–M6:** Első 5 fizető vevő $999 tier-en, alap SOC 2 Type 1 workflow, $5K MRR.
- **M7–M9:** Auditor partnerprogram, 2 boutique CPA, $20K MRR.
- **M10–M12:** ISO 27001 + HIPAA framework, paid pilot programok VC perkkel, $50–80K MRR.

## 6. MVP architektúra

**Mit építünk először.**

```
[Next.js dashboard] → [Probo backend (MIT, forkolt)]
                    → [Saját evidence collector (Python/TS,
                       AWS/GCP/GitHub/Okta/Slack OAuth integráció)]
                    → [Wazuh manager (self-hosted, multi-tenant)]
                    → [DocuSeal (MIT, self-hosted) e-signature]
                    → [Stripe billing]
```

**MVP scope:** Csak SOC 2 Type 1 workflow, 15 integráció (AWS, GCP, GitHub, GitLab, Okta, Google Workspace, Microsoft 365, Slack, Jira, Linear, JumpCloud, Rippling, Vanta CSV import migration), 50 alap control (CC1-CC9 SOC 2 TSC), policy templates (10 darab), Wazuh kétféle szerverlogra.

**Hosting/infra.**
- AWS multi-tenant Postgres (RDS) + S3 evidence storage.
- Wazuh manager Kubernetes-en (EKS) — egy manager per tier, tenant izoláció namespace-en.
- Next.js + Vercel frontend.
- Background workers: Temporal.io vagy BullMQ.
- Compliance evidence engine: Python (FastAPI) + integráció connectorok.
- Költségvetés: $800–1,500/hó infra induláskor (Wazuh elviszi a felét).

**Becsült build time.**
- **Solo founder:** 4–6 hónap MVP-ig (komplex stack: integrációk + SIEM + audit dokumentáció).
- **2–3 fős csapat (1 BE security focus, 1 FE, 1 founder):** 3–4 hónap.

**Build vs. buy.**
| Komponens | Döntés | Miért |
|-----------|--------|-------|
| Control framework | **Build on Probo (MIT)** | Bevált, MIT permissive |
| Evidence collector | **Build (saját)** | AGPL Comp AI = jogi probléma |
| SIEM | **Embed Wazuh (GPLv2)** | Iparági standard, OSS, multi-tenant lehetséges |
| E-signature | **Embed DocuSeal (MIT)** | Documenso AGPL-t kerüljük |
| Auth | **Buy (Clerk vagy WorkOS)** | SAML/SSO standard |
| Audit-as-a-service | **Partner** (boutique CPA) | Nem akarunk auditor lenni jogilag |
| LLM (control mapping) | **Buy (Anthropic)** | Saját nem éri meg |

## 7. Kockázatok és moat

**Top 5 kockázat rangsorolva.**

1. **AGPL licenc-csapda Comp AI / Documenso miatt.** Ha későn rosszul választunk, a teljes kódbázis open-source-olási kötelezettség. **Mitigáció:** induljunk Probo (MIT) + saját evidence collector + DocuSeal (MIT)-ből. AGPL csak ha kereskedelmi licencet veszünk.
2. **Vanta lemegy árban / kínál SMB tier-t.** Vanta már most $7K-tól indul ([sacra.com](https://sacra.com/c/vanta/)) — egy "Vanta SMB" $3K/év terméket bármikor kiadhat. **Mitigáció:** moat self-host opción és SIEM bundleon (Vanta-nak nincs SIEM).
3. **Auditor partnerek nem skálázódnak** — boutique CPA-k egyszerre csak 5–10 platformot tudnak támogatni. **Mitigáció:** "Big 4 alternatív" partnerek (Schellman, A-LIGN) + saját auditor partnerprogram tréninggel.
4. **AI-generated compliance evidence regulatóriumi probléma** — ha AI hallucinálja a control evidence-et, az audit invalidálható. **Mitigáció:** minden AI output human-in-the-loop, audit trail, "AI suggested, human approved" workflow.
5. **Security breach a saját platformunkon** — compliance platform breach katasztrófa (Solorigate-szerű). **Mitigáció:** mi magunk SOC 2 Type 2 + ISO 27001 + pen-test naponta + bug bounty.

**Moat építés.**
- **Auditor hálózat:** 50–100 boutique CPA partner formális partnerprogramban — strukturális moat, mint Vanta-nál.
- **Framework breadth:** SOC 2 → ISO 27001 → HIPAA → GDPR → PCI → FedRAMP Low → ISO 42001 (AI). Minden új framework 2–3 hónap, kódolt switching cost.
- **Evidence dataset:** millió evidence collection event → AI-driven control mapping pontosabb idővel. Vanta-nak van, OSS bundlernek építeni kell.
- **Self-host + sovereignty:** unique pozíció: AI startupok és európai szabályozott vevők (banking, defense) self-host-olnak. Vanta/Drata nem ad ilyet.
- **Brand a "transzparens OSS" terében:** Comp AI/Probo bizonyítja, hogy van rezonancia.

**Failure modes hasonló cégeknél.**
- **Tugboat Logic** — túl korán enterprise, OneTrust felvásárolta, eltűnt startup market-en ([sprinto.com](https://sprinto.com/blog/tugboat-logic-review/)).
- **Hyperproof** — moved upmarket, elveszítette SMB.
- **Korai OSS-compliance projektek** (e.g. monkey365, openSCAP): great tech, no GTM.

## 8. Első 90 nap akcióterv

**Hét 1–2: Validáció + jogi.**
- 20 cold interjú Series A/B CTO-val: "milyen compliance toolt használsz, mi a legrosszabb dolog?"
- Jogász meghívás: AGPL Comp AI/Documenso vs. saját evidence collector döntés véglegesítése.
- Probo, Wazuh, DocuSeal forkolása, helyi setup.

**Hét 3–6: MVP v0.1.**
- 5 integráció (AWS, GitHub, Okta, Google Workspace, Slack) saját connectorral.
- Probo control library beépítése, alap SOC 2 TSC mapping.
- Wazuh self-hosted manager 1 tenant-tal.
- Audit evidence collector → S3 → Probo-ban hivatkozás.

**Hét 7–8: Design partnerek.**
- 3 ingyenes design partner (YC W26 batch-ből vagy LinkedIn outreach Series A CTO-knak).
- Egy elérni dokumentált SOC 2 readiness assessment.

**Hét 9–10: Második design partner kohort + auditor outreach.**
- 5 boutique CPA megkeresése (BARR, Prescient, A-LIGN, KirkpatrickPrice, Linford).
- HIPAA framework MVP-je.

**Hét 11–12: Első fizetők.**
- Stripe + paid pilot $999/hó.
- Cél: 3 fizető vevő ($3K MRR) hét 12-re.
- Content: 5 SEO blogposzt ("SOC 2 for [AI/healthcare/B2B SaaS] startups").

**90. nap KPI:** 3 fizető vevő, $3K MRR, 5 integráció prod-ban, 2 framework (SOC 2 Type 1 + HIPAA gap analysis), 1 auditor partner verbalis, 5 SEO oldal, AGPL probléma véglegesen megoldva.

---

# Összegző döntési mátrix

| Tényező | Niche 1 (Voice) | Niche 2 (Compliance) |
|---------|-----------------|----------------------|
| MVP idő | 6–8 hét | 12–16 hét |
| Vevőszerzés sebessége | Gyors (SMB, $299 impulzív) | Lassú (B2B sales, $1K+ deliberált) |
| ARPU | $5,400/év | $10,800/év |
| Sales komplexitás | Önkiszolgáló + agency | High-touch, demo-vezérelt |
| Verseny intenzitása | Magas (sok játékos), de nincs SMB-vertikális dominator | Magas (Vanta/Drata), nehezebb leszorítani |
| Licenc-tisztaság | Tiszta (csak MIT/BSD/Apache) | Csapdás (Comp AI/Documenso AGPL kerülni kell) |
| Moat lehetőség | PMS-integrációk, vertikális playbook | Auditor partner, framework breadth, self-host |
| Tőkeszükséglet | $50–100K bootstrap-bar | $300–500K seed kell sales-hez |
| Magyar founder előny | Európai vásárlók GDPR-priority, multi-language | EU AI Act tudás, self-host adat-szuverenitás |

**Personal recommendation:** Ha solo founder és gyors revenue kell — **Niche 1**. Ha alapítócsapat van és nagyobb exit-potenciálra mész (Vanta-szerű 5–10 év, $50M+) — **Niche 2**.

---

## Források

**Niche 1 (Voice):**
- [Vapi pricing](https://vapi.ai/pricing), [Vapi $20M Series A](https://vapi.ai/blog/vapi-secures-20m-to-start-the-voice-revolution-2)
- [Retell AI pricing $50M ARR](https://www.retellai.com/blog/ai-voice-agent-pricing-full-cost-breakdown-platform-comparison-roi-analysis), [Retell pricing page](https://www.retellai.com/pricing)
- [Bland AI pricing](https://www.bland.ai/pricing), [Bland $40M Series B](https://www.cloudtalk.io/blog/bland-ai-pricing/)
- [Synthflow](https://synthflow.ai/), [Synthflow voice cost](https://synthflow.ai/blog/voice-ai-cost)
- [Goodcall pricing](https://www.goodcall.com/pricing)
- [Smith.ai AI Receptionist](https://smith.ai/pricing/ai-receptionist), [Ruby Receptionists pricing](https://www.ruby.com/plans-and-pricing/)
- [Air.ai FTC settlement](https://www.ftc.gov/news-events/news/press-releases/2025/08/ftc-sues-stop-air-ai-using-deceptive-claims-about-business-growth-earnings-potential-refund)
- [Missed calls revenue impact](https://www.getaira.io/blog/missed-business-calls-statistics), [PCN missed call study](https://pcnanswers.com/missed-call-revenue-study/), [Contractors lost revenue](https://www.callbirdai.com/blog-contractors-lose-money-missed-calls)
- [AI voice agents market size](https://www.grandviewresearch.com/industry-analysis/ai-voice-agents-market-report), [Conversational AI market](https://www.fortunebusinessinsights.com/conversational-ai-market-109850), [Voice AI funding 8x](https://www.pymnts.com/artificial-intelligence-2/2025/voice-ai-funding-surges-8x-as-businesses-humanize-chatbots/)
- [SBA 36M small businesses](https://advocacy.sba.gov/2025/06/30/new-advocacy-report-shows-the-number-of-small-businesses-in-the-u-s-exceeds-36-million/), [Plumbers count IBISWorld](https://www.ibisworld.com/united-states/number-of-businesses/plumbers/1946/)
- [LiveKit GitHub](https://github.com/livekit/agents), [Pipecat GitHub](https://github.com/pipecat-ai/pipecat), [Dograh GitHub](https://github.com/dograh-hq/dograh), [Chatwoot license](https://www.chatwoot.com/terms-of-service/)
- [Vapi white-label / agency reseller](https://www.trillet.ai/blogs/vapi-alternative-for-agencies)

**Niche 2 (Compliance):**
- [Vanta ARR $300M](https://www.vanta.com/resources/vanta-crosses-300m-in-arr-as-growth-accelerates), [Vanta valuation $4.15B](https://siliconangle.com/2025/07/23/compliance-startup-vanta-valued-4-15b-new-150m-round/), [Vanta GTM playbook](https://thegtmnewsletter.substack.com/p/deconstructing-vantas-gtm-a-journey), [Vanta Sacra](https://sacra.com/c/vanta/)
- [Drata $100M ARR](https://drata.com/blog/announcing-fy25-momentum), [Drata Sacra](https://sacra.com/c/drata/)
- [Secureframe vs Sprinto pricing](https://www.brightdefense.com/resources/secureframe-vs-sprinto/), [Sprinto pricing](https://sprinto.com/blog/secureframe-pricing/)
- [SOC 2 audit cost Drata](https://drata.com/learn/soc-2/cost), [Secureframe cost](https://secureframe.com/hub/soc-2/audit-cost), [Comp AI SOC 2 cost](https://trycomp.ai/soc-2-cost-breakdown)
- [SOC 2 market data techfundingnews](https://techfundingnews.com/10-best-soc-2-compliance-tools-for-scaling-companies-in-2025/)
- [Healthcare compliance software market](https://www.expertmarketresearch.com/reports/healthcare-compliance-software-market)
- [EU AI Act deadline](https://www.hklaw.com/en/insights/publications/2026/04/us-companies-face-eu-ai-acts-possible-august-2026-compliance-deadline)
- [Probo YC](https://www.ycombinator.com/companies/probo), [Probo GitHub](https://github.com/getprobo/probo)
- [Comp AI launch](https://www.helpnetsecurity.com/2026/04/07/comp-ai-open-source-compliance-platform/), [Comp AI GitHub](https://github.com/trycompai/comp), [Trycomp.ai](https://www.trycomp.ai/)
- [Wazuh GitHub](https://github.com/wazuh/wazuh), [Wazuh OSS analysis](https://www.opentechhub.io/wazuh/)
- [Documenso licenses](https://docs.documenso.com/users/licenses), [AGPL non-starter analysis](https://www.opencoreventures.com/blog/agpl-license-is-a-non-starter-for-most-companies)
- [Tugboat Logic OneTrust acquired](https://sprinto.com/blog/tugboat-logic-review/)
