---
name: DeFi Hedge Stratégia - $100,000 USD
description: Teljes lépésről-lépésre hedge stratégia volatile+stablecoin LP pozíciókhoz
date: 2026-03-30
capital: $100,000
chain: Ethereum + Hyperliquid
source: DefiLlama API + Hyperliquid API
prices: ETH $2,072 | BTC $67,877 | PAXG $4,571
---

# Teljes Hedge Stratégia — $100,000 USD

## Jelenlegi piaci adatok (2026.03.30)

| Adat | Érték |
|------|-------|
| ETH ár | $2,072 |
| BTC ár | $67,877 |
| PAXG (arany) ár | $4,571 |
| ETH funding rate (Hyperliquid) | +0.0008% / 8h (+0.83% éves) |
| BTC funding rate (Hyperliquid) | -0.0007% / 8h (-0.74% éves) |
| WETH borrow rate (Aave V3) | 2.23% éves |
| USDC borrow rate (Aave V3) | 3.33% éves |

---

## Tőke elosztás — Áttekintés

```
$100,000 USD teljes tőke

┌─────────────────────────────────────────────────┐
│  POOL POZÍCIÓK ($85,000)                        │
│                                                 │
│  1. ETH/USDC  Uniswap V3    $50,000  (50%)     │
│  2. WBTC/USDC Uniswap V3    $20,000  (20%)     │
│  3. PAXG/USDC Uniswap V3    $15,000  (15%)     │
│                                                 │
├─────────────────────────────────────────────────┤
│  HEDGE POZÍCIÓK ($10,000 margin)                │
│                                                 │
│  4. ETH short perp (Hyperliquid)  $25,000 méret │
│  5. BTC short perp (Hyperliquid)  $10,000 méret │
│                                                 │
├─────────────────────────────────────────────────┤
│  TARTALÉK ($5,000)                              │
│                                                 │
│  6. USDC készpénz (vészhelyzet / margin top-up) │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## LÉPÉS 1: Stablecoin beszerzés

### 1.1 — Fiat → USDC konverzió

```
Hol: Coinbase, Kraken, vagy Binance
Mit:  $100,000 USD → 100,000 USDC
Fee:  ~0% (Coinbase Pro) vagy max 0.1%
```

### 1.2 — USDC átutalás Ethereum mainnet wallet-be

```
Wallet: Saját non-custodial wallet (MetaMask, Rabby, Safe)
⚠️  FONTOS: Hardware wallet ajánlott (Ledger/Trezor) ekkora összegnél
Network: Ethereum mainnet
Gas:     ~$2-5 (transfer)
```

### 1.3 — Swap tokenekre

```
Hol: Uniswap / CowSwap (jobb árak nagy összegnél)

Swap #1: 25,000 USDC → ~12.07 ETH        (az ETH/USDC pool ETH oldalához)
Swap #2: 10,000 USDC → ~0.147 WBTC        (a WBTC/USDC pool BTC oldalához)
Swap #3:  7,500 USDC → ~1.64 PAXG         (a PAXG/USDC pool arany oldalához)

Maradék USDC: 57,500 USDC (pool stable oldalak + hedge + tartalék)
```

> **Tipp:** CowSwap-on add fel limit orderként, így nincs MEV (sandwich attack) kockázat.

---

## LÉPÉS 2: LP pozíciók nyitása

### 2.1 — ETH/USDC pool ($50,000) — Uniswap V3

```
Pool:     USDC/WETH 0.3% fee tier
TVL:      $97.8M
APY:      ~40% (30d átlag: 43.91%)
Platform: app.uniswap.org

Berakás:
  - ~12.07 ETH  ($25,000)
  - 25,000 USDC ($25,000)
  - Összesen:    $50,000

Concentrated Liquidity Range beállítás:
  ┌──────────────────────────────────────┐
  │  Alsó határ:  $1,650  (-20% jelenlegi ártól)
  │  Felső határ: $2,500  (+20% jelenlegi ártól)
  │                                      │
  │  Jelenlegi ár: $2,072                │
  │  Range szélesség: ±20%               │
  │                                      │
  │  Miért ±20%?                         │
  │  - Szűkebb = magasabb fee, de több   │
  │    range management                  │
  │  - Szélesebb = kevesebb fee, de      │
  │    ritkábban kell állítani           │
  │  - ±20% = heti 1x ellenőrzés elég   │
  └──────────────────────────────────────┘

