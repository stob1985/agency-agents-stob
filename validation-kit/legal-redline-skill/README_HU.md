# Legal Redline Skill — Magyar útmutató

A `legal-redline` egy új skill az `ai-legal-claude` framework-höz: olyan Word `.docx` riportot generál, amit **az ügyfél közvetlenül elküldhet a másik félnek tárgyalási alapként**. Igazi Word tracked changes + igazi margin comment + vizuális redline egyben.

---

## Mit ad ki?

`REDLINED-<szerződés-neve>.docx` — egy szakszerű "redline" doksi, mintha egy ügyvéd készítette volna:

- **Borító:** pontszám most / pontszám módosítás után / osztályzat (A-F) / verdikt
- **Klauzulánként:**
  - 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW jelzés
  - Eredeti szöveg **valódi Word tracked deletion**-ként (piros, áthúzva)
  - Javasolt szöveg **valódi Word tracked insertion**-ként (zöld, aláhúzva)
  - Margin comment minden módosításhoz: *Miért problémás · Jogi alap · ⚠️ Mit kockáztat · ✓ Mit véd · 💡 Tárgyalási tipp*
  - Sárga inline-kártya ugyanezzel a tartalommal (akkor is olvasható, ha valaki kikapcsolja a változáskövetést)
- **Összegző táblázat** minden módosításról

→ A Word "Véleményezés" menüjében az ügyfél (vagy a másik fél) **el tudja fogadni / elutasítani** minden egyes módosítást egyenként.

---

## Telepítés

### 1. Előkészület — az alap `ai-legal-claude` legyen telepítve

```bash
curl -fsSL https://raw.githubusercontent.com/zubair-trabzada/ai-legal-claude/main/install.sh | bash
```

### 2. Klónozd a validation-kit-et

```bash
git clone -b claude/validate-core-engine-5AyzT https://github.com/stob1985/agency-agents-stob.git
cd agency-agents-stob/validation-kit/legal-redline-skill
```

### 3. Patch telepítés

```bash
bash install_patch.sh
```

Ez bemásolja:
- `~/.claude/skills/legal-redline/SKILL.md`
- `~/.claude/scripts/generate_redline_docx.py`

És feltelepíti a `python-docx` Python lib-et, ha még nincs.

---

## Használat

Claude Code-ban:

```
/legal redline test-contracts/freelancer_contract.md
```

Vagy a saját szerződéseden:

```
/legal redline my-contract.pdf
```

Claude először elvégzi a teljes review-t (mint a `/legal review` parancsnál), aztán **mindenhez konkrét javasolt új szöveget ír**, és generálja a `.docx`-et.

A kimenet az adott mappában jelenik meg: `REDLINED-<contract-name>.docx`.

---

## Példa minta

A `examples/` mappában van egy működő minta:
- **Bemenet:** `vallalkozoi_hu_redline_input.json` — JSON struktúra, amit a Claude összerak
- **Kimenet:** `REDLINED-Vallalkozoi-HU.docx` — a kész Word doksi

**Nyisd meg a `.docx`-et Word-ben vagy Google Docs-ban,** és kapcsold be a változáskövetést (Word: Review → Track Changes → All Markup). A 10 javasolt módosítást fogod látni, mindegyiknél margin commenttel.

---

## A skill működése részletesen

1. **Review** — Claude végigmegy a szerződésen, azonosítja a piros zászlókat (`legal-review` / `legal-risks` skillek alapján).
2. **Negotiate** — Minden piros zászlóhoz **konkrét új szöveget** ír (nem "törölni kell", hanem ténylegesen használható helyettesítő klauzula).
3. **JSON összeállítás** — A változtatásokat egy JSON-ba rendezi a `SKILL.md`-ben definiált séma szerint.
4. **Script futtatás** — A `generate_redline_docx.py` előállítja a `.docx`-et a JSON-ból, igazi Word tracked changes + comments XML manipulációval.

---

## Mit tartalmaz minden margin comment?

Példa magyar szerződésből (3.1 pont — IP overreach):

```
Miért problémás: A 'függetlenül attól, hogy a Szolgáltatásokhoz kapcsolódik-e' 
megfogalmazás minden szellemi alkotást — még a hobbi-projekteket, más ügyfelek 
számára végzett munkát is — a Megrendelőre ruház át. Ez tisztességtelen.

Jogi alap: Ptk. 6:102. § (tisztességtelen feltétel), Szjt. 16. § (4)-(5)

⚠️ Mit kockáztat: Saját könyvtáraidat, korábban fejlesztett kódjaidat, 
hobbi-projekted is elveszítheted.

✓ Mit véd a módosítás: Csak a kifejezetten Megrendelő számára végzett munka 
kerül át, a Prior IP-d megmarad.

💡 Tárgyalási tipp: Mellékletként adj át egy 'Prior IP' listát a meglévő 
anyagaidról — ez bizonyíték a tulajdonjogra.
```

---

## Nyelvi támogatás

- **Magyar szerződés** → magyar magyarázatok, Ptk./Mt./Szjt./Lt./GDPR magyar nyelven, NAIH-hivatkozás
- **Angol szerződés** → angol magyarázatok, US/UK statútumok (UCC, FTC, NY GOL, CA Labor Code)
- **Bármely más nyelv** → adott nyelven a Claude-tól, megfelelő jogi hivatkozásokkal

A nyelvet a Claude auto-detect-eli a szerződés tartalmából.

---

## Caveat-ok

1. **Ez nem helyettesíti az ügyvédet.** Az AI által generált redline jó tárgyalási alap, de aláírás előtt magyar/EU jog esetén szakember review-zza.
2. **A "score" és "score after redline" becsült.** Az engine nem perfekt — egy nehéz szerződésen ±10 pontot tévedhet.
3. **A javasolt szövegek tárgyalási alapot adnak**, nem végleges szerződésszöveg. A pontos megfogalmazást a tényleges felek közötti tárgyalás csiszolja.

---

## Hibajelentés

Ha a `.docx` nem nyílik meg vagy hibás:
1. Ellenőrizd, hogy `python-docx >= 1.0` van telepítve: `pip3 show python-docx`
2. Próbáld meg LibreOffice-szal vagy Google Docs-szal
3. A `comments.xml` és tracked changes Word 2007+ kompatibilis
