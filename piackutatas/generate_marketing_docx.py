"""
Marketing terv + Lovable prompt - .docx generálás
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def shade_cell(cell, color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def add_heading(doc, text, level=1, color=None):
    h = doc.add_heading(text, level=level)
    if color:
        for run in h.runs:
            run.font.color.rgb = RGBColor.from_string(color)
    return h


def add_para(doc, text, bold=False, italic=False, size=11, color=None, align=None):
    p = doc.add_paragraph()
    if align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    return p


def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r = p.add_run(bold_prefix)
        r.bold = True
        p.add_run(' ' + text)
    else:
        p.add_run(text)
    return p


def add_table(doc, headers, rows, header_color='6B8E7F'):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor.from_string('FFFFFF')
        r.font.size = Pt(10)
        shade_cell(hdr[i], header_color)
    for ri, row in enumerate(rows):
        cells = table.rows[ri + 1].cells
        for ci, val in enumerate(row):
            cells[ci].text = ''
            p = cells[ci].paragraphs[0]
            r = p.add_run(str(val))
            r.font.size = Pt(10)


def add_code_block(doc, text):
    """Add monospace 'code' block for the Lovable prompt"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    r = p.add_run(text)
    r.font.name = 'Consolas'
    r.font.size = Pt(9)
    return p


doc = Document()
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# === CÍMLAP ===
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('MARKETING TERV + LOVABLE WEBOLDAL-BRIEF')
r.bold = True; r.font.size = Pt(22); r.font.color.rgb = RGBColor.from_string('6B8E7F')

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = subtitle.add_run('Access Bars házhozmenős szolgáltatás gyerekeknek')
r.bold = True; r.font.size = Pt(15); r.font.color.rgb = RGBColor.from_string('C9805E')

sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Veszprém vármegye — Indító ár: 12.000 Ft / házhozmenős alkalom')
r.italic = True; r.font.size = Pt(13)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run('Készült: 2026. május 11.\nA 6 ügynökös piackutatás alapján')
r.font.size = Pt(10); r.font.color.rgb = RGBColor.from_string('595959')

doc.add_page_break()

# === A. MARKETING TERV ===
add_heading(doc, 'A. RÉSZ — Marketing terv', 1, '6B8E7F')

# 1. Pozicionálás
add_heading(doc, '1. Pozicionálás egy mondatban', 2)
p = doc.add_paragraph()
r = p.add_run('"Anya és bébiszitter vagyok. Házhoz megyek Veszprémben, és gyengéd, érintéses Access Bars relaxációval segítek a gyerekednek elcsendesedni."')
r.bold = True; r.italic = True; r.font.color.rgb = RGBColor.from_string('C9805E'); r.font.size = Pt(13)

add_para(doc, '')
add_para(doc, 'Három láb:', bold=True)
add_bullet(doc, 'Bizalom — anya + bébiszitter háttér (személyes, ismert vagyok a környékem szülői körében)')
add_bullet(doc, 'Kényelem — házhozmenős, a gyereked saját ágyán/szobájában nyugszik el')
add_bullet(doc, 'Specializáció — gyerekekre (4-14 év) szabott, a felnőtt protokolltól rövidebb és játékosabb')

add_heading(doc, '1.1. Mit NEM mondunk (jogi védelem!)', 3, 'C00000')
for t in ['"kezelés", "terápia", "gyógyítás"', 'ADHD, autizmus, szorongás, depresszió mint cél',
          '"javítja az iskolai teljesítményt"', '"Helyettesíti az orvost"']:
    add_bullet(doc, t)

add_heading(doc, '1.2. Mit MONDUNK helyette', 3, '00B050')
for t in ['"relaxációs élmény", "ellazító érintéses módszer"', '"kifejezetten gyerekeknek szabott 30 perc"',
          '"csendben pihen a saját ágyán"', '"Sok szülő jelzi, hogy a gyerek nyugodtabban alszik utána"']:
    add_bullet(doc, t)

