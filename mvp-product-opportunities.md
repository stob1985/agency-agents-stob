# MVP-szintű termék lehetőségek magyar solo founder számára

**Készült:** 2026-05-12
**Cél:** 10-15 darab, 2-6 hét alatt solo megépíthető micro-SaaS / digitális termék ötlet, amely 50-500 ügyféllel profitábilis.

**Alapelvek (mindenre érvényes):**
- Egy codebase, nincs multi-tenant komplexitás, nincs SSO/audit log az induláskor
- Első ügyfél <30 napon belül
- Pricing: $19-99/hó VAGY $5-49 one-time VAGY $200-500 LTD
- Nincs HIPAA/SOC2/heavy GDPR
- Solo karbantartható örökre

---

## 1. ThumbForge - YouTube thumbnail A/B variant generator

**Kategória:** A) AI wrapper micro-SaaS
**Profil:** Replicate (flux-dev) + Next.js wrapper, niche UI YouTube creatoroknak

**Pitch:** Egy YouTube thumbnail-t feltöltve 8 variánst generál (arckifejezés, szöveg, szín-ütés) és CTR-előrejelzést ad heuristikákból.

**Mit csinál:**
- User feltölt egy meglévő thumbnailt vagy szöveget ad
- Replicate flux-dev + GPT-4o-mini variánst generál (más facial expression, más text overlay, más color contrast)
- Heuristic CTR scoring (contrast ratio, face area, text readability) - nem ML, csak színészlelés képletek
- Bulk export PSD/PNG, gallery hub a régi tesztekkel
- Történet (mit teszteltél, mi nyert)

**Célközönség:** MrBeast-wannabe YouTube creatorok 10k-500k subscriberrel, akik tudják hogy a thumbnail a kulcs. ~200-400k globális, X-en és Reddit r/NewTubers, r/PartneredYoutube fórumon találhatók. Twitter/X "YouTube Shorts" hashtag napi 5-10 ezer aktív poszt.

**Pénz:** $29/hó (50 thumbnail/hó) vagy $79/hó (unlimited) - Stripe
**Tech stack:** Next.js 14 (App Router) + Vercel + Supabase (auth, storage) + Replicate API
**Build time:** 80-100 óra (~3 hét solo)
**Distribution:** X "build in public" + reply guy taktika YouTube creator threadekben, ProductHunt launch, Reddit r/NewTubers, kapcsolat egy közepes YT csatornával affiliate-re
**Validation:** Thumbnail Test (thumbnailtest.com) ~$15k MRR-en, 1of10 (1of10.com) - bizonyítják a piacot. Replicate-en flux modellek napi több millió hívás.
**12 hó ARR:** $30-60k ARR realisztikus (100-150 fizető user @$29)
**Legnagyobb kockázat:** YouTube Studio beépíti natívan az A/B thumbnail tesztet (már részlegesen elérhető), így a "ténylegesen tesztelés" funkció leértékelődik. Mitigáció: legyen a fókusz a *kreatív variációkon*, nem a teszten.

---

## 2. CalmTab - Chrome extension distraction blocker promptokkal

**Kategória:** B) Chrome extension paid
**Profil:** $19 LTD Chrome extension

**Pitch:** Minden új tab egy "miért nyitod most meg?" promptot kér + napi limit + analytics.

**Mit csinál:**
- New Tab override, kötelező 1-mondatos célmegadás mielőtt a böngészés folytatódhat
- Heti report PDF-ben mire ment az idő
- Site blacklist időablakkal (Reddit max 20 perc/nap)
- Lokálisan tárolja az adatokat (chrome.storage), nincs backend
- Egyszer fizetés - lifetime license key

