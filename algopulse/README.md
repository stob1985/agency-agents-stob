# AlgoPulse — AI-vezérelt kripto intelligencia platform

Működő, futtatható Next.js alkalmazás: élő piaci adat, valós indikátor-alapú
szignálmotor, AI napi brief, előfizetési tier-ek. Ez az MVP magja annak az
előfizetéses rendszernek, amit a `strategy/crypto-intel-subscription-concept.md`
ír le üzleti oldalról.

## Mit tud most (külső kulcs nélkül is)

- **Landing page** — hero, élő árticker, feature-grid, 3 szintű pricing
  (Scout 0$ / Pro 29$ / Whale 99$)
- **Dashboard** (`/dashboard`)
  - Top-20 piac élő adatokkal (CoinGecko), 7 napos sparkline-okkal
  - Piaci statisztikák: össz-kapitalizáció, volumen, BTC-dominancia
  - **Szignálmotor**: óránkénti idősoron számolt RSI(14), SMA20/50 kereszt,
    MACD → BUY / SELL / NEUTRAL hívás konfidenciával és indoklással
    (minden szignál megmutatja, miből jött — nincs black box)
  - **Napi AI brief**: ha van `ANTHROPIC_API_KEY`, Claude írja a piaci
    snapshotból; kulcs nélkül determinisztikus, adatvezérelt brief készül
  - Fear & Greed index (alternative.me)
  - Watchlist (csillagozás, localStorage)
  - **Tier-gating demó**: free nézetben csak 3 szignál látszik, a többi
    blurölve, upsell CTA-val — `/dashboard?plan=pro` mutatja a Pro nézetet
- **API**: `GET /api/brief` — a napi brief JSON-ban (e-mail pipeline-nak)

## Futtatás

```bash
cd algopulse
npm install
npm run dev        # http://localhost:3000
```

Opcionális `.env` (lásd `.env.example`):

| Változó | Hatás |
|---|---|
| `ANTHROPIC_API_KEY` | a napi briefet Claude írja a rules-engine helyett |
| `COINGECKO_API_KEY` | magasabb rate limit (demo kulcs elég) |
| `STRIPE_*` | előfizetés-checkout bekötési pont |

## Architektúra

```
app/
  page.tsx              landing (SSR, 120s revalidate)
  dashboard/page.tsx    dashboard (SSR, tier-gating searchParam alapján)
  api/brief/route.ts    brief JSON endpoint (Klaviyo/e-mail pipeline-hoz)
lib/
  coingecko.ts          adatkliens (markets + Fear&Greed)
  indicators.ts         RSI, SMA, EMA, MACD, SMA-kereszt detektor
  signals.ts            szabály-alapú szignálmotor + pontozás
  brief.ts              Claude-os és determinisztikus brief generátor
  tiers.ts              tier-definíciók (Stripe price env bekötési ponttal)
.mcp.json               Smithery MCP szerverek a kutató-agent réteghez
```

## Következő kiépítési lépések (production)

1. **Auth + fizetés**: Clerk/NextAuth + Stripe subscription — a
   `lib/tiers.ts` `stripePriceEnv` mezői a bekötési pontok; a
   `?plan=` demó-paramétert session-beli plan váltja ki.
2. **E-mail kézbesítés**: cron (Vercel Cron / GitHub Actions) →
   `GET /api/brief` → Klaviyo template + kampány tier-szegmensenként.
3. **Watchlist-perszonalizált brief**: a watchlist felküldése profilra,
   a brief promptja a user saját coinjaira szűkítve.
4. **Mélyelemzés (Whale tier)**: a `.mcp.json`-ben definiált
   CoinGecko/CCXT/CMC MCP szerverekre kötött agent generál on-demand
   token-riportot.
5. **Szignál-történet + találati statisztika**: szignálok perzisztálása
   (Postgres) és visszamérése — ez adja a bizalmat az előfizetéshez.

## Disclaimer

A platform elemzési célú; nem minősül befektetési tanácsadásnak. Minden
kimenetben kötelező a kockázati figyelmeztetés (a footer és a brief
Risk Note szekciója ezt tartalmazza).