# 2. Árstruktúra
add_heading(doc, '2. Árstruktúra (12.000 Ft alapra építve)', 2)
add_table(doc, ['Csomag', 'Ár', 'Egy alkalomra', 'Megjegyzés'], [
    ['1 alkalom házhoz (Veszprém + 30 km)', '12.000 Ft', '12.000 Ft', 'Alapcsomag'],
    ['3 alkalmas bérlet', '32.000 Ft', '10.667 Ft', '-11% kedvezmény'],
    ['5 alkalmas bérlet', '52.000 Ft', '10.400 Ft', '-13% kedvezmény'],
    ['Bemutató akció (új ügyfél, egyszer)', '8.900 Ft', '–', '"Ismerd meg" ár'],
    ['Bébiszitter + Bars kombi (3 ó + 1 Bars)', '17.000 Ft', '–', 'Egyedi USP'],
    ['30 km feletti távolság', '+200 Ft / km', '–', 'Tapolca, Pápa irány'],
    ['Ajándékutalvány', '12.000 Ft + igény', '–', 'Karácsonyra szezonális'],
])

add_para(doc, '')
add_para(doc, 'Üzenet az árhoz:', bold=True)
add_para(doc, '"Egy gyermekpszichológus magán: 15-21.000 Ft / alkalom. Egy Access Bars relaxáció a TE otthonodban: 12.000 Ft. A gyereked nem ül buszra, nem várakozik, nem fél új helytől — a saját ágyán pihen el."', italic=True)

# 3. USP
add_heading(doc, '3. Egyedi értékajánlat (USP) — 5 pont', 2)
usps = [
    'Házhoz megyek — egyetlen versenytárs sem Veszprém vármegyében',
    'Anya + bébiszitter háttér — referenciáid vannak meglévő szülőktől',
    'Csak gyerekekre szakosodva — 4-14 év, fókuszált tudás',
    'Bébiszitter+Bars kombi csomag — egyetlen versenytárs sem kínálja',
    'Ingyenes 15 perces telefonos ismerkedés indulás előtt (Tooley-modell)',
]
for i, u in enumerate(usps, 1):
    p = doc.add_paragraph(style='List Number')
    p.add_run(u)

# 4. Tartalompillérek
add_heading(doc, '4. Tartalompillérek — heti 3-5 poszt', 2)
add_table(doc, ['Pillér', 'Arány', 'Példák'], [
    ['"Anya vagyok" — személyes', '40%', 'Bébiszitter sztorik (anonim), kulisszák, Reels day-in-life'],
    ['Szülői tippek', '30%', 'Esti rituálé, iskolakezdés, hisztikezelés (NEM diagnózis!)'],
    ['Edukáció Access Bars-ról', '20%', 'Mi ez, hogy zajlik, mit érez a gyerek (disclaimerrel!)'],
    ['Vélemények, bizonyíték', '10%', 'Szülői testimonialok (engedéllyel), Google review'],
])

doc.add_page_break()

# 5. 90 napos akcióterv
add_heading(doc, '5. 90 napos cselekvési terv', 2)

add_heading(doc, '1-2. hét — Jogi és márka-alap', 3)
for t in ['EV bejelentkezés (NAV ÜPO online), TEÁOR 9604',
          '333-as gyermekvédelmi erkölcsi bizonyítvány igénylés (3.100 Ft)',
          'Szakmai felelősségbiztosítás kötése (~50.000 Ft/év)',
          'Ügyvéddel: szülői beleegyező + GDPR-tájékoztató + szolgáltatási szerződés sablon',
          'Bébiszitter ügyfeleknek email/üzenet a 8.900 Ft-os bemutató alkalomról',
          'Márkanév és logó (Canva, ingyen) — anyás, csendes hangulat',
          'Weboldal Lovable-ben (lásd B. rész)']:
    add_bullet(doc, t)

add_heading(doc, '3-4. hét — Online jelenlét', 3)
for t in ['Google Cégprofil: szolgáltatási terület Veszprém + 30 km',
          'Facebook üzleti oldal és Instagram profil',
          'Belépés helyi FB csoportokba: Gyerekprogramok Veszprém és környékén, Veszprémi Mami klub, Veszprém és környéke Baba-Mama Adok-Veszek, Veszprém Fórum',
          'Veszprémimami portál (imami.hu) — bemutatkozó hirdetés árajánlat kérése',
          'Első 3 blogposzt megírása',
          'CÉL: első 3 ügyfél a bébiszitter klienseidből, kedvezménnyel']:
    add_bullet(doc, t)

