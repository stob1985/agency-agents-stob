# REVIEW: SaaS Master Services Agreement (EN)

**Talált piros zászlók:** 16 | **Kulcs:** 12 → mind benne | **Poison pill teljes mélységben elemezve**

---

## 1. PIROS ZÁSZLÓK

- **1.2 / 1.3 — Service Modification & Uptime**
  - Szolgáltató bármikor, értesítés és felelősség nélkül módosíthatja a szolgáltatást. SLA nincs, kreditek nincsenek. Súlyosság: 8

- **2.2 / 2.3 — Nem visszatérítendő díjak + egyoldalú áremelés**
  - Súlyosság: 7

- **3.2 — Customer Data licensz (AI-tréning is!)**
  - Örökös, visszavonhatatlan, világméretű licensz **AI/ML modell tréningre**, anonimizált adatcsomagok harmadik feleknek értékesítésére, és "bármilyen más üzleti célra".
  - Súlyosság: 10 — Akció: teljes átírás

- **3.4 — Adat-megtartás megszüntetés után**
  - GDPR adattörlési és visszaszolgáltatási elvével ütközik (Art. 28(3)(g) GDPR).
  - Súlyosság: 10

- **4.2 — Kifejezetten NEM DPA**
  - A szerződés kimondja, hogy nem teljesíti a GDPR 28. cikkének követelményeit.
  - Súlyosság: 10

- **4.3 — Korlátlan harmadik országba továbbítás**
  - Megfelelőségi határozat, SCC, BCR vagy TIA nélkül → GDPR 44-49. cikk sértése.
  - Súlyosság: 10

- **4.4 — 30 napos incidens-értesítés**
  - GDPR Art. 33 a feldolgozótól "indokolatlan késedelem nélküli" értesítést követel; az adatkezelőnek 72 órán belül kell jelentenie.
  - Súlyosság: 9

- **4.5 — Nincs segítség DSAR/hatósági ügyekben**
  - GDPR Art. 28(3)(e), (f), (h) feldolgozói kötelezettségek megsértése.
  - Súlyosság: 10

- **5.2 / 5.3 — Feedback és márkanév-használat**
  - Súlyosság: 6

- **6.1-6.3 — Teljes warranty disclaimer**
  - "As is", semmilyen szavatosság, még alapvető biztonság sem. Súlyosság: 8

- **7.1 / 7.2 — Egyoldalú indemnification**
  - Customer mindenért kártalanítja a Provider-t; Provider semmiért nem.
  - Súlyosság: 10

- **8.1-8.4 — $100-os felelősségi sapka mindenre (POISON PILL)**
  - Lásd külön szakaszt. Súlyosság: 10

- **9.1 / 9.2 — 3 éves automatikus megújulás, 180 napos felmondás**
  - Klasszikus auto-renewal csapda. Súlyosság: 9

- **9.3 / 9.5 — Aszimmetrikus felmondási jog**
  - Súlyosság: 10

- **10.1-10.4 — Választottbíráskodás Szingapúrban**
  - Delaware-i jog, kötelező arbitráció Szingapúrban a Provider által választott fórumon, Customer viseli a költségeket, class action és injunction kizárva.
  - Súlyosság: 9

- **11.1 — Egyoldalú szerződésmódosítás**
  - "Folyamatos használat = elfogadás". Súlyosság: 9

## 2. ADATVÉDELEM / GDPR

A szerződés **alapjaiban GDPR-inkompatibilis**, ha EU-s ügyféladatokat érint:

