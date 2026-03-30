---
name: DeFi Pool Kutatás - Ethereum Mainnet
description: Volatile token + stablecoin LP pool elemzés nagy tőke számára, fedezési stratégiákkal
date: 2026-03-30
chain: Ethereum
source: DefiLlama Yields API
---

# DeFi Pool Kutatás — Volatile Token + Stablecoin párok (2026.03.30)

## Összefoglaló

Az alábbi kutatás az Ethereum mainnet **volatile token + stablecoin** liquidity pool párokat vizsgálja (pl. ETH/USDC, WBTC/USDT). Cél: melyik poolba érdemes nagyobb tőkével belépni, és hogyan fedezd a pozíciódat.

---

## 1. Blue Chip token + Stablecoin poolok (nagy TVL, megbízható)

### ETH + Stablecoin párok

| Pool | Protokoll | TVL | APY | 30d átlag APY | Fee tier |
|------|-----------|-----|-----|---------------|----------|
| **USDC-WETH** | Uniswap V3 | **$97.8M** | 40.60% | 43.91% | Concentrated |
| **WETH-USDT** | Uniswap V3 | **$67M** | 29.05% | 43.82% | Concentrated |
| **crvUSD-WETH** | Curve-DEX | **$45.4M** | 5.69% | 7.27% | Full range |
| **ETH-USDC** | Uniswap V4 | **$29.7M** | 14.86% | 20.72% | Concentrated |
| **USDC-WETH** | Uniswap V3 | $23.6M | 15.09% | 25.83% | Concentrated |
| **USDC-WETH** | Uniswap V2 | $18.6M | 5.49% | 6.61% | Full range |
| **WETH-USDT** | Uniswap V2 | $15.4M | 5.40% | 6.58% | Full range |
| **WETH-USDT** | Uniswap V3 | $8.4M | 43.34% | 38.96% | Concentrated |
| **USDC-ETH** | Fluid-DEX | $7.7M | 18.49% | 38.00% | Auto-managed |
| **DAI-WETH** | SushiSwap V3 | $8.4M | 15.09% | 17.93% | Concentrated |
| **ETH-USDT** | Uniswap V4 | $21M | 4.43% | 6.20% | Wide range |

### BTC + Stablecoin párok

| Pool | Protokoll | TVL | APY | 30d átlag APY | Fee tier |
|------|-----------|-----|-----|---------------|----------|
| **crvUSD-CBBTC** | Curve-DEX | **$176.3M** | 3.52% | 4.59% | Full range |
| **crvUSD-TBTC** | Curve-DEX | **$90.2M** | 3.56% | 4.44% | Full range |
| **crvUSD-WBTC** | Curve-DEX | **$89.4M** | 3.65% | 4.88% | Full range |
| **WBTC-USDC** | Uniswap V3 | $27.3M | 18.46% | 17.90% | Concentrated |
| **WBTC-USDT** | Uniswap V3 | $26M | 12.05% | 13.35% | Concentrated |
| **WBTC-USDT** | Uniswap V3 | $16M | 26.66% | 27.16% | Concentrated |
| **USDC-CBBTC** | Uniswap V4 | $10.2M | 13.94% | 25.48% | Concentrated |
| **WBTC-USDC** | Uniswap V4 | $8.7M | 18.79% | 35.65% | Concentrated |

### Arany (safe haven) + Stablecoin

| Pool | Protokoll | TVL | APY | 30d átlag APY |
|------|-----------|-----|-----|---------------|
| **XAUT-USDT** | Uniswap V3 | $9.1M | 11.21% | 22.95% |
| **PAXG-USDC** | Uniswap V3 | $4M | 23.08% | 20.62% |
| **PAXG-USDC** | Uniswap V3 | $2.5M | 17.46% | 32.01% |
| **XAUT-USDC** | Uniswap V4 | $3.5M | 5.23% | 14.75% |

### Egyéb kiemeltek

| Pool | Protokoll | TVL | APY | 30d átlag APY | Megjegyzés |
|------|-----------|-----|-----|---------------|------------|
| **LINK-USDC** | Uniswap V4 | $1.4M | 29.86% | 15.28% | Oracle token |
| **SKY-USDC** | Uniswap V4 | $1.4M | 40.19% | 50.01% | MakerDAO rebrand |
| **1INCH-USDC** | Uniswap V4 | $1M | 13.68% | 12.58% | DEX aggregátor |

---

## 2. Elemzés: Melyik poolba érdemes nagyobb tőkével belépni?

### A) Legalacsonyabb volatilitás egymáshoz képest → ARANY/USD poolok