add_heading(doc, '2. hónap — Tartalom és első fizetett hirdetés', 3)
for t in ['Heti 3 organikus poszt (1 történet + 1 tipp + 1 edukáció)',
          'Heti 1 Reels (15-30 mp, telefon, természetes fény)',
          'Facebook Ads start: napi 800-1.000 Ft (havi ~25.000 Ft)',
          'Célzás: nők 28-45 év, Veszprém + 30 km, érdeklődés: parenting, alternatív gyógyászat, jóga, Waldorf',
          'Google Cégprofil: kérj 5 review-t az első ügyfeleidtől',
          'CÉL: 5-8 új ügyfél, 1 visszatérő']:
    add_bullet(doc, t)

add_heading(doc, '3. hónap — Skálázás', 3)
for t in ['Veszprémimami partneri PR-cikk (15-25.000 Ft)',
          'Email Csillagvár Waldorf Óvoda + Fehérlófia Waldorf vezetőjének — INGYENES bemutató workshop szülői körnek (NEM intézményen belül!)',
          'Első mikroinfluencer (helyi anyukás Instagram, 5-15 ezer követő) — 1 ingyenes alkalom cserébe poszt',
          'Ajánlási rendszer: -20% kedvezmény, ha új ügyfelet hozol',
          'CÉL: havi 8-12 alkalom, 30% visszatérő']:
    add_bullet(doc, t)

add_heading(doc, '4-6. hónap — Szezonális akciók', 3)
for t in ['Augusztus → "Iskolakezdés stresszmentesen" csomag (3 alkalom -15%)',
          'November-december → Karácsonyi ajándékutalvány kampány',
          'Január → "Vizsgaidőszak támogató" csomag']:
    add_bullet(doc, t)

# 6. Hirdetési kreatívok
doc.add_page_break()
add_heading(doc, '6. Hirdetési kreatívok (3 sablon)', 2)

add_heading(doc, 'Kreatív #1 — Szorongó gyerek szülőjének', 3)
p = doc.add_paragraph()
r = p.add_run('🌙 "Nem akarok iskolába menni." Ezt hallottad ma reggel?\n\n'
              'Nem vagy egyedül. 12 évig bébiszitterkedtem Veszprémben, és száz családnál láttam, mikor a gyerek hisztivel, hasfájással, alvászavarral fejezi ki azt, amit szóban nem tud.\n\n'
              'Az Access Bars egy 30 perces gyengéd, érintéses relaxáció a fej 32 pontján. Nem orvosi kezelés — egyszerűen csendes, biztonságos pihenés. A gyereked saját ágyában, otthon.\n\n'
              'Veszprém + 30 km házhoz: 12.000 Ft\n'
              'Bemutató ár új ügyfeleknek: 8.900 Ft\n'
              'Ingyenes 15 perces telefon: foglalj időpontot →')
r.italic = True
add_para(doc, 'Vizuál: Saját, NEM stockfotó. Anya + gyerek lazán a kanapén, természetes fény.', italic=True, size=10, color='595959')

add_heading(doc, 'Kreatív #2 — A bébiszitter narratíva', 3)
p = doc.add_paragraph()
r = p.add_run('Anya vagyok. 12 évig bébiszitterkedtem.\n\n'
              'Aztán egy nap rátaláltam az Access Bars-ra, és láttam, hogy a gyerekek 30 perc alatt elcsendesednek. Nem mágia. Csak gyengéd érintés a fejen.\n\n'
              'Most ezt csinálom. Házhoz megyek Veszprém környékén, mert tudom, milyen nehéz egy meghisztizett gyereket beültetni az autóba.\n\n'
              'Ismerd meg a történetem →')
