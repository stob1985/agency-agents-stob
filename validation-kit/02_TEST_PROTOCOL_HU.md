# ContractMD – Teszt Protokoll

## A teszt célja

Megvizsgálni, hogy az `ai-legal-claude` skill-szett kimenete **eladható minőségű-e**.

### A "Pat Walls" kritérium

Pat Walls vendégei mindig ezt kérdezik: *"Ha ezt megmutatnám egy potenciális ügyfélnek, hajlandó lenne $19-49-et fizetni érte havonta?"*

A válaszunk **csak akkor IGEN**, ha mindhárom teszt szerződésen:

✅ A kimenet legalább **80% pontos** (találja a valós piros zászlókat)
✅ A kimenet **érthető**, nem csak technikai zsargon
✅ A kimenet **akciókat ad**, nem csak listáz
✅ A PDF report **professzionálisan néz ki**

---

## 6 TESZT SZERZŐDÉS (3 EN + 3 HU)

A `contracts-en/` és `contracts-hu/` mappákban találsz mintákat. Az EN szerződések általános/US joghatóságra, a HU szerződések magyar/EU joghatóságra szólnak — szándékos, jellegzetes piros zászlókkal.

### EN-1. `contracts-en/freelancer_contract.md` – Solo Freelancer
- IP overreach (minden, akár kapcsolódik akár nem)
- 24 hónapos non-compete világszerte
- Uncapped indemnification + $100 liability cap = **poison pill**
- Aszimmetrikus termination, Net 90 fizetés

### EN-2. `contracts-en/apartment_lease.md` – NYC lakásbérlés
- **3 havi kaució (NY-ben ILLEGÁLIS, 2019-es Housing Stability Act)**
- Rejtett fees ($175 + $50 + $200)
- No mitigation duty (NY-ben kötelező)
- Bérlő fizet structural javítást is

### EN-3. `contracts-en/saas_msa.md` – B2B SaaS MSA
- **Customer Data AI training-re**
- GDPR explicit kizárás (4.2)
- 30 napos breach notice (GDPR: 72 óra!)
- $100 cap szándékos szerződésszegésre is = **legnehezebb poison pill**
- Arbitráció Szingapúrban, customer költségére

### HU-1. `contracts-hu/vallalkozoi_szerzodes.md` – Magyar vállalkozói
- **Színlelt szerződés gyanú** (heti 40 óra, kötelező iroda → bujtatott munkaviszony)
- 36 hónapos versenytilalom ellenérték nélkül
- Szerzői jog: névfeltüntetésről lemondás (érvénytelen Szjt. szerint)
- ÁSZF egyoldalú módosítása

### HU-2. `contracts-hu/alberleti_szerzodes.md` – Magyar albérlet
- 6 havi kaució
- **Bejelentkezési jog megtagadása** (alkotmányellenes kikötés)
- **NAV-bejelentés elhallgatása** (adócsalási kockázat)
- Vis maior kárt is bérlő viseli (Ptk. ellenes)
- Bérlő fizet szerkezeti javítást (Ptk. 6:332. § ellen)

### HU-3. `contracts-hu/saas_szerzodes.md` – EU/GDPR SaaS
- **GDPR 28. cikk explicit kizárás** (DPA hiánya)
- EU-n kívüli adattovábbítás megfelelő garanciák nélkül (44-49. cikk)
- 30 napos incidens-bejelentés (**GDPR 33. cikk: 72 óra**!)
- 30 000 Ft cap szándékos szerződésszegésre is (Ptk. 6:152. § ellen)
- Választottbíróság Szingapúrban

**A teljes piros zászló lista és pontozás:** lásd `EREDMENYEK_HU.md`.

---

## A TESZT MENETE

### Fázis 1: Setup (5 perc)

1. Klónozd le a kit-et:
   ```bash
   git clone -b claude/validate-core-engine-5AyzT https://github.com/stob1985/agency-agents-stob.git
   cd agency-agents-stob/validation-kit
   ```

2. Telepítsd az `ai-legal-claude` skill-szettet a `01_SETUP_HU.md` szerint.

3. Indítsd el Claude Code-ot a `validation-kit/` mappában:
   ```bash
   claude
   ```

### Fázis 2: A 6 teszt futtatása (~30 perc)

A Claude Code chat ablakban, sorban:

```
/legal review contracts-en/freelancer_contract.md
/legal review contracts-en/apartment_lease.md
/legal review contracts-en/saas_msa.md
/legal review contracts-hu/vallalkozoi_szerzodes.md
/legal review contracts-hu/alberleti_szerzodes.md
/legal review contracts-hu/saas_szerzodes.md
```

Mindegyik 1-2 perc (5 agent párhuzamosan dolgozik). A kimenetet jegyezd fel a `EREDMENYEK_HU.md` fájlba — minden szerződéshez van értékelő blokk + megoldó kulcs (kibontható, **NE nézz rá futtatás előtt**).

### Fázis 3: PDF report (5 perc)

Az utolsó teszt után:
```
/legal report-pdf
```

→ Megkapsz egy szépen szedett PDF-et
→ Ez az, amit egy ügyfél kapna a TE szolgáltatásodtól

### Fázis 4: Értékelés (5 perc)

Töltsd ki az `EREDMENYEK_HU.md` fájlt minden teszten.

---

## ÉRTÉKELÉSI KRITÉRIUMOK

Minden teszten értékeld 1-5-ig:

| Kritérium | Mi a kérdés? |
|---|---|
| **Találat-pontosság** | Megtalálta a beépített problémákat? |
| **Magyarázat minősége** | Egy nem-jogász is érti? |
| **Akciók** | Konkrét "mit csinálj most" tanácsok? |
| **Megjelenés** | Profi look, vagy zavaros markdown? |
| **PDF minőség** | Eladható lenne $14-29-ért? |

---

## DÖNTÉSI MÁTRIX (összes 6 tesztre)

| Eredmény (összes /150) | Mit jelent | Mi a következő |
|---|---|---|
| **120+/150** (75%+ találat) | 🟢 GO! Az engine kész | SaaS frontend építés |
| **90-119/150** (50-75% találat) | 🟡 Tuning kell | Egyedi playbook írás szegmensenként |
| **60-89/150** (30-50% találat) | 🟠 Rebuild | Saját Claude API prompt logika |
| **<60/150** | 🔴 Más alap kell | Más repo vagy más vertikum |

> **EN vs HU külön nézd:** ha a HU jelentősen rosszabb, magyar jogszabály-playbook kell (Ptk., Mt., Szjt., GDPR). Ha EN-ben erős és HU-ban gyenge → indulj US piaccal először.

---

## KÖVETKEZŐ LÉPÉS

Ha kész vagy a teszttel, küldj nekem screenshotokat / másold be a kimeneteket, és **eldöntjük együtt**:
- Milyen szegmenssel kezdjünk
- Kell-e custom playbook
- Mit építünk frontendet köré

Hajrá! 🚀