**PAXG-USDC (Uniswap V3) — AJÁNLOTT alacsonyabb volatilitásra**
- Az arany (PAXG/XAUT) a legstabilabb "volatile" asset a stablecoinhoz képest
- Napi mozgás tipikusan 0.5-2%, szemben ETH 3-8%, BTC 2-5%
- APY: 17-23% (jó hozam, alacsonyabb IL kockázat)
- Hátrány: Kisebb TVL ($4M), nagy tőkével slippage

**XAUT-USDT (Uniswap V3)** — $9.1M TVL, jobb likviditás
- APY: 11.21% (30d átlag: 22.95%)
- Tokenized gold, alacsony volatilitás

### B) Legjobb hozam/kockázat arány → ETH/USDC

**USDC-WETH (Uniswap V3) — $97.8M TVL**
- A legnagyobb ETH/stablecoin pool, hatalmas likviditás
- APY: 40.60% (30d átlag: 43.91% — nagyon konzisztens!)
- Ide nagy tőkét is be lehet tenni slippage nélkül
- DE: Concentrated liquidity = aktívan kell kezelni a range-et
- IL kockázat: MAGAS ha ETH erősen mozog

**ETH-USDC (Uniswap V4) — $29.7M TVL**
- Újabb protokoll, jobb fee struktúra
- APY: 14.86% (30d: 20.72%)
- Kevésbé agresszív concentrated range = kevesebb kezelés

### C) Konzervatív nagy tőke → BTC/crvUSD (Curve)

**crvUSD-CBBTC (Curve-DEX) — $176.3M TVL**
- Legnagyobb BTC/stablecoin pool
- APY: 3.52% — alacsony, DE: full range (nincs range management)
- Set-and-forget: nem kell aktívan kezelni
- BTC volatilitása alacsonyabb mint ETH-é

---

## 3. Hosszú távú befektetési ajánlás

### Melyik párba érdemes hosszú távon belépni?

**Tier 1 — Hosszú távú hold (bikapiac + medvepiac is):**

| Pár | Miért | Kockázat |
|-----|-------|----------|
| **ETH/USDC** | ETH az egész DeFi alapja, hosszú távon felértékelődik, pool fee hozam magas | Magas IL medvepiacon |
| **WBTC/USDT** | BTC "digitális arany" narratíva, alacsonyabb vol mint ETH | Közepes IL |
| **PAXG/USDC** | Arany = infláció-védelem, legalacsonyabb IL a volatile tokenek közül | Alacsony IL, alacsonyabb APY |

**Tier 2 — Ciklikus (most érdemes, ha bullish):**

| Pár | Miért | Kockázat |
|-----|-------|----------|
| **LINK/USDC** | Oracle infrastruktúra, RWA boom hajtja | Közepes-magas IL |
| **SKY/USDC** | MakerDAO ökoszisztéma, 50% 30d avg APY | Magas volatilitás |

---

## 4. Fedezési (Hedging) stratégiák volatile+stablecoin poolokhoz

### A) Perp Short hedge (leggyakoribb)

```
Probléma: ETH/USDC poolban vagy → ha ETH esik, IL + értékvesztés
Megoldás: Short ETH perp pozíció az IL kompenzálására

Példa $100k tőkével ETH/USDC poolban:
1. Pool: $100k berakva (≈$50k ETH + $50k USDC)
2. Hedge: Short $25k ETH perp (Hyperliquid, dYdX, GMX)
   - 50%-os hedge = csökkenti az IL-t, de megtartja felfelé potenciált
   - 100%-os hedge ($50k short) = delta-neutral, csak fee income
3. Eredmény:
   - Ha ETH esik 20%: pool IL ≈ -0.6%, de short profit kompenzál
   - Ha ETH nő 20%: pool IL ≈ -0.6%, short loss, de pool ETH oldal nő
   - Mindkét esetben: fee income megmarad (30-40% APY)
```

### B) Options hedge (put vásárlás)

```
Probléma: Nem akarod aktívan kezelni a short-ot
Megoldás: ETH put opciók vásárlása

Példa:
1. Pool: $100k ETH/USDC
2. Vétel: 3 hónapos ETH put opció (strike: -15% jelenlegi ártól)
   - Költség: ~3-5% a védett összeg értékéből (negyedévente)
   - Protokollok: Lyra, Premia, Aevo
3. Ha ETH 15%-nál többet esik → put kompenzálja a veszteséget
4. Éves hedge költség: ~12-20% → a 40% APY-ból marad 20-28%
```

### C) Kétoldalú LP + lending hedge

```
Stratégia: Pool hozam + lending short kombinálása

1. $100k ETH/USDC Uniswap V3 pool (40% APY)
2. Kölcsönvesz $30k értékű ETH-t Aave-ről (collateral: USDC)
3. Az ETH-t eladja USDC-re → szintetikus short
4. Ha ETH esik: pool IL keletkezik, de a short nyereséges
5. Ha ETH nő: short veszít, de a pool ETH oldala nő
6. Net: fee income (30-40%) - kölcsön kamat (3-5%) = 25-35% net APY
```

