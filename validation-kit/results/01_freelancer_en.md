# REVIEW: Freelancer Contract (EN)

**Agent:** Blind review (general-purpose sub-agent)
**Talált piros zászlók:** 23
**Kulcs:** 7 → **mind benne**

---

## 1. PIROS ZÁSZLÓK

1. **Klauzula:** 1.2 — Scope expansion at Client's sole discretion
   - **Probléma:** A Megbízó egyoldalúan, ingyenesen kibővítheti a munkakört. Ez korlátlan, fizetés nélküli munkát jelent.
   - **Súlyosság:** 9
   - **Akció:** Törölni. Helyette: minden scope-bővítés írásos change order + külön díjazás.

2. **Klauzula:** 1.3 — 40 óra/hét + szombat is elérhetőség
   - **Probléma:** A 40 órás minimum heti elérhetőség és Mon-Sat 9-19 ET ablak gyakorlatilag alkalmazotti jogviszonyt teremt (misclassification risk), miközben a 9.1 szerint nem jár alkalmazotti juttatás.
   - **Súlyosság:** 8
   - **Akció:** Törölni a kötelező órakeretet és a szombatot; a vállalkozó maga osztja be idejét.

3. **Klauzula:** 2.2 — Net 90 + utólagos vitatás
   - **Probléma:** 90 napos fizetési határidő iparági átlag fölött; ráadásul Client „bármikor, akár utólag is" vitathatja az invoice-t — gyakorlatilag visszakövetelhet kifizetett pénzt időkorlát nélkül.
   - **Súlyosság:** 9
   - **Akció:** Net 15-30 napra módosítani; vitatás max. 10 napon belül, fizetés után nincs claw-back.

4. **Klauzula:** 2.3 — 25% performance reserve
   - **Probléma:** A számla 25%-át visszatarthatja „végátadásig", ami soha nem definiált. Cash-flow gyilkos.
   - **Súlyosság:** 7
   - **Akció:** Törölni, vagy max. 10% és konkrét milestone-okhoz kötni, fix határidővel.

5. **Klauzula:** 2.4 — Tax indemnity
   - **Probléma:** Vállalkozó megtéríti azokat az adókat is, amelyeket a Client-nek kellett volna levonni / befizetni — felelősség-áthárítás, jogellenes lehet US-ban (1099 vs W-2).
   - **Súlyosság:** 8
   - **Akció:** Csak saját 1099 adókért feleljen vállalkozó; Client felel az általa visszatartandó adókért.

6. **Klauzula:** 3.1 — IP "whether or not related to the Services"
   - **Probléma:** A vállalkozó MINDEN, a szerződés ideje alatt létrehozott szellemi terméke a Client-é, akkor is, ha nincs köze a munkához (pl. hobbi projekt, másik ügyfél, esti kód). Túl tág, sok államban érvénytelen (CA Labor Code 2870 jellegű védelem hiányzik).
   - **Súlyosság:** 10
   - **Akció:** Csak a Services keretében, munkaidőben, Client erőforrásával létrehozott művekre korlátozni. „Prior IP" listával védeni a meglévő anyagokat.

7. **Klauzula:** 3.2 — Pre-existing IP automatic assignment
   - **Probléma:** A vállalkozó korábban már létező IP-jét is „átruházza", amint az bekerül a projektbe — ez kisajátítja a vállalkozó saját könyvtárait/eszközeit.
   - **Súlyosság:** 9
   - **Akció:** Csere licencre: nem-kizárólagos, örökös licenc a Client-nek a pre-existing IP-re; a tulajdon a vállalkozónál marad.

8. **Klauzula:** 3.3 — At Contractor's expense
   - **Probléma:** A jogátruházáshoz szükséges adminisztrációt is a vállalkozó fizeti.
   - **Súlyosság:** 4
   - **Akció:** Client viseli a perfecting költségeket.

9. **Klauzula:** 3.4 — Moral rights waiver
   - **Probléma:** Sok jogrendben (EU, HU) a személyhez fűződő jog nem lemondható; általában elfogadott US-ban, de globális kontextusban gondot okozhat.
   - **Súlyosság:** 3
   - **Akció:** Korlátozni az érvényesíthető joghatóságokra.