Gas cost: ~$15-30 (pozíció nyitás)
```

### 2.2 — WBTC/USDC pool ($20,000) — Uniswap V3

```
Pool:     WBTC/USDC 0.3% fee tier
TVL:      $27.3M
APY:      ~18.46% (30d átlag: 17.90%)
Platform: app.uniswap.org

Berakás:
  - ~0.147 WBTC  ($10,000)
  - 10,000 USDC  ($10,000)
  - Összesen:     $20,000

Concentrated Liquidity Range:
  ┌──────────────────────────────────────┐
  │  Alsó határ:  $54,000  (-20%)        │
  │  Felső határ: $82,000  (+20%)        │
  │  Jelenlegi ár: $67,877               │
  │  Range: ±20%                         │
  └──────────────────────────────────────┘

Gas cost: ~$15-30
```

### 2.3 — PAXG/USDC pool ($15,000) — Uniswap V3

```
Pool:     PAXG/USDC 0.3% fee tier
TVL:      $4M
APY:      ~17-23% (30d átlag: 20.62%)
Platform: app.uniswap.org

Berakás:
  - ~1.64 PAXG   ($7,500)
  - 7,500 USDC   ($7,500)
  - Összesen:     $15,000

Concentrated Liquidity Range:
  ┌──────────────────────────────────────┐
  │  Alsó határ:  $4,100  (-10%)         │
  │  Felső határ: $5,050  (+10%)         │
  │  Jelenlegi ár: $4,571                │
  │  Range: ±10% (arany kevésbé volatil) │
  └──────────────────────────────────────┘

⚠️ FONTOS: Max $15k ide, mert a pool TVL csak $4M
   (a te $15k-d a pool 0.4%-a — még elfogadható)

Gas cost: ~$15-30
```

---

## LÉPÉS 3: Hedge pozíciók nyitása (Hyperliquid)

### 3.1 — USDC bridge Hyperliquid-re

```
Összeg: $10,000 USDC (hedge margin)
Hol:    app.hyperliquid.xyz → Deposit
Bridge: Arbitrum bridge (olcsóbb gas)

Útvonal: Ethereum USDC → Arbitrum bridge → Hyperliquid deposit
Gas:     ~$5-10 összesen
```

### 3.2 — ETH SHORT perp pozíció

```
┌─────────────────────────────────────────────────────┐
│  ETH SHORT PERP — HYPERLIQUID                       │
│                                                     │
│  Méret:      $25,000 (short)                        │
│  Ez fedezi:  az ETH/USDC pool ETH kitettségének     │
│              100%-át ($25k ETH van a poolban)        │
│                                                     │
│  Margin:     $6,250 (4x leverage)                   │
│  Leverage:   4x                                     │
│  Likvidációs ár: ~$2,590 (+25% ETH emelkedés)       │
│                                                     │
│  Funding cost: +0.83% éves (te FIZETED, mert short) │
│  Éves hedge költség: $25,000 × 0.83% = ~$208/év     │
│                                                     │
│  ⚠️ Ha funding negatívra fordul (medvepiac):        │
│     TE KAPOD a funding-ot = extra hozam!            │
└─────────────────────────────────────────────────────┘

Belépés:
  1. app.hyperliquid.xyz → Trade → ETH-PERP
  2. SELL/SHORT → Market order
  3. Méret: 12.07 ETH (~$25,000)
  4. Leverage: 4x
  5. Confirm
```

### 3.3 — BTC SHORT perp pozíció

```
┌─────────────────────────────────────────────────────┐
│  BTC SHORT PERP — HYPERLIQUID                       │
│                                                     │
│  Méret:      $10,000 (short)                        │
│  Ez fedezi:  a WBTC/USDC pool BTC kitettségének     │
│              100%-át ($10k BTC van a poolban)        │
│                                                     │
│  Margin:     $2,500 (4x leverage)                   │
│  Leverage:   4x                                     │
│  Likvidációs ár: ~$84,846 (+25% BTC emelkedés)      │
│                                                     │
│  Funding cost: -0.74% éves (TE KAPOD, mert negatív!)│
│  Éves hedge bevétel: $10,000 × 0.74% = ~$74/év     │
└─────────────────────────────────────────────────────┘

Belépés:
  1. ETH-PERP → BTC-PERP váltás
  2. SELL/SHORT → Market order
  3. Méret: 0.147 BTC (~$10,000)
  4. Leverage: 4x
  5. Confirm
```

### 3.4 — PAXG: NINCS SHORT HEDGE

```
Miért nem?
  - Az arany természetes hedge a crypto ellen
  - Ha crypto esik → arany tipikusan emelkedik
  - A PAXG/USDC pool pont ellentétes irányba mozog
    mint az ETH/USDC és WBTC/USDC poolok
  - Shortolni az aranyat kontraproduktív lenne