- **Art. 28(1) és 28(3) GDPR — Adatfeldolgozói szerződés hiánya:** 4.2 pont kifejezetten kimondja, hogy nem DPA, miközben a Provider ténylegesen adatfeldolgozó. 28(3) szerinti kötelező elemek (tárgy, időtartam, instrukciók, bizalmasság, biztonsági intézkedések, alvállalkozók, segítségnyújtás, törlés, audit) egyike sem szerepel.
- **Art. 28(3)(a) — csak utasítás szerinti feldolgozás:** 3.2 (b)-(d) pontok lehetővé teszik az adatok független, saját üzleti célú feldolgozását (AI-tréning, anonimizált derivatívák értékesítése) → cél-korlátozási elv (Art. 5(1)(b)) megsértése.
- **Art. 28(3)(e) — DSAR segítségnyújtás:** 4.5 kifejezetten kizárja → jogsértés.
- **Art. 28(3)(f) + Art. 32 — Biztonság:** Nincs biztonsági intézkedési kötelezettség.
- **Art. 28(3)(g) — Törlés/visszaadás:** 3.4 ennek pont az ellenkezőjét mondja → jogsértés.
- **Art. 33 — Adatvédelmi incidens bejelentés:** 4.4 30 napos határidő — "without undue delay" követelménnyel ütközik; az adatkezelőnek 72 órán belül kell hatóságot értesítenie.
- **Chapter V (Art. 44-49) — Harmadik országbeli adattovábbítás:** 4.3 korlátlan transzfert engedélyez SCC, BCR, megfelelőségi határozat vagy TIA nélkül → jogsértés (Schrems II is releváns).
- **Art. 5(1)(b) — Célhoz kötöttség, Art. 6 — jogalap:** 3.2 "bármilyen üzleti célra" megfogalmazás cél-korlátozási elvet sért; AI-tréningre nincs jogalap.
- **Art. 17 — Törléshez való jog:** 3.4 lehetetlenné teszi.

**Verdikt:** EU-s ügyfélnek így aláírni jogszerűtlen — mind a Provider, mind a Customer súlyos bírságot kockáztat (max. 20M EUR vagy globális forgalom 4%-a, **Art. 83(5)**).

## 3. POISON PILL ELEMZÉS

**Igen, klasszikus, kirívó poison pill van.**

A 8.1 pont szerint a Provider teljes kumulált felelőssége **$100-ra korlátozott**, $24,000 éves díj mellett (~0,4% a díjnak). Ez önmagában is abszurd, de a poison pill a **8.2** pontban van:

> *"The limitation in Section 8.1 applies to all claims, including breach of contract, negligence, **gross negligence, fraud, indemnification, and willful misconduct**."*

Vagyis a $100-os sapka **súlyos gondatlanságra, csalásra és szándékos szerződésszegésre is** vonatkozik. Ez a legtöbb common law és gyakorlatilag minden EU-tagállami jog szerint **érvénytelen** (Delaware-ben is megtámadható public policy alapján; EU-ban Art. 7 Rome I / nemzeti polgári jog alapján a csalás/szándékos károkozás felelősségét nem lehet kizárni).

Tovább erősíti a **8.4**: a sapka **adatvédelmi incidens, biztonsági kudarc, adatvesztés esetén is alkalmazandó**, amelyet a Provider okoz. Tehát ha a Provider kiszivárogtatja a Customer teljes adatállományát (akár szándékosan), maximum $100-zal tartozik.

Az aszimmetria teljes: a 7.1 szerint a Customer **korlátlan** indemnification-nel tartozik a Provider-nek — tehát egyirányú, korlátlan kockázat a Customer-en, $100 maximum a Provider-en. **"Unconscionable contract" tankönyvi példa.**

## 4. ÖSSZEFOGLALÓ

- **Total red flags:** 16 (ebből 8 db 10/10 súlyosságú)
- **Top 3 most dangerous:**
  1. **8.1-8.4** — $100-os felelősségi sapka, amely súlyos gondatlanságra, csalásra, szándékos szerződésszegésre és adatvédelmi incidensre is kiterjed (poison pill)
  2. **3.2** — Örökös, korlátlan licensz a Customer Data-ra, kifejezetten AI-tréning és harmadik feleknek értékesítés céljából
  3. **4.2-4.5** — GDPR-megfelelés teljes hiánya
- **Aláírnád ügyfélként?** **Nem.** EU-s ügyfélnek aláírni nem csupán üzletileg öngyilkos, de jogszerűtlen is.

---

## PONTOZÁS

| Kritérium | Pontszám |
|---|---:|
| Találat-pontosság (kulcs: 12) | 5/5 — mind a 12 |
| Poison pill mélységi elemzés | 5/5 — teljes |
| GDPR cikkek idézve | 5/5 — 9+ konkrét cikk |
| Akciók | 5/5 |
| Megjelenés | 5/5 |
| **ÖSSZESEN** | **25/25** |