10. **Klauzula:** 4.1 + 4.3 — Perpetual confidentiality
    - **Probléma:** Az időbeli korlát nélküli titoktartás (örökre) szokatlan és túlzott; szokásos 2-5 év.
    - **Súlyosság:** 6
    - **Akció:** Max. 3-5 év szerződés után, kivéve trade secret-eket, amíg azok titokban maradnak.

11. **Klauzula:** 4.2 — Túl tág Confidential Information definíció
    - **Probléma:** Bármi, amit a vállalkozó észlel, megjelölés nélkül is bizalmas — gyakorlatilag minden tudást „bezár".
    - **Súlyosság:** 6
    - **Akció:** Csak írásban jelölt vagy ésszerűen bizalmasnak tekinthető anyag; standard kivételek (publikus, függetlenül megszerzett, stb.).

12. **Klauzula:** 5.1 — 24 hónapos, világméretű non-compete
    - **Probléma:** 24 hó + „anywhere in the world" + minden ügyfél/prospect/vendor — túl széles. Delaware-ben is megtámadható, CA-ban semmis, FTC 2024-es szabálya ellen is megy. Megakadályozza, hogy a vállalkozó a szakmájában dolgozzon.
    - **Súlyosság:** 10
    - **Akció:** Törölni a non-compete-et; max. 6-12 hó non-solicit a direkt ügyfeleknél, földrajzilag és tevékenységileg szűkítve.

13. **Klauzula:** 5.2 — Waiver of overbreadth defense
    - **Probléma:** Előre lemond a védelemről — sok bíróság érvénytelennek tartja, de elrettentő hatású.
    - **Súlyosság:** 7
    - **Akció:** Törölni.

14. **Klauzula:** 6.1-6.2 — Uncapped, egyoldalú indemnification
    - **Probléma:** A vállalkozó korlátlanul kártalanít MINDEN harmadik fél követelésért, akár nem is a saját hibájából (pl. Client utasítására tett lépés). Nincs reciprocitás.
    - **Súlyosság:** 10
    - **Akció:** Csapdát csökkenteni: csak bizonyított vállalkozói gondatlanságra/szándékos hibára; cap = szerződéses díj 1x-e; kölcsönös indemnification; Client védi a saját utasításait.

15. **Klauzula:** 7.1 — $100 liability cap a Client oldaláról
    - **Probléma:** Aszimmetrikus: Client felelőssége $100-ra korlátozva, vállalkozóé korlátlan (6.2). Még a meg nem fizetett számlák behajtása is $100-ban maximalizálva.
    - **Súlyosság:** 10
    - **Akció:** Tükörkép: vagy mindkét fél felelőssége korlátozott (szerződéses díj értékében), vagy a fizetési kötelezettség kifejezetten kivételként kezelve.

16. **Klauzula:** 8.1 vs 8.2 — Aszimmetrikus felmondás
    - **Probléma:** Client azonnal, indok és értesítés nélkül felmondhat; a vállalkozó csak 90 nappal előre, és csak ha minden „Client megelégedésére" befejeződött (szubjektív).
    - **Súlyosság:** 9
    - **Akció:** Mindkét félnek azonos, ésszerű felmondási idő (pl. 15-30 nap); a vállalkozó megkapja a teljesített munka ellenértékét.

17. **Klauzula:** 8.3 — Forfeiture + transition fee
    - **Probléma:** Vállalkozói felmondás esetén elveszti a kifizetetlen díjakat ÉS fizet 2 havi átlagdíjat. Ez bírság, valószínűleg jogellenes (penalty clause).
    - **Súlyosság:** 10
    - **Akció:** Törölni; a már teljesített munkáért minden esetben jár a díj.

18. **Klauzula:** 9.2 — Policies/dress code
    - **Probléma:** Az IRS / DOL faktor-tesztek szerint ez közvetlen kontroll = alkalmazotti jelleg. Misclassification kockázat.
    - **Súlyosság:** 7
    - **Akció:** Csak biztonsági / titoktartási / on-site szabályokra korlátozni.