**Célközönség:** ADHD-s knowledge workerek, deep work hívők. r/ADHD (1.8M tag), r/productivity (2M), r/getdisciplined. X "deep work" community.
**Pénz:** $19 lifetime via ExtensionPay vagy LemonSqueezy
**Tech stack:** Vanilla JS + manifest v3 + ExtensionPay licensing
**Build time:** 30-50 óra (~1.5 hét)
**Distribution:** ProductHunt, r/ADHD, r/productivity, X "1 hour build" thread, IndieHackers showcase
**Validation:** CSS Scan ($100k+ revenue), Easy Folders ($3.7k MRR @ChatGPT folder ext), Helper-AI ($3.5k 2 hónap alatt). One Sec app (iOS) milliós letöltéssel.
**12 hó ARR:** $15-30k (~1000-1500 lifetime eladás)
**Legnagyobb kockázat:** Chrome Web Store policy változás (manifest v4) megöli vagy újraírást követel. Mitigáció: kódbázis tiszta, gyorsan portolható.

---

## 3. RegexBuddy.ai - Természetes nyelvű regex generátor + tester

**Kategória:** A/C) AI wrapper, no-backend web tool
**Profil:** Frontend + GPT-4o-mini API call, Stripe

**Pitch:** "Find email addresses but not gmail.com" -> generálja a regexet + magyaráz + tesztel egy box-ban azonnal.

**Mit csinál:**
- Plain English -> regex via Claude Haiku API (olcsó)
- Live testing playground (paste test text, highlight matches)
- Explain mode - lépésről lépésre mit csinál a kifejezés
- Cheatsheet, history (localStorage), PCRE/JS/Python flavor switch
- Export gist link

**Célközönség:** Junior-mid devek, data analystok, sysadminok. ~5M dev globálisan használ regexet rendszeresen. r/regex (75k), r/learnprogramming, X devtwitter.
**Pénz:** Freemium - 10 ingyenes/nap, $7/hó pro vagy $39 lifetime via LemonSqueezy
**Tech stack:** Astro/SvelteKit static + Cloudflare Worker az AI proxyhoz + LemonSqueezy
**Build time:** 40-60 óra (~2 hét)
**Distribution:** HackerNews Show HN, r/programming, r/regex, dev.to cikk, X devtwitter
**Validation:** Regex101 (free, óriás traffic), AutoRegex.xyz mutatja a keresletet. ChatGPT regex query-k százmilliósak.
**12 hó ARR:** $8-20k (sok organikus SEO, alacsony LTV de magas volume)
**Legnagyobb kockázat:** A user simán ChatGPT-be írja. Mitigáció: a *tester+explainer combo* az érték, nem a generálás maga.

---

## 4. PodcastPullQuotes - Audio -> social media quote képek

**Kategória:** A) AI wrapper micro-SaaS
**Profil:** Whisper API + Replicate (SDXL) wrapper podcasterekre

**Pitch:** Tölts fel egy podcast epizódot, kapsz 10 idézhető pull-quote-ot kép formátumban Instagram/X-re.

**Mit csinál:**
- MP3/MP4 upload (max 2GB), Whisper transcribe
- GPT-4o-mini kiválasztja a top 10 "tweetable" idézetet (engagement-prediktor prompt)
- Auto-generate quote képek (3 template választható) brand színekkel
- Bulk download ZIP, optional auto-post Buffer integrációval (v2)
- Egyperces "clip" video is - vertikálisan vágott waveform animációval

**Célközönség:** Solo podcasterek 1-50k hallgatóval. Listen Notes szerint ~3M aktív podcast. r/podcasting (350k), Podcast Movement community.
**Pénz:** $19/hó (4 epizód/hó) / $49/hó (unlimited) Stripe
**Tech stack:** Next.js + Supabase Storage + AWS S3 + OpenAI Whisper + Replicate + ffmpeg.wasm vagy serverless ffmpeg
**Build time:** 100-140 óra (~4 hét) - a media pipeline a legtöbb idő
**Distribution:** r/podcasting, X #podernfamily, ProductHunt, podcast hosting partnership (Transistor, Buzzsprout community)
**Validation:** Castmagic ($30k+ MRR), Capsho, Riverside clips. Bizonyítottan zsíros piac.
**12 hó ARR:** $25-50k
**Legnagyobb kockázat:** Castmagic és Riverside már bevett brandek - kell egy keskeny "csak quotes" pozicionálás vagy árban alulvágni.

---