r.italic = True
add_para(doc, 'Vizuál: Saját fotó (arc + meleg mosoly). Vagy "rólam" idézet vizuál.', italic=True, size=10, color='595959')

add_heading(doc, 'Kreatív #3 — Karusszel (lead magnet)', 3)
add_para(doc, '5 slide-os karusszel a "5 jel, hogy a gyermeked stresszes" témáról:')
for s in ['Slide 1: Cím + figyelemfelkeltés',
          'Slide 2: Hasfájás iskola előtt',
          'Slide 3: Nehéz elalvás, éjszakai felébredés',
          'Slide 4: Dühroham apróságokon',
          'Slide 5: "Ha 2+ jelet látsz — INGYENES PDF-em segít. Töltsd le →"']:
    add_bullet(doc, s)
add_para(doc, 'CTA: PDF lead magnet — "7 esti rituálé szorongó gyermekekre"', bold=True)

# 7. Lead magnet
add_heading(doc, '7. Lead magnet ötletek (email lista)', 2)
add_table(doc, ['#', 'Cím', 'Forma'], [
    ['A1', '7 esti rituálé, ami nyugodt gyermeket eredményez', 'PDF (5-8 oldal, Canva)'],
    ['A2', 'Iskolakezdés stresszmentesen — anyák túlélőkészlete', 'PDF (3 oldal + checklist)'],
    ['A3', 'Mi az Access Bars? — őszinte útmutató szülőknek', 'PDF (saját módszer)'],
])
add_para(doc, '')
add_para(doc, 'Eszköz: MailerLite (ingyenes 1000 feliratkozóig).', bold=True)

# 8. KPI
add_heading(doc, '8. Kulcs KPI-ok — mit mérj havonta?', 2)
add_table(doc, ['Mutató', '3. hó', '6. hó', '12. hó'], [
    ['Új ügyfél / hó', '3-5', '5-8', '8-12'],
    ['Visszatérő %', '20%', '35%', '50%'],
    ['Havi bevétel', '50-80 ezer Ft', '100-150 ezer Ft', '180-250 ezer Ft'],
    ['Google review', '5 db', '12 db', '25 db'],
    ['Email feliratkozó', '30', '100', '250'],
    ['Facebook követő', '100', '400', '1.000'],
    ['Weblap látogató/hó', '200', '800', '2.500'],
])

doc.add_page_break()

# === B. LOVABLE PROMPT ===
add_heading(doc, 'B. RÉSZ — Lovable weboldal-prompt', 1, '6B8E7F')

add_para(doc, 'Másold be a következő szöveget EGYBEN a Lovable felületére (lovable.dev). '
              'A [ZÁRÓJELES] részeket cseréld le a saját adataidra MIELŐTT elküldöd.', bold=True)

doc.add_paragraph()

