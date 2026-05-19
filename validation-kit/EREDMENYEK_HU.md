# ContractMD – Validáció Eredmények

> Töltsd ki minden teszt után. A végén összegezzük → GO / TUNE / PIVOT döntés.

---

## TESZT 1: Freelancer Contract (EN)

**Fájl:** `contracts-en/freelancer_contract.md`

### Beépített piros zászlók (referencia – ne nézz rá futtatás előtt!)

<details>
<summary>Kattints a megoldó kulcsért</summary>

1. **IP overreach** (3.1) — minden szellemi alkotás a kliensé, akkor is, ha nem kapcsolódik a feladathoz
2. **24 hónapos non-compete, világméretű** (5.1) — túlzott, valószínűleg érvénytelen
3. **Uncapped indemnification** (6.1, 6.2) — bármilyen kárért, korlátlanul
4. **Poison pill liability cap** (7.1) — $100 cap egy $50k szerződésben, MIKÖZBEN a contractor uncapped indemnify
5. **Aszimmetrikus termination** (8.1, 8.2) — kliens bármikor, contractor 90 napos felmondással
6. **Net 90 fizetés + 25% visszatartás** (2.2, 2.3) — cash flow gyilkos
7. **Egyoldalú szerződésmódosítás** (11.1) — kliens egyoldalúan módosíthat

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság (hányat talált meg a 7-ből?) |   /5 | _Hány találat: _ /7_ |
| Magyarázat minősége (nem-jogász érti?) |   /5 | |
| Akciók (konkrét javaslat, nem csak diagnosis?) |   /5 | |
| Megjelenés (profi vagy zavaros?) |   /5 | |
| PDF minőség |   /5 | |
| **ÖSSZESEN** | **  /25** | |

### Mit hagyott ki, ami fáj?
_(írd ide)_

---

## TESZT 2: Apartment Lease (EN — NYC)

**Fájl:** `contracts-en/apartment_lease.md`

<details>
<summary>Megoldó kulcs</summary>

1. **3 havi kaució** (2.1) — **NY állami törvény szerint max 1 havi** (Housing Stability Act 2019)
2. **Egyoldalú díjemelés bármikor** (1.3) — törvénytelen a határozott idő alatt
3. **Hidden fees** (3.2, 3.3, 3.4) — $175 + $50 + $200 — sok rejtett díj
4. **Korlátlan rule-módosítás + $500/nap büntetés** (5.2, 5.3) — egyoldalú
5. **Belépés bármikor értesítés nélkül** (6.1) — NY-ben min. 24 órás notice kell
6. **Bérlő fizet minden javítást, inkl. structural** (7.1) — törvénysértő (warranty of habitability)
7. **No mitigation duty** (8.2) — NY 2019 óta KÖTELEZŐ a mitigation
8. **Liability waiver gross negligence kivételével** (10.1) — túl tág
9. **Holdover 125% rent** (11.1) — kiszámolható, de aszimmetrikus notice (30 vs 60 nap)
10. **Aszimmetrikus attorney fees** (12.2) — érvénytelen sok joghatóságban

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság |   /5 | _Hány találat: _ /10_ |
| Magyarázat minősége |   /5 | |
| Akciók |   /5 | |
| Megjelenés |   /5 | |
| PDF minőség |   /5 | |
| **ÖSSZESEN** | **  /25** | |

**Kritikus kérdés:** Megtalálta-e a **NY-specifikus jogsértést** (3-havi kaució illegális)?  □ Igen / □ Nem

---

## TESZT 3: SaaS MSA (EN)

**Fájl:** `contracts-en/saas_msa.md`

<details>
<summary>Megoldó kulcs</summary>

1. **Customer Data AI training-re** (3.2.b) — privacy bomb
2. **Adatok harmadik feleknek értékesíthetők** (3.2.c)
3. **Adatok megőrzése termination után is** (3.4)
4. **GDPR explicit elutasítás** (4.2) — "ez NEM DPA"
5. **30 napos incidens-bejelentés** (4.4) — GDPR-ben **72 óra**!
6. **$100 liability cap** (8.1) — poison pill
7. **Cap szándékos szerződésszegésre is** (8.2) — érvénytelen sok joghatóságban
8. **Cap data breach-re is** (8.4) — extrém durva
9. **3-éves auto-renewal, 180 napos notice** (9.2)
10. **Kötelező arbitráció Szingapúrban, customer költségére** (10.2)
11. **No injunctive relief, no jury, no class action** (10.3)
12. **Feedback license assignment** (5.2)

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság |   /5 | _Hány találat: _ /12_ |
| Magyarázat minősége |   /5 | |
| Akciók |   /5 | |
| Megjelenés |   /5 | |
| PDF minőség |   /5 | |
| **ÖSSZESEN** | **  /25** | |

**Kritikus kérdés:** Megtalálta-e a **poison pill** logikát (8.2: cap szándékos szegésre is)? □ Igen / □ Nem
**Kritikus kérdés:** Megtalálta-e az **AI training klauzulát** (3.2.b)? □ Igen / □ Nem