## 5. ColorPaletteHQ - PDF/Image -> brand palette + Tailwind config

**Kategória:** C) No-backend web tool
**Profil:** Csak frontend, fájl helyben dolgozódik

**Pitch:** Drag-drop egy PDF brand guide-ot vagy logo-t, kiköpi a Tailwind/CSS/Figma palette JSON-t.

**Mit csinál:**
- Client-side image/PDF parsing (pdf.js + Canvas)
- K-means dominant color extraction in browser
- Auto-generate 50-900 shade scale (mint a Tailwind)
- Export: Tailwind config, CSS variables, Figma tokens JSON, SCSS map
- "Save to library" $9 Pro tier (Supabase backend opcionális)

**Célközönség:** Frontend devek, designerek, agency-k. ~10M frontend dev globálisan. r/webdev (1.6M), r/css, X frontend Twitter, Designer News.
**Pénz:** $19 lifetime via LemonSqueezy (Pro library opció $4/hó)
**Tech stack:** Pure Vite + React + pdf.js + tinycolor - hostolható Cloudflare Pages-en ingyen
**Build time:** 25-40 óra (~1 hét)
**Distribution:** dev.to "I built X", r/webdev, ProductHunt, X frontend, Smashing Magazine outreach
**Validation:** Coolors.co (több millió user), Realtime Colors. PDF processing helyben - PSPDFKit jelzi a keresletet.
**12 hó ARR:** $5-12k (~500 LTD)
**Legnagyobb kockázat:** Nagyon olcsó, kell tömeg. Mitigáció: SEO-fókusz "Tailwind palette generator from image"

---

## 6. MicroSaaSDirectory.io - Acquisition-ready micro SaaS directory

**Kategória:** D) Niche directory paid listings
**Profil:** Eladók fizetnek listingért, vevők böngésznek

**Pitch:** TinyAcquisitions/MicroAcquire alternatíva - kifejezetten $1k-100k ARR-es micro-SaaS deal-ek listája, paid listing $79/db.

**Mit csinál:**
- Listing form: revenue, tech stack, time to maintain, asking price
- Filtering: kategória, ARR sáv, ár
- Verified badge (manual review) +$50
- Lead form közvetlen üzenetküldéshez (no escrow)
- Newsletter (heti top 10 új listing) - 20k subscriber realisztikus 12 hó alatt

**Célközönség:** 2 oldal - eladók (10k+ micro-SaaS van), vevők (indie hackerek, búvópatak alapok). X "build in public" community ~50k, r/SaaS (200k), IndieHackers.
**Pénz:** $79/listing/30 nap + $199 "featured" + $5/hó newsletter sponsor slot Stripe
**Tech stack:** Next.js + Supabase + Resend (newsletter) + Stripe
**Build time:** 60-80 óra (~2 hét)
**Distribution:** Twist build-in-public posts, ProductHunt, IndieHackers Milestones, X reply guy MicroAcquire/Acquire.com poszt alatt
**Validation:** MicroAcquire (most Acquire.com) felvásárolt, TinyAcquisitions DirStarter ($5k MRR), Flippa nyilvánvalóan dolgozik a téren.
**12 hó ARR:** $15-40k (kritikus: 6 hónapos seeding ingyen listingekkel)
**Legnagyobb kockázat:** Cold start probléma (két oldalas market). Mitigáció: első 100 listing manuálisan scrape-elve + ingyen, csak utána paid.

---

## 7. NotionShipKit - 12-template bundle "Ship Your SaaS"-hez

**Kategória:** E) Notion template pack
**Profil:** One-time $49 digital bundle

**Pitch:** Egy bundle Notion template - SaaS launch checklist, content calendar, customer research DB, pricing tester, runway calculator - all 12 db egyben.

**Mit csinál:**
- Notion workspace teljes setup
- 12 inter-connected template (relations, formulas)
- Walkthrough video minden templatehez (Loom)
- Discord access (community) lifetime
- Évi 1 frissítés