# A teljes prompt egy code blockban
prompt_text = """Készíts egy professzionális, megbízhatóságot sugárzó, mobil-első weboldalt
egy magyar nyelvű gyermek wellness szolgáltatáshoz Veszprém vármegyében.
A szolgáltatás: Access Bars relaxációs érintéses módszer gyerekeknek
(4-14 év), HÁZHOZMENŐS szolgáltatás Veszprém + 30 km körzetében.

A vállalkozó: [A TE NEVED], anya és X évig bébiszitter, akkreditált
Access Bars Practitioner. Egyedi értékajánlat: házhozmenős + gyerek-
specializáció + bébiszitter háttér.

=== TECHNOLÓGIAI KÖVETELMÉNYEK ===
- React + TypeScript + Tailwind CSS + shadcn/ui
- Magyar nyelvű (HTML lang="hu")
- Mobil-első, reszponzív
- Single-page application 6 szekcióval (Home),
  külön oldalak az alább megjelölteknek
- Modern, lágy, anyás hangulatú design
- Lighthouse-optimalizált (gyors betöltés)
- Magyar nyelvű meta tagek (SEO)

=== DESIGN RENDSZER ===
SZÍNPALETTA (lágy, természetes, nem rikító):
- Primary:   #6B8E7F (mohazöld) - CTA gombok
- Secondary: #E8DCC4 (homokszín) - hátterek
- Accent:    #C9805E (terrakotta) - kiemelések
- Text:      #2D3436 (szénszürke)
- Background:#FAF7F2 (krém)
- Muted:     #B8AFA1 (taupe)

TIPOGRÁFIA:
- Címek: "DM Serif Display" (Google Fonts) - meleg, szérifes
- Szöveg: "Inter" (Google Fonts) - modern, jól olvasható

HANGULAT:
- Lágy árnyékok (nem éles)
- Lekerekített sarkok (rounded-2xl, rounded-3xl)
- Sok fehér tér / paddings
- NE legyen csilingelős, gyermekded, csillámos
- Inkább "wellness studio meets anyás otthon"

=== FŐOLDAL SZEKCIÓI ===

1. HERO szekció (fullscreen)
   - H1: "Csendes pillanat a gyermekednek — házhoz megyek."
   - Alcím: "Access Bars relaxációs érintéses módszer 4-14 éveseknek.
     Otthon. Saját ágyon. Anyaként és bébiszitterként."
   - 2 CTA: [Foglalj ingyenes 15 perces telefont] (primary) +
     [Mi az Access Bars?] (secondary, scroll to anchor)
   - Trust-bar alul: "Veszprém + 30 km" • "12.000 Ft / alkalom"
     • "Anya + bébiszitter" • "Erkölcsi bizonyítvány"

2. "RÓLAM 1 PERCBEN" szekció
   - Bal: kör alakú fotó placeholder + név
   - Jobb: 3 rövid bekezdés a háttérről
   - 3 ikonos kártya: bébiszitter év / családok / Bars képzettség
   - CTA: [Olvasd el a teljes történetem] → /rolam

3. "MI AZ ACCESS BARS?" edukációs szekció
   - 4 lépéses folyamat:
     1. Foglalj időpontot
     2. Házhoz megyek
     3. 30 perces csendes pihenés a fej 32 pontján
     4. A gyereked a saját ágyában lazul el
   - Idézet box (terrakotta keret, dőlt):
     "Az Access Bars közérzetjavító, ellazulást elősegítő érintéses
     módszer. NEM orvosi kezelés, nem helyettesíti az egészségügyi
     ellátást, és nem alkalmas betegségek diagnosztizálására
     vagy kezelésére."

4. "KIKNEK AJÁNLOM?" — 4 kártya gyengéd ikonnal
   - "Gyerekeknek, akik nehezen alszanak el"
   - "Gyerekeknek, akik vizsgaidőszakban feszültek"
   - "Gyerekeknek, akik iskolakezdéskor szoronganak"
   - "Anyukáknak, akik csendes 30 percet érdemelnek"
   FONTOS: NE szerepeljen "ADHD", "autizmus", "depresszió"
   vagy bármilyen diagnózis név!

5. "CSOMAGOK ÉS ÁRAK" szekció — 3 oszlopos kártya

   Kártya A (BEMUTATÓ):
   - Cím: "Ismerd meg"
   - Ár: 8.900 Ft
   - "Csak új ügyfeleknek, egy alkalommal"
   - 1 alkalom házhoz Veszprém + 20 km
   - CTA: [Foglalom]

   Kártya B (LEGNÉPSZERŰBB — kiemelt!):
   - Cím: "Egy alkalom"
   - Ár: 12.000 Ft
   - 1 alkalom házhoz Veszprém + 30 km
   - 30 perc fej-relaxáció + kötetlen idő
   - CTA: [Foglalom]

   Kártya C (CSOMAG):
   - Cím: "3 alkalmas bérlet"
   - Ár: 32.000 Ft  ("-11%" badge)
   - 10.667 Ft / alkalom
   - 3 alkalom 8 héten belül
   - CTA: [Foglalom]

   Kisebb kártya alatta:
   "Bébiszitter + Bars kombi: 3 óra felügyelet + 1 Bars-alkalom
   17.000 Ft — egyedi szolgáltatás Veszprémben."

   30 km feletti távolságért +200 Ft/km (apróbetűs).

6. "MI TÖRTÉNIK EGY ALKALOMKOR?" idővonal
   - 0-5 perc: Megérkezés, ismerkedés a gyerekkel
   - 5-10 perc: A gyerek elhelyezkedik
   - 10-40 perc: 30 perc csendes érintés a fej 32 pontján
   - 40-50 perc: Pihenés, beszélgetés a szülővel
   Megjegyzés: "A szülő VÉGIG jelen van. Soha nincs zárt ajtó."

7. SZÜLŐI VÉLEMÉNYEK (testimonialok)
   3-4 idézet kártya, név csak keresztnévvel + város

8. GYIK (FAQ) — accordion-stílus
   - "Veszélyes?"
   - "Mit érez a gyerek?"
   - "Hány alkalom kell?"
   - "Mit visztek magatokkal?"
   - "Mi van, ha a gyerek nem akarja?"
   - "Hogyan kell fizetni?"
   - "Az ADHD-s/szorongó gyermekemen segít-e?" → ITT ÓVATOSAN:
     "Az Access Bars nem orvosi kezelés. A diagnosztizált állapotokat
     gyermekpszichiáter és pszichológus kezeli. Mi egy ellazító
     élményt kínálunk, ami sokszor jó kiegészítője lehet a szakorvosi
     ellátásnak — de nem helyettesíti azt. Beszéld meg a kezelőorvossal."

9. KAPCSOLAT / FOGLALÁS
   - Telefon, email
   - Egyszerű űrlap: Név, Telefon, Email, "Mit kérdeznél?" textarea,
     gyerek életkora dropdown (4-14)
   - GDPR checkbox
   - Submit: "Felveszem veled a kapcsolatot 24 órán belül"

10. FOOTER
    - Logó + szlogen
    - Navigáció
    - Telefon + email + FB + Instagram
    - Apró: "© 2026 [NÉV]. EV nyilv.szám: [SZÁM]."

=== KÜLÖN OLDALAK ===

/rolam — Hosszabb történet, képzettségek, "Miért HÁZHOZMENŐS?"
/mi-az-access-bars — Mélyebb edukáció, 32 pont infografika
/csomagok — Részletes ártáblázat, visszamondási szabályok
/foglalas — 4 lépéses folyamat, szülői beleegyező PDF link
/adatvedelem — GDPR (kiskorú szekcióval)
/impresszum — Cégadatok
/felelossegkizaras — Teljes disclaimer

=== SEO META TAGEK ===

<title>Access Bars Veszprém házhozmenős — gyermek relaxáció</title>
<meta name="description" content="Gyengéd, érintéses relaxációs
módszer 4-14 éves gyerekeknek. Házhoz megyek Veszprém + 30 km
körzetében. Anya és bébiszitter, akkreditált Access Bars Practitioner.
12.000 Ft / alkalom.">

=== AMIT NE TEGYÉL ===

- NE legyen pop-up "Iratkozz fel" indulásnál
- NE legyenek lila/pink csillámos elemek
- NE használj gyermekded fontot
- NE szerepeltesd: "kezelés", "terápia", "gyógyítás", "ADHD-kezelés"
- NE használj megtévesztő stockfotót
- NE ígérj mérhető eredményt

=== KÉSZÍTSD EL ===

Egy professzionális, lágy, anyaías, megbízható weboldalt, ahol egy
35 éves veszprémi anya 2 perc alatt eldönti, hogy szeretne-e foglalni
egy 15 perces ingyenes telefonos beszélgetést. Szakmaiság ÉS
otthoniasság egyszerre."""

