# ContractMD – Validációs Teszt Setup

## Mit fogunk csinálni?

Ez egy **30 perces validációs teszt** a ContractMD ötlet előtt. A célunk **NEM az**, hogy SaaS-t építsünk. A célunk:

1. Telepíteni az `ai-legal-claude` skill-szettet helyileg Claude Code-ba
2. Lefuttatni **3 különböző valós szerződésen**
3. Eldönteni: a kimenete **jó-e ahhoz, hogy ÉRTÉKES legyen** egy ügyfélnek?

Ha igen → megyünk a következő lépéshez (SaaS frontend építés).
Ha nem → más alapot keresünk vagy módosítunk.

**Ez Pat Walls vendégeinek a "validate before you build" filozófiája.**

---

## ELŐKÉSZÜLETEK (egyszeri)

### 1. Claude Code CLI telepítése

Ha még nincs:

**Mac/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (WSL ajánlott):**
- Telepíts WSL2-t ha még nincs
- Majd futtasd a Mac/Linux parancsot WSL Ubuntu-ban

### 2. Anthropic API key beállítása

1. Menj ide: https://console.anthropic.com/
2. Sign up / log in
3. Settings → API Keys → Create Key
4. **Tegyél fel $5-10 USD credit-et** (a teszthez bőven elég lesz)
5. Másold ki a key-t

### 3. Claude Code authentikáció

```bash
claude auth
```
Beilleszted az API key-t, kész.

### 4. Python deps

```bash
pip3 install reportlab
```

---

## A FŐ TELEPÍTÉS (egy parancs!)

Most jön a varázslat. Ez a parancs **letölti, telepíti és beállítja** az összes szükséges skill-t és agentet a Claude Code-ba:

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash
```

### Mit telepít pontosan?

A `~/.claude/` mappádba (a Claude Code-od saját mappája) telepít:

**14 SKILL** (`~/.claude/skills/`):
- `legal` — orchestrator (a fő parancs router)
- `legal-review` — **TELJES contract review (a flagship!)**
- `legal-risks` — mély risk analízis
- `legal-compare` — két contract összehasonlítása
- `legal-plain` — "fordítás" hétköznapi nyelvre
- `legal-negotiate` — counter-proposal generátor
- `legal-missing` — hiányzó protections keresése
- `legal-nda` — NDA generálás
- `legal-terms` — Terms of Service generálás
- `legal-privacy` — Privacy Policy generálás
- `legal-agreement` — business agreement-ek
- `legal-freelancer` — freelancer szerződés review
- `legal-compliance` — compliance gap analysis
- `legal-report-pdf` — professzionális PDF report

**5 PARALLEL AGENT** (`~/.claude/agents/`):
- `legal-clauses` — minden klauzulát azonosít és kategorizál
- `legal-risks` — minden klauzulát beponthoz risk-skálán (1-10)
- `legal-compliance` — szabályozói problémákat jelez
- `legal-terms` — kötelezettségeket, határidőket térképez
- `legal-recommendations` — konkrét fix-eket generál

**3 PYTHON SCRIPT** (PDF generáláshoz)

---

## ELLENŐRZÉS – Sikerült?

Futtasd:

```bash
ls ~/.claude/skills/ | grep legal
```

Ha látsz ~14 sort, kész vagy.

Vagy nyiss Claude Code-ot:
```bash
claude
```

Majd írd be:
```
/legal
```

Ha listázza a parancsokat → minden OK ✅

---

## KÖVETKEZŐ LÉPÉS

Nyisd meg a `02_TEST_PROTOCOL_HU.md` fájlt a teszt-protokollért.