**Célközönség:** Indie hackerek, SaaS solopreneurok. ~200k aktív indie SaaS founder X-en + IndieHackers.
**Pénz:** $49 one-time Gumroad (PPP enabled)
**Tech stack:** Csak Notion + Gumroad - nincs kód
**Build time:** 40-60 óra (~1.5 hét, csak template építés)
**Distribution:** X build-in-public, ProductHunt, Notion Templates by Notion (official marketplace), IndieHackers, sub-reddit r/Notion (400k)
**Validation:** Easlo (Notion templates, milliós bevétel), Marie Poulin templates, Thomas Frank. Gumroad-on top Notion seller-ek $5-20k/hó.
**12 hó ARR:** $10-25k (mostly organic via X + SEO)
**Legnagyobb kockázat:** Notion AI / hivatalos template-ek kiszorítják. Mitigáció: kuráció + community a value, nem maga a template.

---

## 8. SitemapToBlog - API endpoint sitemap -> blog post outline

**Kategória:** F) API-as-a-product
**Profil:** Egy specifikus API endpoint, devek hívják

**Pitch:** POST egy URL-t, visszakapsz egy versenytárs-blog outline + topic gap analysist JSON-ben. $0.05/hívás.

**Mit csinál:**
- /analyze endpoint: input URL -> crawl sitemap -> extract titles -> GPT cluster + missing topics
- API key auth, dashboard usage analytics
- Stripe metered billing (pay-as-you-go)
- 100 free calls/hó
- OpenAPI spec + Python/JS SDK

**Célközönség:** SEO toolok fejlesztői, agency-k automation-ben, devek akik SEO-tooljaikba építenek. ~50k SEO dev/agency X-en + Twitter "SEOTwitter".
**Pénz:** $0.05/call metered Stripe + $49/hó "team" 2000 call-os flat
**Tech stack:** Cloudflare Workers + KV + GPT-4o-mini + Stripe metered API
**Build time:** 50-70 óra (~2 hét)
**Distribution:** RapidAPI marketplace, IndieHackers, X SEO twitter, Dev.to "I built an API", Apify community
**Validation:** Ahrefs API, DataForSEO ($5M+ ARR), Serpapi. API-as-a-product proven model.
**12 hó ARR:** $8-20k (devek lassan vásárolnak, de stickyk)
**Legnagyobb kockázat:** Niche - kérdés mennyi a TAM. Mitigáció: kezdetben "kompetitor content gap" pozicionálás konkrét agency-knek.

---

## 9. PitchDeckPDF - Founder pitch deck PDF generator from Markdown

**Kategória:** G) PDF generator B2B
**Profil:** Speciális PDF gen pre-seed founderknek

**Pitch:** Írd meg az MD-t (problem, solution, traction, team, ask), kapsz 10-template közül választva profi PDF investor decket.

**Mit csinál:**
- Markdown editor + 10 deck template (YC, a16z style stb.)
- Auto-pagination, charts (Mermaid renderer)
- Investor share link with view analytics (ki és mennyit nézett mit)
- Export PDF + PowerPoint
- $29 single deck or $99/évre unlimited

**Célközönség:** Pre-seed/seed founderek - ~50k aktív pitch-elő startup founder globálisan évente. AngelList, ProductHunt founders, X "indie startup".
**Pénz:** $29 per deck egyszer + $99/év unlimited Stripe
**Tech stack:** Next.js + Puppeteer (PDF render) + Supabase + Stripe
**Build time:** 60-90 óra (~2.5 hét)
**Distribution:** Founders Friday newsletters, X startup twitter, IndieHackers, YC Hacker News, accelerator email outreach (manuális)
**Validation:** Pitch.com (több millió ARR), Beautiful.ai. Egyszerűbb verzió mint Pitch.
**12 hó ARR:** $15-30k
**Legnagyobb kockázat:** Pitch.com és Canva ingyen verziók. Mitigáció: "no design skills needed, just write" pozicionálás + investor view tracking mint differentiator.

---

## 10. RemoteRustJobs - Job board csak Rust dev pozíciókra

**Kategória:** H) Job board narrow niche
**Profil:** Paid listings, single niche

**Pitch:** Csak Rust pozíciók (vagy alternatíva: csak Solana, csak ML infra) - $99/listing/30 nap.