add_code_block(doc, prompt_text)

doc.add_page_break()

# Tipp szekció
add_heading(doc, 'Plusz tippek a Lovable-höz', 2)

add_heading(doc, '1. A prompt elküldése után', 3)
add_para(doc, 'Lovable megépíti az alapot. Utána egyenként kérheted:')
add_bullet(doc, '"Cseréld le a hero szlogent erre: ..."')
add_bullet(doc, '"Adj hozzá egy 4. szülői véleményt"')
add_bullet(doc, '"A primary szín legyen kicsit sötétebb mohazöld"')

add_heading(doc, '2. Domain név javaslat', 3)
add_bullet(doc, 'gyermekrelaxacio.hu')
add_bullet(doc, 'csendespillanat.hu')
add_bullet(doc, '[neved].hu')
add_para(doc, 'Domain regisztráció: rackforest.hu vagy domain.hu, ~3.000 Ft/év.')

add_heading(doc, '3. Fotók', 3)
add_para(doc, 'Ne tölts fel a Lovable build során. Helyette Unsplash placeholderek, és cseréld le később SAJÁT fotókra. A saját fotók kritikusan fontosak — egy közeli fotó rólad mosolygósan + 1 fotó a hordozható matracoddal.')

add_heading(doc, '4. GDPR / Adatvédelmi szöveg', 3)
add_para(doc, 'NE bízd a Lovable-re. Kérj jogi sablont ügyvédtől (kb. 30.000 Ft a teljes csomag). A weboldalon csak az ő szövegét tedd fel.')

