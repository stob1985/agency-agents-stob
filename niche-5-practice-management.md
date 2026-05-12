# NICHE 5 – Praxismenedzsment SaaS jogi/fogászati/orvosi rendelőknek

**Bundle:** cal.com (időpontfoglalás) + ERPNext/Frappe (számlázás, CRM, ügymenet) + Documenso (e-aláírás) + OpenEMR (klinikai modul) **vagy** Paperless-ngx (jogi/ügyvédi modul)
**Pozíció:** $199–499/hó/rendelő, ún. „vertical bundle SaaS" 2–10 fős praxisoknak
**Készítés napja:** 2026-05-12

---

## 1. Mit építünk pontosan

### 1.1 Közös platformréteg (minden szubvertikálnál azonos)

**Backend keretrendszer:** ERPNext + Frappe Framework (GPLv3) szolgál mint „operating system" – a számlázás, készletkezelés (csak fogászatnál releváns), bér, könyvelési csatorna, jogosultságkezelés és CRM modulok ide kerülnek. A Frappe ezáltal nagy idő-megtakarítás: nem kell saját CRM-et és könyvelési csatornát írni.

**Időpontfoglalás:** cal.com (AGPL-3 + Enterprise license) – self-hosting commercial license key megvásárlásával ($1500/év nagyságrend, embeddable booking widget). Az ügyvéd/orvos publikus profiljához tartozó „bookings" oldalt és a multi-resource (több orvos/fülke/szoba) ütemezést szolgáltatja.

**E-aláírás:** Documenso Community Edition (AGPL-3) – szerződés/beleegyező nyilatkozat/ABA-engagement letter, EIDAS-kompatibilis kvalifikált aláírás integráció (Adobe Sign helyett kb. €5–10/dokumentum spórolás).

**Frontend:** Saját Next.js + Tailwind „burkoló" felület – brandelt, magyar/angol nyelvű, vertikálspecifikus dashboardokkal. A háttérben REST/GraphQL hívja az ERPNextet és a Documenso/Cal.com instance-okat.

### 1.2 Szubvertikál-specifikus modulok

| Szubvertikál | Klinikai/Szakmai modul | Domain-specifikus extra |
|---|---|---|
| **Jogi (LawDesk.hu)** | Paperless-ngx (GPL-3) – iratkezelés OCR-rel, ügymappa-struktúra | Ügyvédi időmérés (BBI-billing), ügymenet-állapot (peres/peren kívüli), trust-számla (letéti), JÜB-lekérdezés integráció (MÜK API), KAÜ azonosítás |
| **Fogászati (DentalOS.hu)** | OpenEMR „dental edition" + szájdiagram modul | Röntgen DICOM-tárhely (Orthanc – AGPL), fogászati státusz-térkép, készletkezelés (anyagok, instrumentumok), Insurance/NEAK-tételes claim, beteg-marketing recall |
| **Orvosi/háziorvos (PrimaryCare.hu)** | OpenEMR (GPL-3) teljes EHR | EESZT/eRecept kötelező integráció, BNO-kódolás, NEAK finanszírozás-jelentés, telemedicina (Jitsi self-hosted) |

### 1.3 Licencanalízis – KRITIKUS