```

---

## LÉPÉS 4: Stop-loss és alert beállítása

### 4.1 — Hyperliquid stop-loss orderek

```
ETH SHORT ($25k):
  - Stop-loss:   $2,485 (+20%) → $5,000 veszteség ha megüti
  - Take-profit: $1,660 (-20%) → $5,000 nyereség
  - ⚠️ Ha a Uni V3 range alsó határát ($1,650) megüti,
    vedd ki az LP-t is!

BTC SHORT ($10k):
  - Stop-loss:   $81,450 (+20%) → $2,000 veszteség
  - Take-profit: $54,300 (-20%) → $2,000 nyereség
```

### 4.2 — LP range monitoring

```
Beállítás: revert.finance vagy DeBank alert

ETH/USDC alert:
  - Ha ETH < $1,750 VAGY ETH > $2,400 → figyelmeztetés
  - Ez jelzi hogy közel vagy a range szélhez → újra kell pozícionálni

WBTC/USDC alert:
  - Ha BTC < $57,000 VAGY BTC > $78,000 → figyelmeztetés

PAXG/USDC alert:
  - Ha PAXG < $4,200 VAGY PAXG > $4,950 → figyelmeztetés
```

---

## LÉPÉS 5: Heti karbantartás rutin

### Hétfő reggel checklist (15 perc):

```
□ 1. Ellenőrizd az LP range-eket
     - Minden pool aktív range-ben van?
     - Ha nem → LÉPÉS 6 (újrapozícionálás)

□ 2. Ellenőrizd a Hyperliquid pozíciókat
     - Margin ratio OK? (>20%)
     - Ha margin ratio < 15% → tölts fel USDC-t a tartalékból

□ 3. Claim LP fee-ket
     - Uniswap → Pozíciók → Collect fees
     - A begyűjtött fee-t rakd USDC-be

□ 4. Ellenőrizd funding rate-eket
     - Ha ETH funding > +5% éves → fontold meg a hedge csökkentését
     - Ha ETH funding < -2% éves → növeld a short-ot (fizetnek érte)

□ 5. Nézd meg az arany/crypto korrelációt
     - Ha mindkettő esik → csökkentsd a PAXG pozíciót is
```

---

## LÉPÉS 6: Újrapozícionálás (ha kell)

### Ha ETH kimegy a range-ből:

```
Forgatókönyv A: ETH emelkedett $2,500 fölé (bullish breakout)
  1. Vedd ki az LP pozíciót (most főleg USDC van benne)
  2. Zárd a short-ot (veszteséges, de az LP USDC-je kompenzál)
  3. Swap 50/50 az új árhoz
  4. Nyiss új LP range-et: $2,200 - $3,000
  5. Nyiss új short-ot az új ETH kitettségre
  Gas: ~$50-80

Forgatókönyv B: ETH esett $1,650 alá (bearish breakdown)
  1. Vedd ki az LP-t (most főleg ETH van benne)
  2. Zárd a short-ot (NYERESÉGES → zsebeld be)
  3. Döntés:
     a) Újra belépés alacsonyabb range-ben ($1,300-$1,900)
     b) Vagy kivárás USDC-ben
  4. Ha újra belépsz → új short hedge is kell
```

---

## Teljes P&L számítás

### Optimista szcenárió (ETH ±15%, range-ben marad, 1 év):

```
BEVÉTEL:
  ETH/USDC LP fee:      $50,000 × 40% APY  = +$20,000
  WBTC/USDC LP fee:     $20,000 × 18% APY  = +$3,600
  PAXG/USDC LP fee:     $15,000 × 20% APY  = +$3,000
                                    ─────────────────
  Összes LP hozam:                           +$26,600

KÖLTSÉG:
  ETH short funding:    $25,000 × 0.83%    = -$208
  BTC short funding:    $10,000 × (-0.74%) = +$74 (BEVÉTEL!)
  Gas (52 hét × $5):                        = -$260
  Újrapozícionálás (4x):                    = -$200
                                    ─────────────────
  Összes költség:                            -$594

NETTÓ ÉVES HOZAM:  +$26,006
NETTÓ APY:         ~26% ($26,006 / $100,000)
```

### Reális szcenárió (ETH ±30%, 2x újrapozícionálás, 1 év):

```
BEVÉTEL:
  ETH/USDC LP fee (csökkentett, out-of-range idő):  +$14,000
  WBTC/USDC LP fee:                                  +$3,200
  PAXG/USDC LP fee:                                  +$2,500
  Short profit ETH esés fázisban:                    +$2,000
                                    ─────────────────
  Összes:                                            +$21,700

