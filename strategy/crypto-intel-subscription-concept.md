# Crypto Intel Copilot — előfizetéses AI-elemző szolgáltatás kripto befektetőknek

Koncepció: MCP szerverek (Smithery) + agent skillek + a meglévő connector-stack
(Shopify, Klaviyo, Meta Ads, Trendtruck, Higgsfield, WoopSocial) kombinálásával
felépíthető egy ismétlődő bevételt termelő, AI-vezérelt kripto kutatási előfizetés.

## 1. A termék egy mondatban

Napi/heti, személyre szabott, AI által generált kripto piaci brief és on-demand
token-mélyelemzés, e-mailben és webes felületen, három előfizetési szinten —
a teljes pipeline-t (adat → elemzés → tartalom → kiküldés → marketing) agentek
és MCP szerverek hajtják, minimális emberi munkával.

## 2. Miért működhet

- A kripto befektetők bizonyítottan fizetnek kutatásért (Messari, Token Metrics,
  Delphi Digital: 25–250 USD/hó árszintek), de ezek statikus, mindenkinek
  ugyanazt küldő termékek.
- Az MCP réteg miatt a "kutatócsapat" határköltsége közel nulla: a CoinGecko,
  CCXT, Token Metrics stb. szerverek Smithery-n keresztül azonnal bekötve
  adnak élő piaci, tőzsdei és on-chain adatot.
- A differenciátor a **perszonalizáció**: a brief a feliratkozó saját
  watchlistjére/portfóliójára készül, nem általános hírlevél.

## 3. Építőelemek

### 3.1 Adat- és elemzőréteg — Smithery MCP szerverek

| MCP szerver | Mire jó |
|---|---|
| CoinGecko MCP | Árak, market cap, volumen 15k+ coinra; on-chain DEX ár- és likviditásadat 8M+ tokenre (GeckoTerminal) |
| CoinMarketCap MCP | Másodlagos árforrás, listázások, rangsorok |
| CCXT MCP | Tőzsdei adatok (order book, funding rate, OI) 100+ tőzsdéről |
| Token Metrics MCP | Kereskedési szignálok, grade-ek |
| Hír/feed MCP-k (RSS, web search) | Narratíva- és sentiment-figyelés |

### 3.2 Skillek (Smithery skills + saját)

- `daily-market-brief`: piaci összefoglaló generálása sablon szerint
- `token-deep-dive`: egy token teljes átvilágítása (tokenomics, likviditás,
  holder-koncentráció, hírek) fizetős igénylésre
- `portfolio-risk-report`: watchlist-alapú kitettség- és korrelációelemzés
- `whale-alert-digest`: nagy on-chain mozgások értelmezése
- A repo 144 agentje (engineering, marketing, product, sales) a cégépítési
  oldalt fedi: landing page, funnel copy, sprint-priorizálás stb.

### 3.3 Monetizáció és disztribúció — a meglévő connectorok

| Connector | Szerep |
|---|---|
| **Shopify** | Előfizetés értékesítése (digitális termék + subscription app), vásárlói adatbázis, tier-ek kezelése |
| **Klaviyo** | A termék kézbesítési csatornája: napi/heti brief e-mail sablonok, tier-szegmensek, welcome/churn flow-k |
| **Meta Ads** | Ügyfélszerzés: lead gen formok, lookalike audience-ek a fizetős előfizetőkből |
| **Trendtruck** | Versenytárs-hirdetések és nyertes kreatívok kutatása (mit hirdet a Messari, a kripto-hírlevelek) |
| **Higgsfield** | Hirdetési kreatívok, rövid videók generálása + viralitás-előrejelzés |
| **WoopSocial** | Ingyenes teaser-tartalom (napi 1 insight) automatikus posztolása — organikus funnel-top |

## 4. Előfizetési szintek

| Tier | Ár | Tartalom |
|---|---|---|
| Free | 0 | Heti piaci összefoglaló e-mail (lead magnet) |
| Pro | ~29 USD/hó | Napi AI-brief a saját watchlistre, ár- és whale-alertek |
| Whale | ~99 USD/hó | Minden Pro + havi N db on-demand token-mélyelemzés, portfólió-kockázati riport, Telegram/Discord bot hozzáférés |

## 5. Architektúra (MVP)

```
[Smithery MCP-k: CoinGecko, CCXT, TokenMetrics, news]
        │
        ▼
[Orchestrator agent — Claude Agent SDK, ütemezve (cron / GitHub Actions)]
        │  skillek: daily-market-brief, token-deep-dive, ...
        ▼
[Tartalom: markdown → Klaviyo e-mail sablon (klaviyo_create_email_template)]
        │
        ▼
[Klaviyo kampány tier-szegmensenként]          [Shopify: előfizetés + customer tag]
        ▲                                                   │
        └──────────── tag → szegmens szinkron ◄─────────────┘

Marketing hurok: Trendtruck (kutatás) → Higgsfield (kreatív)
→ Meta Ads (fizetett) + WoopSocial (organikus) → Shopify checkout
```

## 6. MVP terv (4 hét)

1. **1. hét — adatpipeline**: CoinGecko + CCXT MCP bekötése Smithery-ről,
   `daily-market-brief` skill megírása, kézi futtatással napi brief generálás.
2. **2. hét — kézbesítés**: Klaviyo sablon + lista/szegmens setup, ütemezett
   futtatás GitHub Actions-ból, free tier hírlevél élesítése.
3. **3. hét — fizetés**: Shopify előfizetési termék (Pro tier), vevő-tag →
   Klaviyo szegmens szinkron, watchlist-űrlap (Klaviyo custom property).
4. **4. hét — growth**: Trendtruck versenytárs-audit, Higgsfield kreatívok,
   első Meta Ads lead gen kampány, WoopSocial napi teaser automatizálás.

## 7. Kockázatok és megfelelés

- **Nem befektetési tanácsadás**: minden kimenetben kötelező disclaimer;
  EU-ban a MiCA marketingszabályaira figyelni kell (kiegyensúlyozott
  kommunikáció, kockázati figyelmeztetés).
- **Adatforrás-függés**: ingyenes API-tierek rate limitje — fizetős
  CoinGecko/CMC kulcs kell skálázásnál.
- **Hirdetési platform szabályok**: a Meta korlátozza a kripto-hirdetéseket;
  a hirdetésnek a *kutatási/oktatási* termékre kell fókuszálnia, nem
  tradingre — egyes régiókban engedély szükséges.
- **Minőségkontroll**: az AI-brief hallucináció-kockázata miatt számadatokat
  csak MCP-forrásból, idézett formában szabad közölni.

## 8. Miért véd ez a stack

Az érték nem egyetlen adatforrás, hanem az **orkesztráció**: adat → elemzés →
perszonalizált kézbesítés → automata growth-hurok egyetlen agent-rendszerben.
Ezt a Smithery-ről bárki által bekapcsolható MCP-k önmagukban nem adják, a
hagyományos hírlevél-kiadók pedig nem tudják perszonalizálni.
