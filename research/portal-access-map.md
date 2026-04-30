# Magyar ingatlan-portál térkép — kutatási hozzáférés-mátrix

**Cél:** lefedni a teljes magyar ingatlan-piaci adatszerzési felületet, jelölve melyik portál működik WebFetch-csel és melyik blokkol.

## Tier 1 — fő piactéri portálok

| Portál | URL | WebFetch hozzáférés | Inventory mélység | Egyedi adatok |
|---|---|---|---|---|
| **ingatlan.com** | ingatlan.com | ❌ 403 (Cloudflare anti-bot) | Magyar piac #1 (~80% lefedettség) | – |
| **Zenga** | zenga.hu | ✅ működik | **Nagy**, jól kategorizált | OTP Bank backend, megbízható |
| **Ingatlanok.hu** | ingatlanok.hu | ✅ működik | Közepes | Külön szegmentált adatok |
| **Otthontérkép** | otthonterkep.hu | ⚠️ csak főoldal, megye-szintű szűrés nehéz | **68 000+** listing | Térképes overlay |
| **Ingatlantájoló** | ingatlantajolo.hu | ✅ működik | Nagy | Lista-szintű ár-aggregátor |
| **Ingatlanok360** | ingatlanok360.hu | ✅ működik | Közepes | – |
| **Ingatlanbazár** | ingatlanbazar.hu | ⚠️ keresés nehéz | n.a. | – |
| **Ingatlankereső** | ingatlankereso.hu | ⚠️ nem teszteltem | n.a. | – |

## Tier 2 — ingatlanos hálózat portálok

| Portál | URL | WebFetch | Mit ad többletet |
|---|---|---|---|
| **Duna House** | dh.hu | ✅ | **Egyedi listing-leírás minden telken HÉSZ-jelöléssel** (best-in-class részletek) |
| **Otthon Centrum** | oc.hu | ✅ | Telepi exclusive listingek |
| **MIK Magyar Ingatlan Központ** | mik.hu | ⚠️ | Saját Béta-fázis |
| **Lakáscentrum** | lakascentrum.hu | ⚠️ 404 a lokáció-URL-eken | Nem skálázható |

## Tier 3 — apróhirdetés / aggregátor

| Portál | URL | WebFetch | Mit ad |
|---|---|---|---|
| **Jófogás Ingatlan** | ingatlan.jofogas.hu | ✅ | **Magánhirdető** dominancia (off-market potenciál) |
| **Trovit** | ingatlan.trovit.hu | ✅ | Keresztaggregátor sok forrásból |
| **Megveszlak** | megveszlak.hu | ✅ | Egyedi link mindenhez, könnyen olvasható |
| **Maxapro** | maxapro.hu | ⚠️ 404 a részleteken | Nem megbízható |
| **Költözz be** | koltozzbe.hu | ✅ | Filterelt listák |
| **Realestatehungary** | realestatehungary.hu | ✅ | Angol nyelvű frontend |
| **Ingatlannet** | ingatlannet.hu | ❌ 403 | Bot-blokk |

## Tier 4 — speciális / albérleti

| Portál | URL | Fókusz |
|---|---|---|
| **Albérlet** | alberlet.hu | Bérleti fókusz (exit-comp számoláshoz hasznos) |
| **Otthonkereső** | otthonkereso.hu | Vegyes |
| **Ingatlanmagazin** | ingatlanmagazin.com | Cikkek + piacelemzés (nem direkt listingek) |
| **Ingatlanjelentés** | ingatlanjelentes.hu | Aggregált piaci jelentések |
| **e-Ingatlanközvetítők** | e-ingatlankozvetitok.hu | Brókerek aggregátora |

## Új találatok a Zenga-ról (előzetes Székesfehérvár csekkolás)

A Zenga **82 telket** mutat Székesfehérvárra, szemben a dh.hu **24** és ingatlanok.hu **8** találatával — érdemi multipler. Új jelöltek a Székesfehérvár-auditba beépítendők:

| Lokáció | Méret | Ár | e Ft/m² | Megjegyzés |
|---|---|---|---|---|
| **Központi 9700 m²** | 9700 | 164,9 M | **17** | **NAGYON OLCSÓ** — fejlesztési potenciál esetén |
| Központi 1461 m² | 1461 | 48,9 M | 33 | építhető |
| Palotaváros 530 m² | 530 | 26,9 M | 51 | premier listing |
| Feketehegy 1398 m² | 1398 | 18 M | 13 | gyanúsan olcsó (lehet 3% külterület!) |
| Maroshegy 488 m² | 488 | 35 M | 72 | drága |
| Maroshegy 810 m² | 810 | 5,8 M | 7 | gyanúsan olcsó (külterület) |

> A **Központi 9700 m² @ 164,9 M Ft (17 e Ft/m²)** ár-méret arány alapján potenciálisan a legjobb jelölt — ha a HÉSZ Lk-1/Lk-2/Vt és nem zártkert.

## Új találatok az Ingatlanok.hu-ról

Veszprém:
- **Veszprém Belváros (kertvárosias) 800 m² @ 22 M Ft** (28 e Ft/m²) — Lke övezet (32-szer megerősítve)
- **Veszprém történelmi belváros 1811 m² @ 209 M Ft** (115 e Ft/m²) — drága, de **valódi belvárosi**, „összközműves"
- **Veszprém-Jutaspusztán 974 m² @ 39,9 M Ft** ← **a te általad ellenőrzött telek**, helyesen nem Belváros, hanem **Jutaspuszta**
- **Veszprém-Csatárhegyen 985 m² @ 24 M Ft** — zártkerti

## Stratégiai következmény a kutatás-módszertanra

Eddigi kutatásom **alulmintázott** — főleg dh.hu-t és ingatlantajolo-t használtam, ami a teljes piac ~30%-át fedi le. A **zenga.hu az új belépő**, ami 3-4× nagyobb mélységet ad. Az **ingatlan.com** eléréséhez vagy:
- Felhasználói login-token (a te ingatlan.com fiókod) — én nem érem el
- Manuális keresés és copy-paste — a te oldaladon
- **Trovit, Zenga, Otthontérkép** kombináció — nagyrészt fedi az ingatlan.com állományt másodlagos forrásként

## Mit javaslok következő lépésnek

**A.** Folytassam a **Zenga** alapú audit-ot Székesfehérváron (a 82 listing áttekintése a 25%+ margin szűrővel), majd ugyanezt **Vác / Kecskemét / Tatabánya** városokra

**B.** Ha tudsz adni egy **ingatlan.com saját keresési URL-t** (a te szűrőiddel), abból is olvasok — én csak a publikus eléréseket tudom használni

**C.** **Off-market csatornákra** (Jófogás magánhirdető, helyi DH/OC vezetők) átállás — a hirdetett piacban a 25% margin telek-jelölt sok megyében hiánycikk

Melyiket?