KÖLTSÉG:
  Impermanent Loss (nettó, hedge után):              -$1,500
  Short loss ETH emelkedés fázisban:                 -$2,000
  Funding + gas + újrapozícionálás:                  -$800
                                    ─────────────────
  Összes költség:                                    -$4,300

NETTÓ ÉVES HOZAM:  +$17,400
NETTÓ APY:         ~17.4%
```

### Pesszimista szcenárió (50%+ crypto crash):

```
BEVÉTEL:
  LP fee (csökkentett):                    +$5,000
  ETH short profit ($25k × 50%):          +$12,500
  BTC short profit ($10k × 50%):          +$5,000
  PAXG emelkedés (arany safe haven):      +$2,000
                                    ─────────────────
  Összes:                                  +$24,500

VESZTESÉG:
  Impermanent Loss (ETH/USDC pool):       -$7,000
  Impermanent Loss (WBTC/USDC pool):      -$2,500
  LP range-ből kikerülés → 0 fee idő:    -$3,000
                                    ─────────────────
  Összes veszteség:                        -$12,500

NETTÓ:  +$12,000 POZITÍV!
→ A hedge MEGVÉDTE a tőkéd, és még profitban is vagy!
```

---

## Összefoglaló: Minden pozíció egy helyen

```
┌────────────────────────────────────────────────────────────┐
│                    $100,000 TŐKE ELOSZTÁS                  │
├──────────┬──────────┬────────┬─────────┬──────────────────┤
│ Pozíció  │ Összeg   │ Hol    │ Típus   │ Hedge            │
├──────────┼──────────┼────────┼─────────┼──────────────────┤
│ ETH/USDC │ $50,000  │ Uni V3 │ LP      │ $25k ETH short   │
│ BTC/USDC │ $20,000  │ Uni V3 │ LP      │ $10k BTC short   │
│ PAXG/USDC│ $15,000  │ Uni V3 │ LP      │ nincs (term.hedge)│
│ ETH short│ $6,250*  │ HyperL │ Perp    │ -                │
│ BTC short│ $2,500*  │ HyperL │ Perp    │ -                │
│ Tartalék │ $5,000   │ Wallet │ USDC    │ -                │
│ Gas/fee  │ $1,250   │ -      │ -       │ -                │
├──────────┼──────────┼────────┼─────────┼──────────────────┤
│ ÖSSZESEN │$100,000  │        │         │                  │
└──────────┴──────────┴────────┴─────────┴──────────────────┘
  * margin összeg, a pozíció méret 4x leverage-dzsel nagyobb
```

---

## Vészhelyzet protokoll

### Ha ETH 30%-ot esik 1 nap alatt:

```
1. NE PÁNIKOLJ — a short hedge dolgozik érted
2. Ellenőrizd: LP range-ben van? Ha nem → vedd ki
3. Short nyereség → részben zárd (profit taking)
4. Várj 24h-t, majd értékeld újra
5. Új range beállítás az új ár körül
```

### Ha egy stablecoin de-peg történik (USDC < $0.95):

```
1. Azonnal vedd ki az USDC-t tartalmazó LP pozíciókat
2. Swap USDC → DAI vagy USDT (diverzifikáció)
3. A short pozíciók nem érintettek (Hyperliquid margin USDC-ben van!)
   → Ha USDC de-peg: tölts át USDT-re a margin-t is
4. Várj amíg stabilizálódik
```

### Ha Hyperliquid technikai probléma / exploit:

```
MAX veszteség: $10,000 (ami a Hyperliquid-on van)
A $85,000 LP pozíció + $5,000 tartalék NINCS érintve
→ Ezért tartjuk külön a hedge margin-t
```

---

## Fontos figyelmeztetés

> Ez a dokumentum kutatási és oktatási célokat szolgál, **NEM minősül pénzügyi
> tanácsadásnak**. A DeFi protokollok smart contract kockázatot hordoznak.
> A leverage-es short pozíciók likvidációs kockázattal járnak.
> Mindig végezz saját kutatást (DYOR) és csak annyit fektess be, amennyit
> hajlandó vagy elveszíteni.

---

*Adatforrás: DefiLlama Yields API + Hyperliquid API (2026.03.30)*
*Árak: ETH $2,072 | BTC $67,877 | PAXG $4,571*
