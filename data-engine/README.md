# Narrative Data Engine

**Nem dashboardot adunk el felhasználóknak — derivált adatot adunk el rendszereknek.**

Egy ingestion-pipeline, **két eladható adattermék**, API-kulcsos hozzáféréssel és
plan-gateléssel. Az agent-flotta a gyár, a felhalmozott idősor a védőárok.

Futtatható, élő RSS-ből tesztelt rendszer (211 valós cikk beolvasva és
strukturált adattá alakítva az első futásnál).

## A tézis

Nyers árfolyamadat commodity, és a CoinGecko/CMC licence tiltja a
továbbértékesítését. Amit el lehet adni, az **általunk gyártott derivált adat**:
egy LLM-agent óránként végigolvassa a hírfolyamot, és minden cikkből strukturált
rekordot készít (érintett tokenek, sentiment, narratíva, esemény). Ezt a munkát
2 éve csak elemző-hadsereggel lehetett elvégezni — most egy Haiku-agent végzi
napi pár dollárból. A felhalmozott, visszamenőleg címkézett idősort **senki nem
tudja utólag reprodukálni**, ezért az adatbázis minden nappal értékesebb.

## A két termék (egy pipeline-ból)

### A — Narrative Heat Index
Tokenenkénti és narratívánkénti óránkénti „hype" idősor sentimenttel.
Vevő: quant fundok, trading-bot fejlesztők, kutatók.
- `GET /v1/heat/top?window_hours=24` — mi forró most (rangsorolt tokenek + narratívák)
- `GET /v1/heat?token=BTC&narrative=ETF&from=&to=` — idősor

### B — Token Event Feed
Strukturált, forrásolt események: listing, unlock, mainnet, hack, ETF-filing…
- `GET /v1/events?type=unlock&token=ARB&limit=50`
- `POST /v1/webhooks` — push értesítés új eseményekre (Pro+)

## Architektúra

```
RSS-források (CoinDesk, Cointelegraph, Decrypt, …)   ← csak DERIVÁLUNK, nem osztunk újra
        │  src/sources.js  (fetch + dedup hash)
        ▼
  Extraction agent           src/extract.js
   ├─ Claude (Haiku)  ← ANTHROPIC_API_KEY esetén a produkciós címkéző
   └─ rules-v1        ← determinisztikus fallback, kulcs nélkül is fut
        │  kimenet a TAXONÓMIÁRA normalizálva (src/taxonomy.js)
        ▼
  SQLite (node:sqlite)        src/db.js
   ├─ articles  ├─ labels
   ├─ heat   → Termék A        ├─ events → Termék B
        │  src/ingest.js  (fan-out a két termékbe)
        ▼
  REST API + kulcs-auth + plan-gating   src/server.js
   ├─ /v1/heat*, /v1/events, /v1/webhooks, /v1/export.csv
   └─ free / pro / enterprise            src/plans.js
```

## Üzleti modell — a packaging maga a termék

Ugyanaz az adat, három szinten gatelve (`src/plans.js`):

| Plan | Ár/hó | History | Rate | Webhook | CSV |
|---|---|---|---|---|---|
| Free | $0 | 24h | 30/min | — | — |
| Pro | $199 | 90 nap | 300/min | ✓ | ✓ |
| Enterprise | $999 | teljes | 3000/min | ✓ | ✓ |

A history-gating **szerveroldalon** kényszerített: a free kulcs nem tud a 24
óránál régebbi adathoz férni, akárhogy is paraméterez — a moat (a felhalmozott
történet) így ténylegesen a fizetős szint mögött van.

## Futtatás

```bash
cd data-engine
npm install
npm run seed-keys     # demo kulcsok: pk_demo_free / pk_demo_pro / pk_demo_ent
npm run ingest        # élő RSS-ből beolvas + címkéz (rules, vagy Claude ha van kulcs)
npm run serve         # API a http://localhost:8787 címen (docs a gyökéren)
```

Próbahívás:
```bash
curl -H "X-API-Key: pk_demo_pro" "http://localhost:8787/v1/heat/top?window_hours=72"
curl -H "X-API-Key: pk_demo_pro" "http://localhost:8787/v1/events?type=unlock"
```

Opcionális env:
| Változó | Hatás |
|---|---|
| `ANTHROPIC_API_KEY` | a címkézést Claude végzi a rules-engine helyett |
| `EXTRACT_MODEL` | címkéző modell (alapért. `claude-haiku-4-5`) |
| `PORT` | API port (alapért. 8787) |

## Production felé hátralevő lépések

1. **Cron ingest** — `npm run ingest` óránként (GitHub Actions / Vercel Cron).
   Re-runokra idempotens (cikkek hash-elve, címke egyszer készül).
2. **Webhook-kézbesítő worker** — az `events` táblát figyeli, és a `webhooks`
   regisztrációkra POST-ol (retry + aláírás). A regisztrációs végpont kész.
3. **Kulcs-mintázás fizetésnél** — Stripe checkout → `api_keys` insert a vett
   plannel (most a `seed.js` csinálja kézzel).
4. **Több forrás + Smithery MCP** — a `.mcp.json`-stílusú CoinGecko/CCXT MCP
   szerverekkel on-chain és tőzsdei jeleket is a heat-be fűzni.
5. **Minőség-visszamérés** — a címkék mintavételes humán-ellenőrzése, a
   sentiment kalibrálása az árelmozdulásokhoz (ez adja el az Enterprise szintet).

## Megfelelés

Csak derivált adatot (saját címkék, aggregátumok) szolgáltatunk, forrás-cikkeket
nem osztunk újra. Az adat elemzési célú, nem befektetési tanácsadás.