---

## TESZT 4: Vállalkozói szerződés (HU)

**Fájl:** `contracts-hu/vallalkozoi_szerzodes.md`

<details>
<summary>Megoldó kulcs (magyar specifikus!)</summary>

1. **Színlelt szerződés gyanú** (1.3, 1.4) — heti 40 óra, kötelező iroda, eszközhasználat, projektvezető-jelentés → **bujtatott munkaviszony**, NAV-cél lehet (Mt. 2/A. §)
2. **8 napos fizetési határidő** (2.3) — Ptk. 6:130. § szerint **B2B-ben max 60 nap**, de itt fordítva: túl rövid + felfüggeszthető
3. **Korlátlan IP-átruházás, jogkimerítően nélküli ellenérték** (3.1, 3.2) — Szjt. szerint a vagyoni jogok átruházásához **arányos ellenérték kell**, "benne van a díjban" formula gyakran nem elég
4. **Személyhez fűződő jogokról lemondás** (3.3) — a Szjt. szerint a **névfeltüntetés joga érvényesen nem mondható le**
5. **36 hónapos versenytilalom ellenérték nélkül** (5.1, 5.2) — Mt. 228. § szerint vállalkozóra nem teljes mértékben, de bíróság **ellenérték nélkül érvénytelennek mondja ki**
6. **Korlátlan kártérítés + előreláthatóság kizárása** (6.1, 6.2) — Ptk. 6:143. § előreláthatósági korlát **kizárása vitatható**
7. **Aszimmetrikus felelősség** (6.3) — 50 000 Ft cap a megrendelőre
8. **ÁSZF egyoldalú módosítása** (7.2) — Ptk. 6:78. § szerint a tisztességtelen ÁSZF kikötés **érvénytelen**
9. **Aszimmetrikus felmondás** (8.1, 8.2) — kliens azonnal, vállalkozó 90 nappal
10. **Megrendelő székhelye szerinti kizárólagos illetékesség** (9.2) — gyakori, de fogyasztói/gyengébb fél esetén támadható

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság |   /5 | _Hány találat: _ /10_ |
| Magyar jog ismerete (idéz-e Mt./Ptk./Szjt.?) |   /5 | **KRITIKUS** |
| Magyarázat minősége |   /5 | |
| Akciók |   /5 | |
| Megjelenés |   /5 | |
| **ÖSSZESEN** | **  /25** | |

**Kritikus kérdés:** Felismerte-e a **színlelt szerződést** (bujtatott munkaviszony)? □ Igen / □ Nem
**Kritikus kérdés:** Idéz-e **konkrét magyar jogszabályt** (pl. Ptk., Mt., Szjt.)? □ Igen / □ Nem

---

## TESZT 5: Albérleti szerződés (HU)

**Fájl:** `contracts-hu/alberleti_szerzodes.md`

<details>
<summary>Megoldó kulcs (magyar specifikus!)</summary>

1. **6 havi kaució** (3.1) — szokatlanul magas, jogi szürke zóna (Ptk. 6:343. §)
2. **Egyoldalú bérletidíj-emelés** (2.2) — határozott időtartamban **tilos** módosítani
3. **Bejelentkezés megtagadása** (6.1) — **alkotmányos jog**, érvénytelen kikötés (Btk.: lakóhely bejelentési kötelezettség)
4. **NAV-bejelentés elhallgatása** (6.2) — adócsalási kockázat a bérbeadónak, megtévesztés a bérlőnek
5. **Bérlő minden javítást fizet, inkl. szerkezeti** (5.1) — Ptk. 6:332. § szerint a **bérbeadó kötelezettsége** a rendeltetésszerű használatra alkalmas állapot
6. **Vis maior kárt is bérlő viseli** (10.2) — Ptk. ellenes
7. **Bérbeadó bármikor beléphet** (8.1) — **birtoksértés**, Ptk. ellenes
8. **Háziállat tartás abszolút tilalma + büntetés** (7.3) — vitatható
9. **Egyoldalú szabálymódosítás** (7.1) — tisztességtelen
10. **8 napos felmondás bérbeadó részéről** (9.1) — túl rövid
11. **Bérlő nem mondhatja fel + teljes hátralévő díj** (9.2) — kárenyhítés hiánya (Ptk. 6:144. §)
12. **Auto-renewal Bérbeadó által meghatározott új díjjal** (11.1)

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság |   /5 | _Hány találat: _ /12_ |
| Magyar jog ismerete |   /5 | **KRITIKUS** |
| Magyarázat minősége |   /5 | |
| Akciók |   /5 | |
| Megjelenés |   /5 | |
| **ÖSSZESEN** | **  /25** | |

**Kritikus kérdés:** Felismerte-e a **bejelentkezési jog megtagadásának** súlyosságát? □ Igen / □ Nem
**Kritikus kérdés:** A Ptk.-ra hivatkozik-e a karbantartási probléma kapcsán? □ Igen / □ Nem