**Mit csinál:**
- Submit form, manual review (anti-spam), pay-to-post
- Filter: remote-only, salary visible, sponsorship
- RSS feed, Twitter auto-post
- Talent profile oldal jelölteknek (ingyen) - 2-sided market seed
- Heti newsletter 500-2000 subscriberhez

**Célközönség:** Rust devek (~200k globálisan), companies hiring Rust (Solana, blockchain, embedded). r/rust (300k), This Week in Rust newsletter, Rust Twitter.
**Pénz:** $99/listing/30 nap + $299 featured Stripe
**Tech stack:** Astro + Supabase + Resend - egyszerű
**Build time:** 30-50 óra (~1.5 hét)
**Distribution:** r/rust, This Week in Rust submissions, X RustLang community, HackerNews, Rust conferences
**Validation:** RealWorkFromAnywhere ($5k MRR), RustJobs.dev exists, CryptoJobsList. Niche job boards working.
**12 hó ARR:** $6-15k (lassú indulás, organic growth)
**Legnagyobb kockázat:** Volume - Rust kis piac. Mitigáció: válassz forrón növő nyelvet (Bun, Zig, Mojo) vagy AI/ML infra niche-t Rust helyett.

---

## 11. EtsyProfitDash - Etsy seller profit tracker mini-tool

**Kategória:** I) Workflow automatizáló konkrét pain pointra
**Profil:** Lightweight web app Etsy sellerekkel

**Pitch:** Csatlakoztasd az Etsy fiókod + Printful, megkapod a *valódi* profit/listing számot, nem csak revenue-t.

**Mit csinál:**
- Etsy API OAuth + Printful/Printify cost API
- Auto-számolja: revenue - Etsy fees - shipping - POD cost - VAT = net profit
- Listing-by-listing profitability ranking
- "Kill list" - veszteséges listing-eket javasol leszedni
- CSV export bookkeepingnek

**Célközönség:** POD Etsy sellerek (1-10k éves bevétel), ~3M Etsy seller. r/Etsy (700k), r/EtsySellers (180k), Etsy Facebook groups.
**Pénz:** $19/hó vagy $149/év Stripe
**Tech stack:** Next.js + Supabase + Etsy API + Printful API
**Build time:** 70-100 óra (~3 hét, OAuth és reconciliation munkás)
**Distribution:** r/Etsy, r/EtsySellers, Etsy seller Facebook groups (több 100k tag), YouTube collab Etsy YouTuberekkel
**Validation:** ProfitTree, EverBee ($mUSD revenue), Alura. Bizonyítottan pénzes piac.
**12 hó ARR:** $20-50k (Etsy sellers szeretnek toolt fizetni)
**Legnagyobb kockázat:** EverBee/Alura dominálja - kell egy keskeny insight ("profit, nem revenue"). Mitigáció: 100%-os fókusz profitra, ne SEO/research-re.

---

## 12. AltTextBatch - Figma plugin tömeges alt-text generálás AI-val

**Kategória:** B/A) Figma plugin + AI
**Profil:** Figma plugin paid tier

**Pitch:** Egy Figma fileben minden képhez GPT-4o-vision generál alt-text-et tömegesen + accessibility audit.

**Mit csinál:**
- Plugin scan: minden image/icon component
- GPT-4o vision API call -> alt text suggestion
- Bulk apply, edit, regenerate
- Accessibility report (contrast, missing alt, etc.) export PDF
- Free: 5 image/file; Pro $9/hó unlimited

**Célközönség:** Figma designerek a11y-tudatos cégeknél. ~10M Figma user, ~500k pro designer. Figma Community, DesignerNews, X UX twitter.
**Pénz:** $9/hó vagy $79 LTD via dedicated payment page (Polar.sh vagy LemonSqueezy)
**Tech stack:** Figma Plugin API (TypeScript) + Cloudflare Worker OpenAI proxy
**Build time:** 30-50 óra (~1.5 hét)
**Distribution:** Figma Community plugin page (organic), X UX twitter, DesignerNews, Smashing Magazine
**Validation:** Több Figma plugin keres $1-5k MRR-t (Easy Folders pattern). A11y compliance growing market.
**12 hó ARR:** $5-15k
**Legnagyobb kockázat:** Figma natívan integrálja az AI alt-textet. Mitigáció: bulk + audit kombináció - Figma valószínűleg csak single-itemes.