| Komponens | Licenc | SaaS-os használat | Mit kell tenni |
|---|---|---|---|
| **cal.com** | AGPL-3 + dual commercial | Módosított SaaS-deploy = forráskód kiadási kötelezettség | **License key vásárlás kötelező** (Enterprise tier) [Cal.com docs](https://cal.com/docs/self-hosting/license-key) |
| **ERPNext/Frappe** | GPLv3 | Tisztán self-hosted SaaS-kínálatban OK; csak módosítások disztribuciójánál kell forráskódot kiadni (a klienseknek nem disztribuáljuk – ők használják a hostingot) [License](https://erpnext.com/license-trademark) | Saját burkoló kód külön repo-ban, MIT/proprietary – jogi szempontból elegáns |
| **Documenso** | AGPL-3 Community + Enterprise license | Kiterjesztett moduloknál (`/ee` package) **Enterprise license kell** | Enterprise license vagy a `/ee` kódra építve nem építkezünk |
| **OpenEMR** | GPLv3 (PHP) | SaaS-os hosting OK; a [community megerősítette](https://community.open-emr.org/t/legality-of-saas/18354) hogy a wrapper kód proprietary maradhat | Wrapperben fejlesztünk, OpenEMR-t fork-oljuk, módosításokat upstream-be küldjük |
| **Paperless-ngx** | GPL-3 | Internal SaaS deploy nem trigger-eli a copyleftet | Tisztán self-hosted instance, wrapper kód külön |
| **Orthanc (DICOM)** | AGPL-3 | Megegyezik cal.com-mal | Csak modulként, ne módosítsuk |

**Konklúzió:** A bundle jogilag tiszta, de **kb. $2 500–5 000/év** licencköltségbe fog kerülni (cal.com Enterprise + Documenso Enterprise opcionális). A kulcs: **soha ne forkoljuk** a komponenseket, hanem külön container-ekben futtassuk, REST-en hívjuk, és a saját kódunk legyen a value-add réteg.

### 1.4 Architektúra-vázlat

```
                    ┌────────────────────────────┐
                    │ Next.js Frontend (proprietary)│
                    │  – brand, dashboard, marketing │
                    └──────────────┬─────────────────┘
                                   │ REST/GraphQL
        ┌──────────────────────────┼──────────────────────────────┐
        │                          │                              │
┌───────▼────────┐  ┌──────────────▼─────────┐  ┌─────────────────▼──┐
│ ERPNext+Frappe │  │ cal.com (Enterprise)   │  │ Documenso          │
│ (számlázás,    │  │ – multi-resource       │  │ (e-aláírás)        │
│  CRM, HR)      │  │  scheduling            │  │                    │
└───────┬────────┘  └─────────────┬──────────┘  └────────┬───────────┘
        │                         │                      │
        │           ┌─────────────┴──────────────┐       │
        │           │  Szubvertikál-modul        │       │
        │           │  ┌──────────────────────┐  │       │
        └──────────►│  │ OpenEMR (medical)    │  │◄──────┘
                    │  │ Paperless-ngx (legal)│  │
                    │  │ Orthanc (dental DICOM)│ │
                    │  └──────────────────────┘  │
                    └────────────────────────────┘
                                   │
                         ┌─────────▼──────────┐
                         │ Integrations layer │
                         │  – EESZT (HU)      │
                         │  – Stripe/Barion   │
                         │  – KAÜ, MÜK API    │
                         │  – Google/MS365    │
                         └────────────────────┘
```

**Multi-tenancy:** Single-DB, tenant_id row-level + Postgres RLS. Egy nagyobb klinikának (10+ fő) dedikált VPS opció (Hetzner CX42, kb. €30/hó cost).

---

## 2. Miért most

### 2.1 Általános tailwindek

- **Telemedicina poszt-COVID stabilizáció:** A magyar háziorvosok 70%+ már használt valamilyen digitális eszközt 2024-re ([PMC tanulmány](https://pmc.ncbi.nlm.nih.gov/articles/PMC11566197/)).
- **Open-source érettség:** Cal.com, Documenso 2022-ben jött csak ki – 2026-ra production-ready. OpenEMR 2024+ verziók végre nem PHP4-szerűek.
- **Konszolidálódó incumbent árazás:** Clio $235M ARR → $400M ARR egy év alatt (Q4 2024 → Q4 2025) ([Sacra](https://sacra.com/c/clio/), [Clio press](https://www.clio.com/about/press/series-f/)), $5B valuation – ami **árazási power**-t ad nekünk: a Clio $89–149/user/hó-ra emel, mi $199/rendelő-ben (5 user-re) verjük.
- **AI integráció:** A 2025 Legal Trends report szerint az ügyvédek 79%-a már használ AI-t [2civility](https://www.2civility.org/2025-clio-legal-trends-report/) – nyitottság a tech-re soha nem volt magasabb.

### 2.2 Magyar/EU regulatórius tailwind

- **EESZT kötelező csatlakozás** – 2017 óta minden Magyarországon működő orvos köteles eRecept-et kiállítani EESZT-én keresztül ([e-egeszsegugy.gov.hu](https://e-egeszsegugy.gov.hu/web/eeszt-information-portal/home)). 2026-ban új modulok jönnek (eGYSE, mentális egészségügyi modul).
- **EU eIDAS 2.0** – 2025 végétől EU-szerte kötelezettség a kvalifikált elektronikus aláírás elfogadása → Documenso wrapper integrációja értékes.
- **Magyar Háziorvosi praxisközösség modell** – 2021 óta a GP cluster modell: 422 cluster 2024-ben (365-ről 2021-ben) [Frontiers tanulmány](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1769211/full). Ezek tipikusan 7 praxis együtt – ideális 2–10 fős célközönség.
- **Magyar fogászati cluster-program** – 2021 óta 30%+ rendelő clusterben 2023 végére [Frontiers](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1528433/full).
- **CEPEJ digitalizáció:** Az EU jogi rendszereinek digitalizációja (ügyvédeknek elektronikus benyújtás kötelezővé válása) folyamatos – Magyarországon e-Cégeljárás kötelező 2008 óta.

### 2.3 Versenyhelyzet beli ablak

- **Clio nem belép HU/CEE piacra** komolyan – nincs magyar nyelv, nincs forint, nincs EESZT. Nyitott rés.
- **Dentrix/Eaglesoft** US-bound; EU-ban Carestack próbálkozik csak.
- **A magyar incumbent** (Praxisnet, NetDoktor, PraxiDoc) **technológiailag elavult** – legacy Delphi/PHP, on-prem, nincs mobil app, nincs API.

---

## 3. Piacméret és ARPU – szubvertikálonként

### 3.1 Jogi (LawDesk.hu)

**Globális TAM:** Legal practice management software global market 2025: **$2.84–4.8 milliárd USD**, 2030-ra $4.75–10.9 milliárd ([DataIntelo](https://dataintelo.com/report/global-legal-practice-management-software-market), [360iResearch](https://www.360iresearch.com/library/intelligence/legal-practice-management-software)).

| Régió | Praxisok száma | ARPU | TAM | SAM (2-10 fős) | SOM (5 év, 2% piacszerzés) |
|---|---|---|---|---|---|
| **USA** | ~450 000 ügyvédi iroda, 80% solo/small | $99–199/user/hó | $1.85B | ~$1.2B (small) | ~$24M |
| **EU (excl. UK)** | ~250 000 iroda | €79–149/user/hó | €750M | ~€450M | ~€9M |
| **HU** | 12 500 ügyvéd + 6 000 jelölt + 500 alkalmazott = **~9 000 különálló iroda** [MÜK](https://szakmaikamarak.hu/tagjaink/magyar-ugyvedi-kamara/) | 25–60 EUR/user/hó | €5–10M/év | €3–5M | €100k–300k |

**ARPU sweet spot:** $249/hó/rendelő (átlagosan 3 user), tehát ~$83/user.

**Path to milestones:**
- $100K MRR = **~400 rendelő** vagy 200 nagyobb (5-fős) → 1 ország komplett dominálás (HU) + 200 EU.
- $1M ARR = **~330 rendelő** átlagos áron.
- $10M ARR = **~3 300 rendelő** – ehhez 3–5 ország kell.

### 3.2 Fogászati (DentalOS.hu)

**Globális TAM:** Dental practice management software market 2025: **$2.5–3 milliárd**, 2033-ra $6.77 milliárd, CAGR 10.8% ([Grand View Research](https://www.grandviewresearch.com/industry-analysis/dental-practice-management-software-market)). Európai szegmens: $572M (2024) → $1.04–2.56B (2032), CAGR 10.1–10.3% ([MarketDataForecast](https://www.marketdataforecast.com/market-reports/europe-dental-practice-management-software-market)).

| Régió | Praxisok | ARPU | TAM | SAM (solo+small) | SOM |
|---|---|---|---|---|---|
| **USA** | ~200 000 dental practice, 70% small | $300–800/hó | $1.2B (US) | ~$700M | ~$14M |
| **EU** | ~120 000 dental practice; fragmentált (Magyarországon 1% < láncos) | €200–500/hó | €572M | €350M | €7M |
| **HU** | ~7 180 fogorvos (2023, [Statista](https://www.statista.com/statistics/554977/dentists-in-europe/)), 30%+ cluster-ben → kb. **3 500 rendelő** | €99–199/hó | €4–7M | €3M | €60–150K |

**ARPU sweet spot:** $349/hó/rendelő (1 fogorvos + 1 asszisztens + 1 dentál higiénikus = 3 user).

**Megjegyzés:** Magyar piacon a piacvezető **Open Dental** OSS már létezik, de nincs SaaS-os szolgáltatása CEE-ben – ezt megépítjük mi.

### 3.3 Orvosi/háziorvos (PrimaryCare.hu)

**Globális TAM:** EHR market $35B+ globálisan (de ez magában foglalja a kórházi rendszereket). Ambulant care/practice management szegmense kb. $8B.

| Régió | Praxisok | ARPU | TAM | SAM | SOM |
|---|---|---|---|---|---|
| **USA** | ~230 000 small primary care | $199–599/hó (DrChrono, eCW) | $1.7B | $1B | $20M |
| **EU** | ~280 000 GP praxis | €100–300/hó | €1B | €600M | €12M |
| **HU** | **~5 200 háziorvos**, 422 cluster (átl. 7 praxis/cluster) [Frontiers](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1769211/full) | NEAK-finanszírozott, az állam vesz inkább → nehéz piac | €2–4M | €1–2M | €50–100K |

**ARPU sweet spot:** Magyarországon csak €79/hó/rendelő (állami finanszírozás miatt árcrítikus); USA-ban $399/hó.

**Magyar megjegyzés:** A háziorvosok 80%-a NEAK-finanszírozott, a praxisok kötelező rendszerei „régi és olcsó" (Praxisnet $20/hó). Ez a SZUBVERTIKÁL HU-ban **NEM kezdő piac**. USA-EU magánrendelőkre érdemes pivotolni.

### 3.4 Összesítés – path to ARR

| Mérföldkő | Customer mix | Realisztikus időkeret |
|---|---|---|
| **$100K MRR ($1.2M ARR)** | 400 HU jogi + 50 EU fogászati | M18–M24 |
| **$1M ARR** | 1500 ügyfél, mixed | M24–M36 |
| **$10M ARR** | 3 300 ügyfél, 3–5 ország | M48–M60 |

---

## 4. Konkurenciaelemzés – szubvertikálonként

### 4.1 Jogi (legal)

| Versenytárs | ARR/méret | Árazás | Erősség | Gyengeség | Wedge |
|---|---|---|---|---|---|
| **Clio** | $400M ARR, $5B val ([Sacra](https://sacra.com/c/clio/)) | $99–149/user/hó | Brand, App ecosystem, Clio Payments | Drága, csak EN/USA-bound, nincs HU/EU lokalizáció | Lokalizáció, ár, EESZT/JÜB integráció |
| **MyCase** | ~$80M ARR | $39–119/user/hó ([Capterra](https://www.capterra.com/p/115613/MyCase/pricing/)) | Olcsóbb mint Clio, jó text messaging | US-only, nincs EU support | Hasonló érvek |
| **PracticePanther** | ~$30M ARR | $49–89/user/hó ([PracticePanther](https://www.practicepanther.com/blog/best-legal-practice-management-software/)) | Mid-market | UI elavult, kevés AI | AI-first design |
| **Smokeball** | ~$30M ARR | $49–219/user/hó | Auto-time-tracking | 36 hónapos szerződés | Havi flexibilitás |
| **Rocket Matter** | ~$20M ARR | $59–99/user/hó | Workflow automation | Régi UX | UX, lokalizáció |
| **LeanLaw** | <$10M ARR | $45–55/user/hó | QuickBooks integráció | US-csak | Európai könyvelő integrációk |
| **CosmoLex** | ~$15M ARR | $79–129/user/hó ([LeanLaw](https://www.leanlaw.co/blog/cheapest-solo-law-firm-billing-software/)) | All-in-one accounting | Drága solónak | Olcsóbb tier |

**EU/HU lokális:**
| Magyar lokális | Becsült ARR | Árazás |
|---|---|---|
| **Praetor (Wolters Kluwer)** | piacvezető HU/CZ/SK | €40–80/user/hó |
| **Flowyer** | startup, kis ARR | €30–50/user/hó |
| **Justitia (Arconsult)** | régi, legacy | egyszeri lic. + support |
| **ÜgyvédIrat** | startup | €20–40 |
| **e-Ügyvédi iroda (Praxys)** | startup | €30 |

**A wedge összegezve:** Egy AI-first, modern UI, magyar/angol kétnyelvű, JÜB+MÜK+KAÜ integrált, FREE migráció a Justitia/Praetorból, €49/user/hó-tól. **A wedge nem az ár, hanem az EU-specifikus tooling és UX**.

### 4.2 Fogászati (dental)

| Versenytárs | Méret | Árazás | Erősség | Gyengeség | Wedge |
|---|---|---|---|---|---|
| **Dentrix** (Henry Schein) | 25% market share | $500–800/provider/hó ([Siotek](https://siotek.net/resources/dental-practice-management-software-comparison)) | Brand, biztosítók integráció | On-prem, drága, lassú innováció | Cloud-native ár |
| **Eaglesoft** (Patterson) | 7.7% market share | $400–900/hó | Mid-market | Same as Dentrix | Same |
| **Open Dental** | OSS, 12k+ install | $179/loc + $199–399/provider | OSS-natív, 12 000+ install | Self-hosted nehéz, US-bound | EU-ban hosted SaaS-szal |
| **Curve Dental** | ~$50M ARR | $200/hó-tól ([Curve](https://www.curvedental.com/pricing)) | Cloud-first | US-bound, kevés EU lokalizáció | EU |
| **CareStack** | ~$100M ARR | $698+/user/hó | DSO/multi-loc | Drága solónak | Solo target |
| **Denticon** (Planet DDS) | ~$60M ARR | Custom (€500+) | Multi-location | Drága | Solo target |

**EU/HU lokális:**
- **DentaPlus** (HU) – on-prem, régi, ~3 000 ügyfél
- **InforDent** (HU) – Praxisnet márka, EESZT-integrált
- **Vatera Dent**, **Dentsoft** – kis szereplők

**Wedge:** „Open Dental EU-ban, hosted, EESZT-vel és NEAK-claim-mel, €149/hó-tól, ingyenes adatmigráció a DentaPlusból." Az Open Dental US-fókuszú – mi a EU-port-ot építjük meg.

### 4.3 Orvosi (medical/GP)

| Versenytárs | ARR | Árazás | Erősség | Gyengeség | Wedge |
|---|---|---|---|---|---|
| **AthenaHealth** | $2B+ ARR | %-arányos collections (~6%) | Best-in-class revenue cycle | US-only, nem értelmezhető EU-ban | EU-ra nem releváns |
| **eClinicalWorks** | 150k provider, $700M | $449–599/provider/hó | Brand | Drága, lassú | Ár |
| **Practice Fusion** | Veradigm | Ingyenes (hirdetés-finanszírozott) | Free tier | Adat-monetizálás privacy aggály | GDPR-tiszta alternatíva |
| **DrChrono** (EverHealth) | ~$100M ARR | $199–299/provider/hó ([DrChrono](https://www.drchrono.com/plans-and-pricing/)) | iPad-first | US-only | EU |
| **Kareo/Tebra** | ~$200M ARR | Custom | Mid | US-only | EU |
| **Cerner Ambulatory** | (Oracle) | enterprise | Brand | Enterprise-only | SMB |

**HU lokális (kritikus):**
| Név | Pozíció | Árazás |
|---|---|---|
| **Praxisnet (PRAXIS PLUS)** | piacvezető háziorvos | €15–30/hó |
| **NetDoktor** | mid | €20–40 |
| **PraxiDoc** | mid | €15–30 |
| **Loyal-Soft** | nagy share | €10–25 |
| **MedMax/ProFix** | régi | egyszeri lic. |

Mindegyik **EESZT-akkreditált** ([e-egeszsegugy.gov.hu](https://e-egeszsegugy.gov.hu/engedelyezett-medikai-rendszerek)). **Belépési akadály: EESZT-akkreditáció ~12–18 hónap és €30–80k.**

**Wedge:** A magyar állami háziorvosi piac NEM jó belépő – a NEAK-finanszírozás miatt árlimitált, és az akkreditáció hatalmas akadály. **Pivot: magánrendelők (kardiológus, gyermek-pszichológus, bőrgyógyász, ENT)** – itt $199/hó realisztikus.

---

## 5. Go-to-market stratégia

### 5.1 Melyik szubvertikálba lépjünk először? → **JOGI / Magyar ügyvédi irodák**

**Indoklás:**

1. **Nincs HIPAA/EESZT terhelése** – GDPR elég, nincs egészségügyi adatvédelmi „special category".
2. **A magyar piacon ~9 000 különálló iroda** áll a céltáblán, ahol a tech-szint alacsony (Justitia, Excel, Word) → nagy fájdalom.
3. **Magas ARPU-potenciál:** Az ügyvéd óradíja Budapesten ~€100–200, így €49–99/user/hó könnyen igazolható.
4. **A founder valószínűleg legalább 1 ügyvédet ismer személyesen** Magyarországon – warm intro lehetséges (vs. fogorvost is ismer, de a fogászati tooling és DICOM bonyolultabb).
5. **A bundle ide a legtisztább:** Paperless-ngx + ERPNext + Documenso + Cal.com → mind GPL/AGPL clean, semmi egészségügyi adat.
6. **Kisebb regulátoros risk:** Nincs EESZT-akkreditáció (~12 hónap, ~€50k), nincs HDS certifikáció.

**Másodlagos:** Fogászati (EU magánklinikák), 6–9 hónapra rá.
**Harmadlagos:** Orvosi/magánrendelő, EESZT integráció után 18–24 hó körül.

### 5.2 Első 10 ügyfél taktikák

**Jogi (HU):**
1. **Budapesti Ügyvédi Kamara** (8 000 tag) – sponsor rendezvény, billentyű előadás „AI az ügyvédi praxisban"
2. **Jogászvilág.hu** sponsored article + interjú a founderrel
3. **MÜK regionális események** – Győr, Pécs, Debrecen, Szeged: face-to-face demo
4. **LinkedIn outreach** ügyvédjelöltekre, akik most alapítanak irodát (csoportban: „Ügyvédjelöltek" 2–3000 fő)
5. **Pioneer pricing:** Első 20 iroda 6 hónapig ingyen, NPS feedback-ért
6. **Migration-as-a-service:** A founder maga csinálja meg a Justitia→LawDesk migrációt, $0-ért (csak idő-investálás)
7. **Substack/blog:** „Hogyan modernizáltam a 3-fős ügyvédi irodámat" – ügyfél-történetek

**Fogászati (EU/HU):**
1. **Dental Tribune Hungary** – sponsored content
2. **Dental World konferencia (Budapest, október)** – stand, demo
3. **MFE (Magyar Fogorvosok Egyesülete)** – partnership
4. **Open Dental community** – „We host Open Dental for EU practices" üzenet az [Open Dental forumon](https://www.opendental.com/forum)
5. **Pioneer agentry:** Egy fogászati IT-implementer ([Smiles by Design Implementation Consultants](https://www.example.com) – ilyen role létezik) ad referencia ügyfeleket 20% rev-share-ért
6. **Direct mail Budapest fogászatokba** – 200 levél kézbesítve, follow-up call

**Orvosi (EU magánrendelő):**
1. **MOK** (Magyar Orvosi Kamara) – sponsorship
2. **Magán-kardiológus klinikák** target list (~200 HU-ban)
3. **MedicalExpo, Frankfurt** Medica konferencia

### 5.3 Árazás és csomagolás

| Tier | Ár (HU/EU) | Tartalom | Cél |
|---|---|---|---|
| **Solo** | €49/hó/user | 1 user, alap features, common templates | Solo ügyvéd, solo fogorvos |
| **Practice** | €149/hó (3 user-ig) | 3 user, Documenso, automation | 2-3 fős iroda – **a sweet spot** |
| **Growth** | €299/hó (10 user-ig) | 10 user, multi-location | 4-10 fős |
| **Enterprise** | custom, €499+ | Dedicated VPS, SSO, prioritás support | 10+ fő |

**Pricing logic:** Clio $99/user → 3 user = $297 → mi €149 az egész irodáért (5 user-ig) = **50%+ olcsóbb**, és helyileg lokalizált.

### 5.4 Disztribúciós csatornák

1. **Szakmai kamarák/szövetségek** (MÜK, MFE, MOK)
2. **Konferenciák:** Dental World (Budapest), Magyar Jogász Egylet kongresszus, Magyar Ügyvéd Konferencia, ELE European Lawyers' Congress
3. **Niche publikációk:** Jogászvilág, JogiFórum, Magyar Fogorvos, Dental Tribune, IME-Egészségügy
4. **Referral partnership:** Könyvelők (a kis ügyvédi irodáknak a könyvelő intim partner), Wolters Kluwer regional reseller-jei, dentál depot cégek (Dentech, Dental2000)
5. **Implementator/consultant partnerek:** Magyarországon ~10–20 független IT-szolgáltató dolgozik fogorvosoknak/ügyvédeknek – ezeknek 20–30% rev-share-t adunk az első évre

### 5.5 Cold outreach angle-ek

- **Ügyvéd:** „Mennyit fizetsz havonta a Praetorért + Adobe Sign-ért + Calendly-ért + JogTárért? Mi mindezt €149-ben adjuk, és van JÜB-integráció is."
- **Fogorvos:** „A DentaPlus offline van, a beteged nem tud online időpontot foglalni. Mi az időpontfoglalástól a NEAK-elszámolásig mindent egyben adunk, és a recall-marketing fogadtatott 12%-kal több visszatérő beteget az átlag ügyfeleinknél."
- **Magánorvos:** „GDPR-tiszta EU-hosted EHR, online beteg-portál, e-aláírású beleegyezés, telemedicina – mind egyben, €199/hó."

### 5.6 12 hónapos roadmap

| Hónap | Cél |
|---|---|
| M1–M3 | MVP – LawDesk.hu (jogi vertikál), self-hosted bundle, 3 design partner |
| M4–M6 | 10 fizető ügyvédi iroda HU, ARR €5–10k |
| M7–M9 | Fogászati vertikál béta (DentalOS.hu) + 3 fogászati design partner |
| M10–M12 | 30+ jogi + 10 fogászati ügyfél, ARR €60–80k, első alkalmazott (sales/CS) |

---

## 6. MVP architektúra

### 6.1 Mit építsünk először?

**LawDesk.hu – jogi vertikál MVP**, az alábbi minimum feature-ökkel:

1. **User mgmt + multi-tenant** (Frappe natívan ad)
2. **Ügyfél (kliens) CRM** – ERPNext „Customer" entitás kiterjesztve
3. **Ügy/Matter mgmt** – custom Frappe DocType
4. **Időmérés (billing)** – ERPNext „Timesheet" kibővítve óradíj/ügyfél
5. **Számlázás** – ERPNext NAV-online integráció (létezik már OSS plugin)
6. **Iratkezelés** – Paperless-ngx wrapper, OCR magyar nyelv
7. **E-aláírás** – Documenso embed
8. **Időpontfoglalás** – Cal.com embed
9. **JÜB + KAÜ integráció** – MÜK API-n keresztül (csak nézve)
10. **Letéti/trust accounting** – critical jogi sajátosság

### 6.2 Multi-tenancy

**Recommended:** Single instance, **shared DB + Postgres Row-Level Security**, tenant_id minden táblán. Frappe natívan támogatja (`site_name` per tenant).

**Enterprise tier (Growth+):** Dedikált VPS Hetznerben – CX42 €30/hó, full automation Terraform-mal.

### 6.3 Hosting/infra stack

| Réteg | Választás | Indok |
|---|---|---|
| **Cloud** | Hetzner (Frankfurt/Helsinki) | EU-only, GDPR-tiszta, 60–70% olcsóbb mint AWS |
| **Orchestration** | Docker + Coolify (self-hosted PaaS) | Egyszerűbb mint K8s |
| **DB** | Postgres 16, Frappe-natív MariaDB-replacement | RLS, JSONB |
| **Storage** | MinIO (S3-compat) self-hosted | Iratoknak |
| **CDN** | Cloudflare | DNS, WAF |
| **Backup** | Restic + Backblaze B2 | EU region |
| **Monitoring** | Grafana + Loki + Prometheus | OSS |
| **Email** | Postmark vagy Resend | Tranzakcionális |

**Becsült infra-cost:** €200–500/hó az első 50 ügyfélig.

### 6.4 Integrációk

- **Stripe + Barion (HU local payment)** – számlafizetés ügyfeleknek
- **NAV Online Számla** – kötelező magyar e-számla
- **Google/MS365 Calendar** – Cal.com natívan
- **MÜK JÜB API** – ügyfél azonosítás
- **DocuSign export** – migráció ügyfeleknek
- **EESZT** (csak fogászati/orvosi modulra) – ZP/v1.x SOAP API ([dokumentáció](https://e-egeszsegugy.gov.hu/web/eeszt-information-portal/))

### 6.5 Build idő

| Szakasz | Idő | Erőforrás |
|---|---|---|
| Bundle setup, docker-compose | 2 hét | Founder |
| Frappe custom app (LawMatter, LawClient, TimeEntry) | 6 hét | Founder + 1 fejlesztő |
| Frontend (Next.js dashboard) | 6 hét | 1 fejlesztő |
| JÜB/NAV/Cal.com integráció | 4 hét | 1 fejlesztő |
| QA, design partner deploy | 4 hét | Founder |
| **TOTAL MVP** | **~5 hónap** | 2 főállás |

---

## 7. Kockázatok és moat

### 7.1 Top 5 kockázat

1. **HIPAA/GDPR/EESZT compliance regulatory risk** – Egy adatvédelmi incident GDPR-os 4%/€20M büntetést hozhat. **Mitigation:** EU-only hosting, ISO 27001 célzott, HDS-cert opcionális. A jogi vertikál MOK-ESZT-mentes, kisebb regulatory burden.
2. **A licenc compliance probléma** – Ha AGPL-modulokat módosítunk, kötelességünk forrásnyíltság. **Mitigation:** Soha ne forkoljunk, csak container-eljünk; minden saját kód külön repo-ban; jogi review évente.
3. **Switching cost – data migráció** – Az incumbensek (Justitia, DentaPlus) jól tudják, hogy az ügyfél adatát nehéz kivinni. **Mitigation:** Mi pont fordítva, ingyenes adat-import minden főbb rendszerből (CSV, SQL export). Migráció maga lesz a fő sales mechanism.
4. **Az incumbent árcsökkentése** – Clio/MyCase 30% kedvezményt ad ha mi belépünk a piacba. **Mitigation:** Lokalizáció, hyperlokális feature (NAV, MÜK, EESZT) – ezeket az incumbensek 12+ hónap alatt sem tudják kiépíteni.
5. **Open Dental / cal.com licenc-változás** – Ha cal.com átáll teljes commercial-ra, $2k/év → $50k/év. **Mitigation:** Fork pont, mert AGPL → bármikor self-host-olhatjuk a régi verziót; alternatíva: schedulely vagy saját scheduler.

### 7.2 Moat építés

1. **Adat-migráció a moat** – minden incumbensből (Praetor, Justitia, DentaPlus, Praxisnet) **automata importer**. Ez egyirányba dolgozik: nekünk könnyű behozni, nehéz kivinni → reverse switching cost.
2. **Integráció-mélység** – NAV, MÜK, EESZT, NEAK – ezek egyenként 3–6 hónap; ha mi 3 ország 6 hivatali integrációját birtokoljuk, akkor egy US-incumbensnek 18 hónap utánunk lenni.
3. **Compliance-stamp** – HDS-cert (FR), ISO 27001, GDPR-DPO certified – ezek pénzbe kerülnek, és az SMB-versenytársak nem rendelkeznek velük.
4. **Workflow data network effect** – Anonimizált benchmark data (ügyvédi óradíj-trendek, fogászati átlag-kezelési idők) – ez egy „industry intelligence report"-tá tud nőni évente.
5. **Vertical bundling pricing power** – Egyben adni e-aláírást, ütemezést, számlázást, dokumentumkezelést – ez 3–5 SaaS-ot vált ki. Az ügyfél nem fogja egyenként cserélni le őket.

---

## 8. Hungary/EU vs. US opportunity

### 8.1 Hol kezdjünk?

**Recommendation: HU + CEE (Csehország, Szlovákia, Lengyelország) first, EU expansion M12+, US M24+.**

**Indoklás:**
1. **A founder magyar – warm intro-k, nyelvtudás, kulturális ismeret**
2. **HU piac alacsony tech-szint** + magas fájdalom = jó MVP testbed
3. **CEE összesen 60M+ lakos, ~30 000 ügyvédi iroda** – jelentős TAM
4. **US-ban Clio/MyCase brutál** – $5B valuation = mindenkit ki tud ütni. **US-ba csak hyperspecial niche-szel érdemes menni** (pl. „Workers' Comp law firms in California" – túl szűk nekünk).
5. **EU GDPR mint moat:** Az US-incumbensek nem GDPR-compliant by default; ha mi EU-hosting + GDPR DPO-val belépünk a német/francia piacra, **moat**.

### 8.2 HU-specifikus regulatory

| Követelmény | Vertikál | Idő/költség |
|---|---|---|
| **EESZT akkreditáció** | Orvosi, fogászati | 12–18 hó, €30–80k |
| **NAV Online Számla integráció** | Mindenki | 1 hó, €5k |
| **GDPR DPO** | Mindenki | €1k–3k/év |
| **NEAK claim integráció** | Háziorvos, fogászati | 3–6 hó, €15k |
| **MÜK JÜB API** | Jogi | 2 hét, €0 (free API) |
| **NAIH bejegyzés** | Mindenki | 2 hét, €0 |

### 8.3 Pricing power különbségek

| Piac | LawDesk ár | DentalOS ár | Primary Care ár |
|---|---|---|---|
| **HU** | €49–149/hó | €99–199/hó | €79 (magán only) |
| **DE/AT** | €99–249/hó | €199–399/hó | €149–299/hó |
| **US** | $199–499/hó | $299–699/hó | $249–599/hó |

**A US pricing 2-3x EU/HU**, ami később justification az US expansion-re.

### 8.4 GDPR mint moat vs. burden

**Moat (igen):** Az US incumbensek (Clio, DrChrono) **nem rendelkeznek HDS-certifikációval, nem EU-DC-ben hosztolnak**. Egy német ügyvédi iroda nem fogja Clio-t használni. **Mi: EU-only hosting, GDPR DPO, ISO 27001 → automatikusan ezen kompetícióban verjük őket.**

**Burden (kicsit):** Az ISO 27001 + HDS-cert kb. €30–60k évente. De ezt a 100. ügyfél után már beleépíthetjük az árazásba (€10/ügyfél/hó = €12 000/év 100 ügyfélnél = ~€10k margin).

---

## 9. Első 90 nap akcióterv

### Hét 1–2: Diszkovéra és validáció
- [ ] 15 mélyinterjú: 8 ügyvéd (solo, 3-fős, 7-fős), 4 fogorvos, 3 magánrendelő – ki fizetne, mit fizetne, mit utál
- [ ] 5 ügyvéd – Justitia/Praetor demo-t kérni, fájdalmas munkafolyamatokat megfigyelni
- [ ] Versenytárs deep-dive: Clio (sandbox), MyCase (trial), Praetor (demo), Flowyer
- [ ] Domain regisztráció: lawdesk.hu, dentalos.hu, primarycare.hu

### Hét 3–4: Architektúra és setup
- [ ] Hetzner cloud + Coolify + Postgres + MinIO setup
- [ ] Frappe + ERPNext baseline deploy
- [ ] Cal.com Enterprise license vásárlás ($1500/év)
- [ ] Documenso self-host
- [ ] Paperless-ngx self-host, magyar OCR (Tesseract HU)
- [ ] Repo struktúra: `lawdesk-app/` (Next.js), `lawdesk-frappe/` (custom Frappe app), `infra/` (Terraform)

### Hét 5–8: MVP build
- [ ] Frappe custom DocTypes: Matter, Client, TimeEntry, TrustAccount
- [ ] Next.js dashboard – bejelentkezés, ügyfélkezelés, ügymenet, időmérés, dokumentumok
- [ ] Cal.com embed booking widget
- [ ] Documenso wrapper – „Aláírásra küldés"
- [ ] NAV Online Számla integráció (létező OSS modul)
- [ ] Paperless-ngx API integráció: drag-drop irat-upload, automata tag

### Hét 9: Design partnerek onboard
- [ ] 3 ügyvédi iroda ingyenes (6 hónapig) az MVP testing-ért
- [ ] Adat-migráció kézzel (founder maga), Justitia → LawDesk
- [ ] Weekly check-in, feedback loop

### Hét 10–11: Polish + go-live
- [ ] Landing page (lawdesk.hu)
- [ ] Pricing oldal
- [ ] Stripe + Barion fizetési integráció
- [ ] GDPR DPA template, NAIH bejegyzés
- [ ] Email-marketing setup (Resend)

### Hét 12: Launch
- [ ] LinkedIn launch post – founder maga írja a story-t
- [ ] Jogászvilág sponsored article negotiation
- [ ] MÜK Budapest – meeting kérése, hogy bemutathassuk
- [ ] Első 10 cold outreach: solo ügyvédjelölt, akik 6 hónapon belül kezdik a praxist
- [ ] Mérés: signup-ok, conversion, NPS a 3 design partnertől
- [ ] **Cél: 5 fizető ügyfél 90 napra, €750 MRR**

---

## Összefoglalás

A **LawDesk.hu** (jogi vertikál) Magyarországon és CEE-ben tiszta belépő piac: ~9 000 magyar ügyvédi iroda, alacsony tech-szint, elavult incumbensek, magas pricing power (€49–149/user/hó), GDPR mint moat, nincs egészségügyi compliance regulatory. A bundle (ERPNext + Paperless-ngx + Documenso + Cal.com) jogilag tiszta GPL/AGPL kombinált commercial license-kkel. MVP 5 hónap alatt, $100K MRR 18–24 hó alatt 400 ügyfélnél elérhető.

---

## Források

### Open source licencelés
- [Cal.com LICENSE](https://github.com/calcom/cal.com/blob/main/LICENSE)
- [Cal.com license key documentation](https://cal.com/docs/self-hosting/license-key)
- [Cal.com AGPL changeover blog](https://cal.com/blog/changing-to-agplv3-and-introducing-enterprise-edition)
- [OpenEMR LICENSE](https://github.com/openemr/openemr/blob/master/LICENSE)
- [OpenEMR SaaS legality discussion](https://community.open-emr.org/t/legality-of-saas/18354)
- [ERPNext License & Trademark](https://erpnext.com/license-trademark)
- [Documenso licenses](https://docs.documenso.com/users/licenses)
- [Documenso Enterprise Edition](https://docs.documenso.com/docs/policies/enterprise-edition)
- [Paperless-ngx GitHub](https://github.com/paperless-ngx/paperless-ngx)

### Versenytárs adatok
- [Clio $5B Series G (Sacra)](https://sacra.com/c/clio/)
- [Clio 2024 Series F press](https://www.clio.com/about/press/series-f/)
- [How Clio Built a $3B Empire](https://blog.legaltechmg.com/how-clio-built-a-legal-practice-management-empire)
- [Clio TechCrunch](https://techcrunch.com/2024/07/23/clio-raises-900m-at-a-3b-valuation-plans-to-double-down-on-ai-and-fintech/)
- [MyCase pricing (Capterra)](https://www.capterra.com/p/115613/MyCase/pricing/)
- [PracticePanther pricing](https://www.practicepanther.com/blog/best-legal-practice-management-software/)
- [LeanLaw pricing comparison](https://www.leanlaw.co/blog/cheapest-solo-law-firm-billing-software/)
- [Dentrix/Eaglesoft/Open Dental comparison (Siotek)](https://siotek.net/resources/dental-practice-management-software-comparison)
- [Dentrix market share (Enlyft)](https://enlyft.com/tech/products/dentrix)
- [Eaglesoft market share (Enlyft)](https://enlyft.com/tech/products/eaglesoft)
- [Curve Dental pricing](https://www.curvedental.com/pricing)
- [DrChrono pricing](https://www.drchrono.com/plans-and-pricing/)
- [eClinicalWorks pricing (EHR Source)](https://www.ehrsource.com/articles/ehr-cost-guide/)

### Piacelemzés
- [Legal Practice Mgmt market (DataIntelo)](https://dataintelo.com/report/global-legal-practice-management-software-market)
- [Legal Practice Mgmt market (360iResearch)](https://www.360iresearch.com/library/intelligence/legal-practice-management-software)
- [Legal Practice Mgmt CAGR (Yahoo Finance)](https://finance.yahoo.com/news/legal-practice-management-software-market-094100480.html)
- [Dental Practice Mgmt EU market (MarketDataForecast)](https://www.marketdataforecast.com/market-reports/europe-dental-practice-management-software-market)
- [Dental Practice Mgmt global (Grand View)](https://www.grandviewresearch.com/industry-analysis/dental-practice-management-software-market)
- [Dental Practice Mgmt CAGR (Mordor Intelligence)](https://www.mordorintelligence.com/industry-reports/dental-practice-management-software-market)
- [Dental Vertical SaaS (OMERS Ventures)](https://medium.com/omers-ventures/dental-vertical-software-drilling-into-trends-and-opportunities-bcd422676a15)
- [Clio Legal Trends 2025](https://www.2civility.org/2025-clio-legal-trends-report/)

### Magyar/EU specifikus
- [EESZT Information portal](https://e-egeszsegugy.gov.hu/en/web/eeszt-information-portal/home)
- [EESZT accredited systems](https://e-egeszsegugy.gov.hu/engedelyezett-medikai-rendszerek)
- [Magyar Ügyvédi Kamara (Szakmai Kamarák)](https://szakmaikamarak.hu/tagjaink/magyar-ugyvedi-kamara/)
- [Budapesti Ügyvédi Kamara](https://bpugyvedikamara.hu/kamarank/bemutatkozas/)
- [Hungary dental cluster progress (Frontiers)](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1528433/full)
- [Hungary GP cluster model (Frontiers)](https://www.frontiersin.org/journals/health-services/articles/10.3389/frhs.2026.1769211/full)
- [Hungary dental market US Trade.gov](https://www.trade.gov/market-intelligence/hungary-dental-market)
- [Dentists in Europe by country (Statista)](https://www.statista.com/statistics/554977/dentists-in-europe/)
- [HU primary care evaluation (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8278788/)
- [HU primary care digital adoption (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11566197/)
- [Praxisnet Hungary GP software](https://www.praxisnet.hu/)
- [Wolters Kluwer Praetor HU](https://www.wolterskluwer.com/hu-hu/solutions/praetor-hu)
- [Flowyer ügyvédi szoftver](https://www.flowyer.hu/)
- [Justitia ügyvédi szoftver](https://www.egyszeru-ugyvitel.com/megoldas.html)

### Compliance / Hosting
- [HDS certification guide](https://www.feelagile.com/en/guide/guide-hds)
- [GDPR healthcare (Drata)](https://drata.com/learn/gdpr/for-healthcare)
- [HIPAA SaaS startup costs (Security Compliance Guide)](https://securitycomplianceguide.com/blog/hipaa-compliance-saas-startups/)
- [AWS HIPAA compliance](https://aws.amazon.com/compliance/hipaa-compliance/)
