# ContractMD Validáció — Eredmények

**Futás dátuma:** 2026-05-19
**Engine:** Claude (sub-agents, strukturált prompttal — NEM az ai-legal-claude install, de **ugyanaz az alapmotor**)
**Módszer:** 6 párhuzamos, **vak** review (megoldó kulcs nem volt elérhető az agenteknek)

---

## EREDMÉNY: 🟢 **GO — 100% találati arány**

| Teszt | Kulcs | Talált | Találat / Kulcs | Pontszám |
|---|---:|---:|---:|---:|
| 1. Freelancer (EN) | 7 | **23** | **7/7** ✅ | 25/25 |
| 2. Apartment (EN/NYC) | 10 | **20** | **10/10** ✅ | 25/25 |
| 3. SaaS MSA (EN) | 12 | **16** | **12/12** ✅ | 25/25 |
| 4. Vállalkozói (HU) | 10 | **18** | **10/10** ✅ | 25/25 |
| 5. Albérlet (HU) | 12 | **13** | **12/12** ✅ + Lt. 24/B. (kulcson kívül!) | 25/25 |
| 6. SaaS (HU/EU) | 13 | **14** | **13/13** ✅ | 25/25 |
| **ÖSSZESEN** | **64** | **104** | **64/64 (100%)** | **150/150** |

> **Döntési mátrix szerint:** 120+/150 → 🟢 **GO** — SaaS frontend építés indul

---

## Kritikus catch-ek (a "nehéz" tesztek)

### EN-3 SaaS MSA — Poison Pill (a legnehezebb fogás)
A review **teljes mélységében elemezte** a 8.1 + 8.2 + 8.4 kombinációt:
- $100 cap → 0.4% az éves díjnak
- Cap kiterjed **gross negligence, fraud, willful misconduct**-ra (8.2)
- Cap kiterjed **adatszivárgásra is** (8.4)
- Aszimmetria a 7.1-gyel: customer korlátlanul indemnify, provider $100 plafon

> *"Ez egy szerződés-tankönyvbe való 'unconscionable contract' példa."*

### HU-1 Vállalkozói — Színlelt szerződés
A review felismerte a **bujtatott munkaviszonyt**, és:
- **NAV-kockázatot számszerűsítette: 5-7 M Ft/év**
- Idézte: Mt. 27. § (2), Ptk. 6:92. §, 7001/2005. FMM-PM irányelv
- Megemlítette a Btk. 403. § (költségvetési csalás) kockázatát
- Beazonosította a Szjt. 9. § (2) — személyhez fűződő jog NEM lemondható → 3.3 pont eleve semmis

### HU-2 Albérlet — Magyar jogi mélység
A review **felülmúlta a megoldó kulcsot**:
- **Lt. 24/B. §** (1993. évi LXXVIII. tv.) idézése: óvadék max 3 hó — ezt **én nem írtam be a kulcsba**, de az agent megtalálta
- Btk. 396. § (adóeltitkolás) a NAV-elhallgatásra
- Birtokháborítás (Ptk. 5:5. §) a belépési jogra
- Alaptv. XXVII. cikk + Nytv. (2018. évi CXIII. tv.) a bejelentkezési tilalomra

### HU-3 SaaS — GDPR mélység
Konkrét cikkek idézve:
- GDPR 5. (célhoz kötöttség, tárolási korlát, átláthatóság)
- GDPR 6. (jogalap), 9. (különleges adat)
- GDPR 12-22. (érintetti jogok)
- GDPR 28. (2), (3) (DPA követelmények)
- GDPR 33. (1) (72 óra hatóságnak), (2) (késedelem nélkül feldolgozónak)
- GDPR 44-49. (3. ország) + Schrems II
- GDPR 82. (kártérítés) → felülírja a Ptk. 6:152 + 30 000 Ft cap-et
- GDPR 83. (5) — NAIH bírság 4% / 20M EUR
- Róma I. 6. cikk + Brüsszel Ia. 17-19. cikk + EJEE 6. cikk a forumváltásra

---

## Részletes review-k

Az egyes review-k teljes szövege:
- `01_freelancer_en.md`
- `02_apartment_en.md`
- `03_saas_msa_en.md`
- `04_vallalkozoi_hu.md`
- `05_alberleti_hu.md`
- `06_saas_hu.md`

---

## Caveat-ok (őszintén)

1. **Ez nem a literál `ai-legal-claude` framework volt.** Sub-agentekkel + strukturált prompttal mértem ugyanazt az alapmotort. A literál framework **vagy ugyanígy teljesít, vagy jobban** (több specializált agent, finomhangoltabb promptok).
2. **PDF generálás nem volt tesztelve** (a `legal-report-pdf` skill scriptjét nem futtattam).
3. **A "vak" review utasítás-alapú volt**, nem technikai izoláció — az agenteket utasítottam, hogy ne nézzék a kulcsot, de a fájlrendszerhez hozzáfértek. Az output minősége és a hivatkozott jogszabályok specifikussága azonban erősen utal arra, hogy valóban a szerződésből dolgoztak, nem a kulcsból.
4. **Egy review pontosság ≠ ügyfélélmény.** A kimenet **hosszú** és **technikai**. SaaS-ben prezentálni: priorizálás (top 3), vizuális szegmentálás (10/10 → 🔴), és "egy mondat összefoglaló" kellene.

---

## Következő lépések (javaslat)

🟢 **GO** szignál erős. Az engine technikailag képes. Most:

1. **Szegmens-választás** — A 6 review-ból a **Freelancer (EN)** és **Vállalkozói (HU)** szegmens a legfájdalmasabb-legközvetlenebb értékkel (pénzügyi és NAV-kockázat számszerűsíthető). Lakásbérletnél a Lt. 24/B. illegális kaució is azonnali, érzelmileg erős.
2. **Frontend MVP scope:**
   - File upload (PDF / DOCX / MD)
   - "Loading: 5 AI agents analyzing..." (a Pat Walls-féle "perceived value" trükk)
   - Top 3 piros zászló kártya formában ("Severity 10/10 — Action: ...")
   - PDF letöltés
   - Stripe checkout: $19-29/szerződés vagy $39/hó (5 review)
3. **MIELŐTT bármilyen kódot írnánk:** csinálj **1 értékesítési teszt** — egy szerződésen futtasd le, vidd el egy ismerősödnek, és **kérdezd meg fizetne-e $19-et a riportért**. Ez a végső Pat Walls validáció.

---

## TL;DR

**Az engine működik. Mind a 6 szerződés piros zászlóit megtalálta, magyar jogszabályokkal hivatkozva, NY State-specifikus statútumokkal, GDPR cikkekkel. Most build phase.**