### D) "Barbell" stratégia (ajánlott nagy tőkére)

```
Tőke elosztás:

40% — ETH/USDC (Uniswap V3, $97.8M TVL)
       APY: ~40%, aktív range management kell
       → Hozamtermelő motor

30% — crvUSD-WBTC (Curve, $89.4M TVL)
       APY: ~3.65%, full range, passzív
       → Stabil alap, BTC kitettség

20% — PAXG/USDC (Uniswap V3, $4M TVL)
       APY: ~17-23%, alacsony IL
       → Arany hedge, infláció-védelem

10% — Hedge pozíció: ETH perp short
       → Az ETH/USDC pool IL-jének kompenzálása

Súlyozott APY: ~22-26%
Kockázati profil: Kiegyensúlyozott
```

### E) "Csak lefelé védekezés" stratégia (ha bullish vagy)

```
Ha hiszel az emelkedésben, de védeni akarod a tőkéd:

1. 70% ETH/USDC pool (magas APY)
2. 30% PAXG/USDC pool (arany = safe haven, ha crypto esik)
3. Nincs short → teljes felfelé potenciál megtartva
4. Ha crash jön: arany tipikusan emelkedik amikor crypto esik
   → természetes hedge

Ez a legegyszerűbb és legolcsóbb hedge.
```

---

## 5. Kockázati mátrix — Volatile + Stablecoin poolok

| Kockázat | ETH/USDC | WBTC/USDT | PAXG/USDC | LINK/USDC |
|----------|----------|-----------|-----------|-----------|
| Impermanent Loss | 🔴 Magas | 🟡 Közepes | 🟢 Alacsony | 🔴 Magas |
| Smart contract | 🟢 (Uni V3 battle-tested) | 🟢 | 🟢 | 🟢 |
| Likviditás (ki-belépés) | 🟢 Kiváló ($97M) | 🟢 Jó ($27M+) | 🟡 Közepes ($4M) | 🔴 Alacsony ($1.4M) |
| Hosszú távú felértékelődés | 🟢 Magas | 🟢 Magas | 🟡 Mérsékelt | 🟡 Közepes |
| APY konzisztencia | 🟢 (30d avg: 43%) | 🟢 (30d avg: 17-27%) | 🟡 (30d: 20-32%) | 🔴 (volatilis) |

---

## 6. Végső ajánlás

### Nagy tőkével ($50k+), jelenlegi piaci helyzetben:

**1. Elsődleges pozíció: USDC-WETH (Uniswap V3) — $97.8M TVL**
- 40% APY, nagyon konzisztens (30d avg: 43.91%)
- Hatalmas likviditás, nagy tőkét is elbír
- SZÜKSÉGES: Concentrated liquidity range aktív kezelése
- SZÜKSÉGES: 50% perp short hedge az IL ellen (lásd 4/A stratégia)

**2. Kiegészítő pozíció: WBTC-USDC (Uniswap V3) — $27.3M TVL**
- 18.46% APY (30d: 17.90% — stabil!)
- BTC alacsonyabb volatilitás mint ETH → kevesebb IL
- Diverzifikáció az ETH pool mellé

**3. Safe haven: PAXG-USDC (Uniswap V3) — $4M TVL**
- 17-23% APY, legalacsonyabb IL a volatile tokenek közül
- Arany = természetes hedge crypto esés ellen
- Korlát: Max $500k-$1M tőke (TVL miatt)

### Javasolt allokáció:

| Allokáció | Pool | Várható APY | Hedge |
|-----------|------|-------------|-------|
| 50% | ETH/USDC (Uni V3) | ~40% | Perp short 50% |
| 30% | WBTC/USDC (Uni V3) | ~18% | Nincs (alacsonyabb vol) |
| 20% | PAXG/USDC (Uni V3) | ~20% | Nincs (természetes hedge) |

**Súlyozott átlagos APY: ~28-30% (hedge költségek előtt)**
**Hedge után net APY: ~22-26%**

---

## Fontos figyelmeztetés

> Ez a dokumentum kutatási célokat szolgál és **NEM minősül pénzügyi tanácsadásnak**.
> A DeFi protokollok smart contract kockázatot hordoznak. Az impermanent loss jelentős
> veszteséget okozhat volatile token + stablecoin poolokban. Mindig végezz saját kutatást
> (DYOR) és csak annyit fektess be, amennyit hajlandó vagy elveszíteni. A múltbeli hozamok
> nem garantálják a jövőbeli teljesítményt.

---

*Adatforrás: DefiLlama Yields API (2026.03.30)*
*Elemzés: AI-alapú DeFi kutatás*