---

## 13. KuruzslóEU - EU VAT OSS one-stop bookkeeping export indie sellerseknek (MAGYAR/CEE)

**Kategória:** Bonus #1 - magyar/CEE piac
**Profil:** EU VAT automation

**Pitch:** Stripe + LemonSqueezy + Gumroad bevételeket EU VAT OSS-compliant havi reportba alakít magyar/szlovák/cseh KKV-knak.

**Mit csinál:**
- Connect Stripe/LemonSqueezy/Gumroad/Paddle API
- Customer country detect + reverse-charge B2B/B2C logika
- OSS quarterly report PDF + CSV (NAV/SK/CZ formátum)
- Invoice ID mapping
- Magyar nyelv + angol UI

**Célközönség:** Magyar/szlovák/cseh indie hackerek, digitális termékárusítók akik EU-ba adnak el. ~5-10k aktív magyar digitális vállalkozó. SaaSHungary FB group, Digitális Vállalkozók HU, X HU dev community.
**Pénz:** 9 990 Ft/hó (~$28/hó) vagy 99 000 Ft/év Stripe + Barion
**Tech stack:** Next.js + Supabase + Stripe Connect + jelek API-i
**Build time:** 100-140 óra (~4 hét) - country tax logic kihívás
**Distribution:** HUP.hu, Digitális Tőzsér (Pásztor Eszter community), magyar indie hacker FB groupok, X HU buildinpublic
**Validation:** Quaderno, Octobat, Sphere. EU VAT compliance fájdalom igazolt - de magyar nyelvű alternatíva 0 db.
**12 hó ARR:** $8-20k (kis piac, de magas pain point + low competition lokálisan)
**Legnagyobb kockázat:** Stripe Tax / LemonSqueezy MoR átveszi (LS már Merchant of Record). Mitigáció: fókusz a *not-MoR* platformokra (Stripe direct, Gumroad).

---

## 14. SzámlaCheck.hu - NAV Online Számla "kapott számlák" rendszerező KKV-nak (MAGYAR)

**Kategória:** Bonus #2 - magyar/CEE piac
**Profil:** Magyar mikro-SaaS NAV API-ra

**Pitch:** Csatlakoztasd a NAV Online Számla kliensed, kapj havi dashboard-ot a beszállítóidról + "fizetés esedékesség" emlékeztetőket.

**Mit csinál:**
- NAV Online Számla API (XML 3.0) integration - "kapott számlák" lekérése
- Beszállítónkénti kategorizálás, AI alapú ledger kódolás
- Email reminder esedékes számlákról
- Excel export könyvelőnek
- Anomália detektálás (szokatlan összeg, új beszállító)

**Célközönség:** Magyar KKV-k 1-20 fős, akik nem akarnak teljes ERP-t. ~300-400k mikrovállalkozás Magyarországon. KKV csoportok FB-on, könyvelő network.
**Pénz:** 14 900 Ft/hó (~$42/hó) + 4 900 Ft Setup, Barion / Stripe HU
**Tech stack:** Next.js + Supabase + NAV WS API XML klient + Magyar lokalizáció
**Build time:** 120-160 óra (~5 hét - NAV API komplex)
**Distribution:** Könyvelő partnerek (commission), HUP, KKV FB csoportok, magyar LinkedIn KKV szegmens
**Validation:** Billingo, számlázz.hu, Számla.eu - nagyok kibocsátáson dolgoznak, de a *kapott* oldal nem fókuszuk. Hiánypótló.
**12 hó ARR:** $15-30k (B2B HU, sticky de lassú sales cycle)
**Legnagyobb kockázat:** Billingo bővít. NAV API változás (XML 4.0). Mitigáció: legyél fókuszban: csak inbound oldal, ne építs számlakibocsátást.