19. **Klauzula:** 10.3 — Aszimmetrikus attorney fees
    - **Probléma:** Ha Client nyer, a vállalkozó fizeti; ha vállalkozó nyer, mindenki a sajátját. Egyirányú „loser pays".
    - **Súlyosság:** 8
    - **Akció:** Vagy kölcsönös prevailing-party szabály, vagy „each party bears own fees".

20. **Klauzula:** 10.4 — Jury + class action waiver
    - **Probléma:** Standard nagyvállalati záradék, de a class waiver elvághatja a kollektív misclassification igényeket.
    - **Súlyosság:** 5
    - **Akció:** Class waiver-t törölni; jury waiver megtárgyalható.

21. **Klauzula:** 10.2 — Delaware fórum
    - **Probléma:** Ha a vállalkozó nem DE-i, kényszerített fórum drága peresedés esetén.
    - **Súlyosság:** 5
    - **Akció:** A vállalkozó székhelye szerinti fórum vagy semleges arbitráció.

22. **Klauzula:** 11.1 — Egyoldalú módosítás
    - **Probléma:** Client bármikor egyoldalúan módosíthatja a szerződést, és a folytatólagos munka „elfogadás". Ez a szerződés jellegét kérdőjelezi meg (illusory contract).
    - **Súlyosság:** 10
    - **Akció:** Törölni; minden módosítás kölcsönös írásos megegyezést igényel.

23. **Klauzula:** 11.2 — Egyoldalú assignment
    - **Probléma:** Client szabadon átruházhatja a szerződést (pl. felvásárláskor), a vállalkozó nem.
    - **Súlyosság:** 4
    - **Akció:** Kölcsönös; vagy legalább a vállalkozó hozzájárulása versenytárs felé történő átruházáshoz.

## 2. ÖSSZEFOGLALÓ

- **Total red flags found:** 23
- **Top 3 most dangerous (by score 10):**
  1. **3.1** — Korlátlan IP-átruházás munkán kívüli alkotásokra is
  2. **5.1** — 24 hó / világméretű non-compete
  3. **6 + 7.1** — Korlátlan kártalanítás vállalkozó részéről, $100 plafon Client részéről (aszimmetria)
- **Overall assessment:** **Nem** — jelenlegi formájában aláírhatatlan. **Csak ha módosítják** legalább a top 8 piros zászló (1.2, 2.2, 3.1, 5.1, 6, 7.1, 8.1-8.3, 11.1) tekintetében lényegesen.

## 3. HIÁNYZÓ VÉDELEM

- **Limitation of liability a vállalkozó oldalán** — nincs cap a vállalkozó felelősségére (szerződéses díj 1x szokásos).
- **Mutual indemnification** — Client nem kártalanítja a vállalkozót a saját utasításai / saját anyagai miatti igényekért.
- **Kill fee / cancellation fee** — Client azonnali felmondása esetén semmilyen minimum kifizetés.
- **Late payment interest** — nincs késedelmi kamat Net 90 ellenére.
- **Acceptance / deliverables definíció** — „final acceptance" nincs definiálva, deemed acceptance záradék kell.
- **Insurance** — nincs előírva sem Client, sem vállalkozó felelősségbiztosítása.
- **Audit / record-keeping korlátozás** — nincs szabályozva.
- **Portfólió / referencia jog** — vállalkozó nem mutathatja be a munkát a portfóliójában.
- **Force majeure** — egyáltalán hiányzik.
- **Sublicense / subcontractor jog** — nincs szabályozva.
- **Data protection / GDPR** — adatkezelési záradék hiányzik.
- **Background IP / Contractor tools lista** — nincs Schedule, ahol a vállalkozó listázhatná a már meglévő IP-jét.
- **Notice mechanism** — formális értesítési cím / mód nincs definiálva.

---

## PONTOZÁS

| Kritérium | Pontszám | Megjegyzés |
|---|---:|---|
| Találat-pontosság (kulcs: 7) | 5/5 | Mind a 7 megvan + 16 extra |
| Magyarázat minősége | 5/5 | Konkrét, érthető |
| Akciók | 5/5 | Minden flag-hez konkrét javaslat |
| Megjelenés | 5/5 | Strukturált markdown |
| PDF minőség | N/A | Nem volt PDF generáció |
| **ÖSSZESEN** | **25/25** | |