---

## TESZT 6: SaaS szerződés (HU/EU/GDPR)

**Fájl:** `contracts-hu/saas_szerzodes.md`

<details>
<summary>Megoldó kulcs</summary>

1. **GDPR 28. cikk explicit kizárás** (4.2) — DPA hiánya, **érvénytelen + GDPR-sértés**
2. **Adatkezelési tájékoztató "később" + egyoldalú módosítás** (4.1) — átláthatóság alapelv sérülése (GDPR 5. cikk)
3. **EU-n kívüli adattovábbítás megfelelő garanciák nélkül** (4.3) — **GDPR 44-49. cikkek sértése** (SCC vagy adequacy szükséges)
4. **30 napos incidens-bejelentés** (4.4) — **GDPR 33. cikk: 72 óra a hatóságnak**!
5. **Érintetti kérelmek elutasítása** (4.5) — GDPR 12-22. cikkek sértése
6. **Al-adatfeldolgozó lista hiánya** (4.6) — GDPR 28(2) sértése
7. **Adatok korlátlan AI training-re** (3.2.b) — célhoz kötöttség sértése
8. **Adatok harmadik feleknek** (3.2.c)
9. **30 000 Ft felelősségi cap szándékos szerződésszegésre is** (7.1, 7.2) — Ptk. 6:152. § szerint **szándékos károkozásért a felelősség nem korlátozható**
10. **EU fogyasztói jogok kifejezett kizárása** (9.1) — érvénytelen
11. **Választottbíróság Szingapúrban** (9.2) — EU-ban gyengébb fél javára támadható
12. **3 éves auto-renewal új díjjal** (8.2)
13. **Felhasználói visszajelzés ingyen átszáll** (5.2)

</details>

### Értékelés (1-5)

| Kritérium | Pontszám | Jegyzet |
|---|---:|---|
| Találat-pontosság |   /5 | _Hány találat: _ /13_ |
| GDPR-ismeret (cikkek idézése!) |   /5 | **KRITIKUS** |
| Magyarázat minősége |   /5 | |
| Akciók |   /5 | |
| Megjelenés |   /5 | |
| **ÖSSZESEN** | **  /25** | |

**Kritikus kérdés:** Felismerte-e a **72 órás GDPR bejelentési kötelezettséget**? □ Igen / □ Nem
**Kritikus kérdés:** Idézte-e a **GDPR 28. cikket** (DPA)? □ Igen / □ Nem
**Kritikus kérdés:** Felismerte-e, hogy szándékos szerződésszegésre **nem lehet** felelősséget korlátozni? □ Igen / □ Nem

---

## ÖSSZEGZÉS

| Teszt | Pontszám | Találatok |
|---|---:|---:|
| 1. Freelancer (EN) |   /25 |   /7  |
| 2. Apartment (EN) |   /25 |   /10 |
| 3. SaaS MSA (EN) |   /25 |   /12 |
| 4. Vállalkozói (HU) |   /25 |   /10 |
| 5. Albérlet (HU) |   /25 |   /12 |
| 6. SaaS (HU/EU) |   /25 |   /13 |
| **ÖSSZESEN** | **  /150** | **  /64** |

---

## DÖNTÉSI MÁTRIX

| Eredmény | Mit jelent | Következő lépés |
|---|---|---|
| **120+/150 pont, 75%+ találat** | 🟢 **GO** — Az engine eladásra érett | SaaS frontend építés indul |
| **90-119/150, 50-75% találat** | 🟡 **TUNE** — Az engine alap jó, de finomítás kell | Custom playbook írás szegmensenként, hiányzó red flag patterns hozzáadása |
| **60-89/150, 30-50% találat** | 🟠 **REBUILD** — Az engine logikája gyenge | Saját Claude API prompt írása, sokkal több testreszabás |
| **<60/150** | 🔴 **PIVOT** — Más ötlet vagy más alap | Másik repo keresése, vagy más vertikum |

---

## ELTÉRŐ TELJESÍTMÉNY EN vs. HU?

| | EN átlag | HU átlag | Eltérés |
|---|---:|---:|---:|
| Találat % | __% | __% | |
| Magyarázat | __ /5 | __ /5 | |

**Ha HU jelentősen rosszabb:** lokalizált playbook kell magyar jogszabályokkal (Ptk., Mt., Szjt., GDPR).
**Ha HU jó:** mehet a magyar piac is első körben.

---

## SZEGMENS-AJÁNLÁS

A legjobb teljesítményű szegmens(ek) alapján:

- **Ha freelancer/SaaS MSA erős, lakásbérlés gyenge** → B2B szegmens prioritás
- **Ha lakásbérlés erős** → Consumer/individual szegmens életképes
- **Ha mindegyik közepes** → Egy szegmensre fókusz, mély playbook

---

## SZABAD SZÖVEGES MEGJEGYZÉSEK

_(Mit éreztél? Mi lepett meg? Mi hiányzott? Melyik szegmensen lennél lelkes az eladást elképzelni?)_