---

## 15. MagyarPromptbiblia - Magyar nyelvű GPT prompt-pack KKV-knak (MAGYAR)

**Kategória:** Bonus #3 - magyar/CEE piac + E) template pack
**Profil:** One-time digital download magyar nyelven

**Pitch:** 200 magyar nyelvre optimalizált, KKV-feladatra szabott GPT/Claude prompt (állásinterjú leírás, Facebook poszt, ügyfél email, NAV-levél magyarázat).

**Mit csinál:**
- 200 magyar prompt szabás szerint kategorizálva (HR, marketing, jog, könyvelés, ügyfélszolgálat)
- Notion database formátum
- 30 perces magyar nyelvű video tutorial
- Heti 5 új prompt update 1 évig (Discord access)
- B2B agency licensz +5x ár

**Célközönség:** Magyar KKV-k, asszisztensek, marketingesek - akik még nem komfortosak az AI-jal. ~50-100k aktív magyar AI-tudatos KKV felhasználó. AI Magyarországon FB group, Prompt Hungary, magyar LinkedIn.
**Pénz:** 14 990 Ft (~$42) Gumroad + Barion. Agency licensz 79 900 Ft.
**Tech stack:** Csak Notion + Gumroad + Discord. Zero kód.
**Build time:** 30-50 óra (~1.5 hét, főleg content írás)
**Distribution:** Magyar AI-fókuszú LinkedIn influencerek (commission), HUP, FB AI csoportok, magyar YouTuber collab (Filevine, Bagi Iván Ottó stb.)
**Validation:** Angol prompt packek a Gumroadon $50-150k bevétellel (PromptBase, AI Prompt Packs). Magyar nyelven 0 db verseny.
**12 hó ARR:** $8-15k (lifetime, alacsony churn)
**Legnagyobb kockázat:** Open-source magyar promptlisták (GitHub) ingyen. Mitigáció: a Discord community + frissítések a value, ne a 200 prompt egyszer.

---

# Összefoglaló prioritás-mátrix

| # | Termék | Build idő | 12hó ARR | Effort/Profit | Top? |
|---|--------|-----------|----------|---------------|------|
| 1 | ThumbForge | 3 hét | $30-60k | KIVÁLÓ | TOP3 |
| 2 | CalmTab | 1.5 hét | $15-30k | KIVÁLÓ | TOP3 |
| 3 | RegexBuddy.ai | 2 hét | $8-20k | jó | |
| 4 | PodcastPullQuotes | 4 hét | $25-50k | jó | |
| 5 | ColorPaletteHQ | 1 hét | $5-12k | átlagos | |
| 6 | MicroSaaSDirectory | 2 hét | $15-40k | KIVÁLÓ | TOP3 |
| 7 | NotionShipKit | 1.5 hét | $10-25k | jó | |
| 8 | SitemapToBlog API | 2 hét | $8-20k | átlagos | |
| 9 | PitchDeckPDF | 2.5 hét | $15-30k | jó | |
| 10 | RemoteRustJobs | 1.5 hét | $6-15k | átlagos | |
| 11 | EtsyProfitDash | 3 hét | $20-50k | jó | |
| 12 | AltTextBatch Figma | 1.5 hét | $5-15k | átlagos | |
| 13 | KuruzslóEU (HU) | 4 hét | $8-20k | átlagos | |
| 14 | SzámlaCheck.hu | 5 hét | $15-30k | átlagos | |
| 15 | MagyarPromptbiblia | 1.5 hét | $8-15k | jó | |

**Forrásként használt validáció:**
- IndieHackers Products / Milestones posztok 2025-2026
- Easy Folders Chrome ext ($3.7k MRR, $42k összes 6 hónap)
- CSS Scan ($100k+ revenue)
- Castmagic ($30k+ MRR podcast wrapper)
- DirStarter / RealWorkFromAnywhere ($5k+ MRR directory/jobboard)
- Easlo Notion templates (milliós Gumroad bevétel)
- Helper-AI Chrome ext ($3.5k 2 hónap alatt)