add_heading(doc, '5. Az első hét', 3)
add_para(doc, 'NE nyomd marketingre. Töltsd be az oldalt 5-10 ismerőssel, kérdezd meg, ki mit ért belőle 30 másodperc alatt. Csak utána indítsd a hirdetést.')

# Indulás előtti ellenőrzőlista
doc.add_page_break()
add_heading(doc, 'Indulás előtti ellenőrzőlista', 2, '6B8E7F')

checklist = [
    'EV bejelentve, TEÁOR 9604',
    'Erkölcsi bizonyítvány 333-as megérkezett',
    'Felelősségbiztosítás aktív',
    'Szülői beleegyező nyilatkozat (ügyvéddel)',
    'Weboldal Lovable-ben kész és élesben',
    'Google Cégprofil verifikált',
    'Facebook + Instagram oldal aktív',
    'Az első 5 hirdetési szöveg megírva',
    'Bébiszitter ügyfeleknek üzenet kiment',
    'Egy testreszabott PDF lead magnet kész (Canva)',
    'Lead magnet → MailerLite kapcsolat él',
    'Google Maps + Apple Maps szolgáltatási terület bejelölve',
]
for c in checklist:
    p = doc.add_paragraph()
    p.add_run('☐  ' + c)

add_para(doc, '')
add_para(doc, 'Ha mind a 12 megvan → indulhat a hirdetés.', bold=True, color='00B050')

# Ügyvéd-könyvelő szekció
add_heading(doc, 'Mit kérj az ügyvédtől és könyvelőtől?', 2)

add_heading(doc, 'Ügyvédnek (~80-150.000 Ft):', 3)
for t in ['Szolgáltatási szerződés sablon (szülővel)',
          'Szülői beleegyező nyilatkozat sablon (Access Bars-specifikus)',
          'GDPR adatkezelési tájékoztató (kiskorú szekcióval)',
          'Felelősségkizáró nyilatkozat szövege a weboldalra',
          'Weboldal jogi átvilágítás (egyszer)']:
    p = doc.add_paragraph(style='List Number')
    p.add_run(t)

add_heading(doc, 'Könyvelőnek (~10.000 Ft/hó):', 3)
for t in ['EV bejelentés segítség',
          'Havi számlák beérkeztetése',
          'Évi adóbevallás',
          'NAV-os ügyintézés']:
    p = doc.add_paragraph(style='List Number')
    p.add_run(t)

# Footer
doc.add_paragraph()
doc.add_paragraph()
footer = doc.add_paragraph()
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = footer.add_run('— A marketing terv vége —')
r.italic = True; r.font.color.rgb = RGBColor.from_string('595959')

footer2 = doc.add_paragraph()
footer2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = footer2.add_run('Ez a terv a 6 ügynökös piackutatás (Piackutatas_AccessBars_Veszprem.docx)\n'
                    'eredményeire épül. A teljes elemzést lásd ott.\n\n'
                    '2026. május 11.')
r.italic = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string('808080')

out = '/home/user/agency-agents-stob/piackutatas/Marketing_Terv_es_Lovable_Prompt.docx'
doc.save(out)
print(f'OK: {out}')
