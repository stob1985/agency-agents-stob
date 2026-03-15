# Ingatlan.com Budapest Scraper

Playwright-alapú, emberi viselkedést utánzó ingatlan scraper.

## Keresési feltételek

| Feltétel | Érték |
|---|---|
| Kerületek | I., II., XI. (Sasad & Bartók Béla), XII. |
| Max ár | 120M Ft |
| Max nm-ár | 1,4M Ft/m² |
| Min emelet | 1. emelet |
| Lift | kötelező 2. emelettől |
| Épület kora | 1950 előtt VAGY 1980 után |
| Kilátás | utcai / kertre néző / panorámás |
| Állapot | felújítandó vagy befejezetlen |

## Telepítés

```bash
pip install playwright playwright-stealth
playwright install chromium
```

## Futtatás

```bash
python3 scraper.py
```

Az eredmények a `results/` mappában kerülnek mentésre JSON és CSV formátumban.

## Anti-detektálás technikák

- `playwright-stealth`: elrejti az automatizálás nyomait
- Véletlenszerű késések oldalak és kártyák között
- Emberi görgetés és egérmozgás szimulálás
- Magyar böngésző locale és User-Agent
- Főoldal meglátogatása induláskor (természetes belépési pont)
- 10–25 mp szünet kerületek között
