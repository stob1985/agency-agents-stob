"""
Access Bars gyerekeknek - Veszprém vármegye
Piackutatási beszámoló generálása .docx formátumba
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
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


def add_table(doc, headers, rows, header_color='2F5496'):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = ''
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor.from_string('FFFFFF')
        run.font.size = Pt(10)
        shade_cell(hdr_cells[i], header_color)
    for r_idx, row in enumerate(rows):
        cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row):
            cells[c_idx].text = ''
            p = cells[c_idx].paragraphs[0]
            run = p.add_run(str(val))
            run.font.size = Pt(10)
    return table


doc = Document()

# margins
for section in doc.sections:
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2)
    section.right_margin = Cm(2)

# default style
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ===== CÍMLAP =====
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run('PIACKUTATÁSI BESZÁMOLÓ')
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = RGBColor.from_string('1F3864')

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = subtitle.add_run('Access Bars házhozmenős szolgáltatás gyerekeknek')
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = RGBColor.from_string('2F5496')

sub2 = doc.add_paragraph()
sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub2.add_run('Veszprém vármegye – döntéstámogató elemzés')
r.italic = True
r.font.size = Pt(13)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run('Készült: 2026. május 11.\n6 specializált AI kutatási ügynök párhuzamos elemzése alapján\nForrások: ~150 webes hivatkozás, KSH, NAV, jogtár, hazai és külföldi szakmai oldalak')
r.font.size = Pt(10)
r.font.color.rgb = RGBColor.from_string('595959')

doc.add_paragraph()
doc.add_paragraph()

# ===== VEZETŐI ÖSSZEFOGLALÓ =====
add_heading(doc, 'Vezetői összefoglaló', 1, '1F3864')

verdict_p = doc.add_paragraph()
r = verdict_p.add_run('VERDIKT: ')
r.bold = True
r.font.size = Pt(14)
r.font.color.rgb = RGBColor.from_string('C00000')
r2 = verdict_p.add_run('FELTÉTELES IGEN – de nem abban a formában, ahogy eredetileg tervezted.')
r2.bold = True
r2.font.size = Pt(14)

add_para(doc,
    'Az ötlet életképes mellékállásként vagy lassú építkezésű kiegészítő bevételként a bébiszitterség mellett. '
    'A 6 ügynök kutatása azonban három olyan kockázatot tárt fel (jogi, pénzügyi, reputációs), amely átírja '
    'az induló feltételeket. A korábbi (egyszerű) piackutatás ezeket nem jelezte:')

add_bullet(doc, 'Az Access Bars NINCS a 11/1997. NM rendelet 18 elismert természetgyógyászati eljárása között. '
                'A 2020-ban módosított Btk. 187. § (kuruzslás) 1-3 év szabadságvesztést ír elő engedély nélküli '
                'gyógyító tevékenységre. ADHD-ra/szorongásra/autizmusra tett gyógyhatás-állítás GVH-bírságot vonhat '
                'maga után (precedens: GymBeam 2024 = 100 millió Ft).',
                bold_prefix='JOGI:')

add_bullet(doc, 'Az 1. év várhatóan veszteséges (~-366.000 Ft). A reális szcenárió (180.000 Ft/hó) eléréséhez '
                '12-18 hónap kitartó építkezés kell. A tervezett 7-8.000 Ft-os ár alulárazott a magyar piaci '
                'átlaghoz képest (10-16.000 Ft).',
                bold_prefix='PÉNZÜGYI:')

add_bullet(doc, 'Az Access Consciousness anyaszervezet ellen dokumentált kultusz-vádak (McGill University), '
                'Scientology-kapcsolat (alapító Gary Douglas), és érintési visszaélési vádak (Dain Heer társalapító, '
                'ausztrál sajtó). Egyetlen "iskolai kísérlet" sem peer-reviewed.',
                bold_prefix='REPUTÁCIÓS:')

add_para(doc, '')
add_para(doc, 'A részletes 8 fejezet bemutatja, MIÉRT életképes mégis, és HOGYAN kell elindulni helyesen, '
              'hogy a kockázatokat minimalizáld és a valódi versenyelőnyödet (bébiszitter háttér + házhozmenős + '
              'gyerek-specializáció) kihasználd.', italic=True)

doc.add_page_break()

# ===== 1. FEJEZET =====
add_heading(doc, '1. A 3 legfontosabb új megállapítás', 1, '1F3864')

add_heading(doc, '1.1. Veszprémben már VAN direkt versenytárs gyerekekre', 2, 'C00000')
add_para(doc, 'A Csodavilág Fejlesztőközpont (Veszprém, Vilonyai u. 6/A) már kínál Access Bars-t gyermek-fejlesztő '
              'keretben, kineziológiával, gyermekjógával, hangtállal. Vagus terápia gyermek: 13.000 Ft / 30 perc. '
              'Mellette Napos Szalon (Lajkó Tamás) és Veszprém Bowen is ad gyermek-Access Bars-t 8.000 Ft-ért. '
              'A tiszta üres rés nem a "gyerek-Access Bars", hanem a HÁZHOZMENŐS + GYEREK + BÉBISZITTER HÁTTÉR '
              'kombináció.')

add_heading(doc, '1.2. Magas jogi kockázat – Btk. 187. § (kuruzslás)', 2, 'C00000')
add_para(doc, 'A 2020-as Btk. módosítás kifejezetten kiterjeszti a kuruzslást a természetgyógyászati eljárásokra. '
              'Az Access Bars NINCS a hivatalosan elismert 18 eljárás között. Bárminemű gyógyhatás-ígéret (ADHD, '
              'autizmus, szorongás, alvás) → 1-3 év szabadságvesztés + GVH-bírság akár 100 millió Ft.')

add_heading(doc, '1.3. Reputációs vörös zászlók az anyaszervezetnél', 2, 'C00000')
add_bullet(doc, 'Gary Douglas (alapító) saját bevallása szerint Raszputyin szellemétől csatornázta a 32 fej-pont '
                'koncepciót (forrás: McGill University Office for Science and Society)')
add_bullet(doc, 'Dain Heer (társalapító) ellen az ausztrál sajtó (The Australian, Houston Press) érintési '
                'visszaélési vádakat dokumentált')
add_bullet(doc, 'Nova Scotia-ban egy szociális munkás engedélyét visszavonták Access-tevékenység miatt')
add_bullet(doc, 'A Science-Based Medicine "új phrenológiának" nevezi')
add_bullet(doc, 'Egyetlen iskolai kísérlet (olasz "It\'s Okay to Be Happy", spanyol Mallorca-Biddle) sem '
                'peer-reviewed – mind az Access Consciousness saját marketinganyaga')

doc.add_page_break()

# ===== 2. FEJEZET: PIAC =====
add_heading(doc, '2. A piac – mit mutat a kutatás', 1, '1F3864')

add_heading(doc, '2.1. Veszprém vármegye demográfia és kereslet', 2)
add_table(doc,
    ['Mutató', 'Adat'],
    [
        ['Veszprém vármegye lakossága', '~340.000 fő'],
        ['Veszprém város', '55.247 fő (2025)'],
        ['Pápa / Ajka / Várpalota / Tapolca / Balatonfüred', '~105.000 fő összesen'],
        ['Veszprém vármegye 4-14 éves gyerekek', '~34.000 fő'],
        ['Wellness-tudatos diplomás szülő közönség', '5.000-7.000 gyerek (15-20%)'],
        ['ADHD-érintett gyerek vármegyei becslés', '2.700-3.400 fő'],
        ['Magyar gyermek szorongásban (UNICEF)', 'minden 5.'],
        ['Iskolai bullyingot átélt magyar tinédzser', '85%'],
        ['Veszprém átlagkereset (országos rang)', 'top-6'],
        ['Veszprém boldogság-rang 2025', '#1 Magyarországon'],
        ['Veszprém vármegye nettó átlagkereset 2024', '331.197 Ft / hó'],
    ])

add_heading(doc, '2.2. Versenytársak Veszprémben (gyerek-Access Bars)', 2)
add_table(doc,
    ['Szolgáltató', 'Ár', 'Helyszín', 'Gyerek?', 'Házhoz?'],
    [
        ['Csodavilág Fejlesztőközpont', '13.000 Ft / 30 perc (vagus)', 'Vilonyai u. 6/A', 'IGEN', 'NEM'],
        ['Napos Szalon (Lajkó Tamás)', '8.000 Ft (14 alatt)', 'Jutasi út 10.', 'IGEN', 'NEM'],
        ['Veszprém Bowen', '8.000 Ft (14 alatt)', 'Veszprém', 'IGEN', 'NEM'],
        ['Kántás Kata (A végtelenbe és tovább)', '25.000 Ft / óra (felnőtt)', 'Haszkovó u. 12/B', 'Nincs külön profil', 'Nincs info'],
        ['Teremts Velem', 'változó', 'Veszprém + GMS', 'általános', 'NEM'],
    ])

add_heading(doc, '2.3. Indirekt verseny Veszprémben', 2)
add_table(doc,
    ['Szolgáltatás', 'Szolgáltató', 'Ár'],
    [
        ['Gyermekpszichológus', 'Geiszt Johanna', '15.000 Ft / 50 perc'],
        ['Gyermekpszichológus', 'PszichoFészek', '19.000-21.000 Ft / 50 perc'],
        ['TSMT terápia', 'Veszprém TSMT, HÓRUKK, Napraforgóház', '10-15.000 Ft'],
        ['Ayres/DSZIT', 'Gyermekbolygó', 'n/a'],
        ['Kineziológia', 'Scheck Szilvia, Szófia Klinika', '10-15.000 Ft'],
        ['Logopédus / fejlesztőped.', 'sok szolgáltató', '8-12.000 Ft'],
    ])

add_heading(doc, '2.4. Külföldi minták összehasonlítása', 2)
add_table(doc,
    ['Ország / Szolgáltató', 'Ár (gyerek)', 'Forint', 'Modell'],
    [
        ['UK – Gentle Touch (vidék)', '£15 / 30 perc', '~6.800 Ft', 'low-cost vidéki'],
        ['UK – Joyful Body (rendelő)', '£125 / 75 perc', '~57.000 Ft', 'prémium'],
        ['UK – Joyful Body (házhoz)', '£150-200 / 75 perc', '68-91.000 Ft', 'prémium házhoz'],
        ['Ausztrália – Tooley', '$150 AUD', '~35.000 Ft', '+ ingyen 15 perc Discovery'],
        ['Veszprém piaci szint', '8.000-10.000 Ft', '–', 'félprémium, vidéki'],
    ])

add_para(doc, '')
add_para(doc, 'TANULSÁG a külföldi minták kutatásából:', bold=True)
add_bullet(doc, 'A "kismama-anya vagyok" narratíva (Tooley-modell) jól skáláz vidéki környezetben.')
add_bullet(doc, 'Az INGYEN 15 perces "Discovery Session" alacsony belépési küszöbet ad, magas konverzióval.')
add_bullet(doc, 'A rétegzett árazás (rendelő / házhoz / csomag / képzés) működik – Joyful Body modell.')
add_bullet(doc, 'Az olasz/spanyol "iskolai kísérletek" NEM peer-reviewed, csak Access marketinganyag – '
                'magyar szülő előtt érvként ne használd, könnyen cáfolható.')

doc.add_page_break()

# ===== 3. FEJEZET: PÉNZÜGYI =====
add_heading(doc, '3. Pénzügyi életképesség', 1, '1F3864')

add_heading(doc, '3.1. Három forgatókönyv (havi/éves bevétel)', 2)
add_table(doc,
    ['Mutató', 'Pesszimista', 'Reális', 'Optimista'],
    [
        ['Alkalom / hét', '2', '5', '10'],
        ['Alkalom / hó', '8', '20', '40'],
        ['Átlag ár', '8.000 Ft', '9.000 Ft', '10.000 Ft'],
        ['Havi bruttó', '64.000 Ft', '180.000 Ft', '400.000 Ft'],
        ['Éves bruttó', '768.000 Ft', '2.160.000 Ft', '4.800.000 Ft'],
    ])

add_heading(doc, '3.2. Induló költségek (jogilag tiszta verzió)', 2)
add_table(doc,
    ['Tétel', 'Összeg'],
    [
        ['EV indítás (NAV ÜPO)', '0 Ft'],
        ['Speciális gyermekvédelmi (333-as) erkölcsi bizonyítvány', '3.100 Ft'],
        ['Kamarai hozzájárulás (VMKIK)', '5.000 Ft / év'],
        ['Szakmai felelősségbiztosítás', '~50.000 Ft / év'],
        ['Jogi tanácsadás + sablonok (szülői beleegyező, GDPR)', '80-150.000 Ft'],
        ['Könyvelő (átalányadó, ~10.000 Ft / hó)', '120.000 Ft / év'],
        ['Hordozható matrac, eszközök', '50-110.000 Ft'],
        ['Weboldal (Wix/WordPress)', '0-150.000 Ft'],
        ['INDULÓ ÖSSZKÖLTSÉG', '260.000 – 600.000 Ft'],
    ])

add_heading(doc, '3.3. Havi rezsi (reális szcenárió)', 2)
add_table(doc,
    ['Tétel', 'Összeg'],
    [
        ['Üzemanyag (Veszprém + 30 km, 20 alk × 30 km)', '35.000 Ft'],
        ['Marketing / hirdetés', '20.000 Ft'],
        ['Telefon / internet (üzleti rész)', '5.000 Ft'],
        ['KATA havi tételes', '50.000 Ft'],
        ['Eszközpótlás', '5.000 Ft'],
        ['HAVI ÖSSZESEN', '~115.000 Ft'],
    ])

add_heading(doc, '3.4. 3 éves pénzügyi forecast (reális)', 2)
add_table(doc,
    ['Mutató', 'Év 1 (rampup)', 'Év 2 (stabil)', 'Év 3 (növekedés)'],
    [
        ['Éves bevétel', '914.000 Ft', '2.576.000 Ft', '4.300.000 Ft'],
        ['Éves költség', '1.280.000 Ft', '1.340.000 Ft', '1.580.000 Ft'],
        ['NETTÓ EREDMÉNY', '-366.000 Ft', '+1.236.000 Ft', '+2.720.000 Ft'],
        ['Havi nettó átlag', '-30.000 Ft', '+103.000 Ft', '+227.000 Ft'],
    ])

add_para(doc, '')
add_para(doc, 'Break-even: ~10 alkalom/hó (havi ~80.000 Ft fix költségnél). Reális szcenárió eléréséhez: 12-18 hónap.',
         bold=True)

add_heading(doc, '3.5. Az árazás kritikája', 2)
add_para(doc, 'A korábbi 7-8.000 Ft / alkalom ALULÁRAZOTT a piaci helyzethez képest:')
add_bullet(doc, 'Csodavilág Fejlesztőközpont: 13.000 Ft / 30 perc (vagus)')
add_bullet(doc, 'Magyar gyerek-Access Bars országos átlag: 10.000-16.000 Ft')
add_bullet(doc, 'Veszprém gyermekpszichológus: 15.000-21.000 Ft / 50 perc')
add_para(doc, 'JAVASOLT ár: 9.000 Ft (saját tér) / 12.000 Ft (házhozmenős). 3 alkalmas csomag: 30.000 Ft (10% kedvezmény).',
         bold=True, color='2F5496')

doc.add_page_break()

# ===== 4. FEJEZET: JOGI =====
add_heading(doc, '4. Jogi kötelező minimum (NEM opcionális!)', 1, '1F3864')

add_heading(doc, '4.1. 12 lépéses jogi indulási csomag', 2)
steps = [
    'EV indítás + átalányadózás (NAV ÜPO, ingyenes online)',
    'TEÁOR 9604 / szakmakód 960404 – "Fizikai közérzetet javító szolgáltatás" (NEM 86.90 egészségügyi!)',
    'Veszprémi sávos HIPA – 50.000 Ft / év',
    'Kamarai regisztráció VMKIK-nél – 5.000 Ft, márc. 31-ig',
    'Speciális gyermekvédelmi (333-as) erkölcsi bizonyítvány – 3.100 Ft (SZÜLŐK ELVÁRJÁK)',
    'Szakmai felelősségbiztosítás kiskorúra + harmadik fél otthonára (min. 10 M Ft/eset), ~50.000 Ft/év',
    'Access Bars Facilitator szint megszerzése idővel (bizalomépítő, nem jogi követelmény)',
    'Írásbeli sablonok ügyvéddel: szülői beleegyező, GDPR (16 év alatt KÖTELEZŐ), szolgáltatási szerződés, jogi disclaimer',
    'Weboldal jogi átvilágítás – minden "gyógyhatás" szóra utalás KIIRTANI',
    'NE menj iskolába/óvodába intézményi keretben (csak otthoni szülői megrendelés)',
    'Mindig szülő jelenlétében dolgozz – SOHA ne legyél kettesben a gyerekkel',
    'Évente jogi és könyvelői felülvizsgálat (~100-200 ezer Ft/év)',
]
for i, s in enumerate(steps, 1):
    p = doc.add_paragraph(style='List Number')
    p.add_run(s)

add_heading(doc, '4.2. Mit SZABAD és mit NEM mondani', 2)
add_table(doc,
    ['SZABAD (✓)', 'TILOS (✗) – kuruzslás / GVH-bírság'],
    [
        ['"relaxációs élmény"', '"ADHD kezelése"'],
        ['"ellazító érintéses módszer"', '"autizmust enyhíti"'],
        ['"gyermekek számára kifejlesztett"', '"szorongást gyógyítja"'],
        ['"stresszoldás, közérzetjavítás"', '"iskolai teljesítményt javít"'],
        ['"érintéses energetikai módszer"', '"minden gyereken segít"'],
        ['Kötelező disclaimer minden anyagban', '"helyettesíti az orvosi ellátást"'],
    ])
add_para(doc, '')
add_para(doc, 'KÖTELEZŐ disclaimer minden hirdetésen, weboldalon, szórólapon:',  bold=True)
add_para(doc, '"Az Access Bars közérzetjavító, ellazulást elősegítő érintéses módszer, amely nem orvosi kezelés, '
              'nem helyettesíti az egészségügyi ellátást, és nem alkalmas betegségek kezelésére."',
              italic=True, color='C00000')

add_heading(doc, '4.3. Hivatkozott jogszabályok', 2)
laws = [
    '1997. évi CLIV. törvény az egészségügyről (Eütv.) 104. §',
    '40/1997. (III. 5.) Korm. rendelet a természetgyógyászati tevékenységről',
    '11/1997. (V. 28.) NM rendelet (a 18 elismert eljárás – Access Bars NINCS köztük!)',
    '2012. évi C. törvény (Btk.) 187. § – Kuruzslás (2020. évi módosítás)',
    '2008. évi XLVIII. törvény (Grtv.) – gazdasági reklámtevékenység',
    '2008. évi XLVII. törvény (Fttv.) – tisztességtelen kereskedelmi gyakorlat',
    'GDPR (EU 2016/679) 8. cikk – gyermekek adatvédelme (16 év alatt szülői hozzájárulás)',
]
for l in laws:
    add_bullet(doc, l)

doc.add_page_break()

# ===== 5. FEJEZET: MARKETING =====
add_heading(doc, '5. Marketing- és hirdetési stratégia', 1, '1F3864')

add_heading(doc, '5.1. Veszprém-specifikus platformok', 2)
add_table(doc,
    ['Platform', 'Költség', 'Stratégia'],
    [
        ['Google Cégprofil', 'ingyenes', '30 km szolgáltatási terület, min. 5 review az első hónapban'],
        ['Veszprémimami portál (imami.hu)', '15-25.000 Ft / hó banner/PR-cikk', 'Helyi szülői közönség, legjobb célzás'],
        ['Helyi FB csoportok', 'ingyenes (organikus)', 'Heti 1 értékadó poszt – Gyerekprogramok Veszprém és környékén, Veszprémi Mami klub'],
        ['Facebook / Instagram hirdetés', '20-30.000 Ft / hó', 'Célzás: nők 28-45, Veszprém + 30 km'],
        ['Google Ads', '20.000 Ft / hó', 'Brand + helyi kulcsszavak, CPC ~100-300 Ft'],
        ['Veol.hu / Vehir.hu PR-cikk', '30-80.000 Ft', 'Esetenkénti megjelenés'],
        ['Waldorf közösség (Csillagvár, Fehérlófia)', 'ingyenes', 'Ingyenes bemutató workshop szülői körnek'],
    ])

add_heading(doc, '5.2. Helyi szülői Facebook csoportok (becsült taglétszám)', 2)
add_table(doc,
    ['Csoport', 'Becsült tag'],
    [
        ['Adok-Veszek [Veszprém]', '30-50.000'],
        ['Veszprém megye adok-veszek', '50.000+'],
        ['Gyerekprogramok Veszprém és környékén', '5-15.000'],
        ['Veszprém és környéke Baba-Mama Adok-Veszek', '10-20.000'],
        ['Veszprém Fórum', '15-50.000'],
        ['Veszprémi Mami klub', '1-3.000 (több kiscsoport)'],
        ['Veszprémi Waldorf Egyesület', '1-3.000'],
    ])

add_heading(doc, '5.3. 6 hónapos marketing-keret', 2)
add_table(doc,
    ['Hónap', 'Keret', 'Fókusz'],
    [
        ['1', '70.000 + 150.000 egyszeri', 'Weblap, Google Cégprofil, FB/IG profil'],
        ['2', '90.000 Ft', 'Első fizetett kampányok, Veszprémimami partnerség'],
        ['3', '100.000 Ft', 'Lookalike, mikroinfluencer'],
        ['4', '120.000 Ft', 'Skálázás'],
        ['5', '120.000 Ft', 'Helyi rendezvény (Gizella Napok, Gyermeknap)'],
        ['6', '100.000 Ft', 'Optimalizáció, retention'],
        ['Összesen', '~750.000 Ft', '6 hó marketing-büdzsé'],
    ])

add_heading(doc, '5.4. 3 célcsoport-specifikus üzenet', 2)

add_para(doc, 'CÉLCSOPORT 1: ADHD-s gyermek anyja', bold=True)
add_para(doc, 'Hangvétel: empatikus, megértő. "Tudom, milyen érzés, mikor reggel 7-kor már kétszer kiabáltál. '
              'Anyaként és bébiszitterként láttam, hogy az ADHD-s gyerekek néha csak egyetlen dolgot szeretnének: '
              'egy pillanatra elcsendesedni. Az Access Bars egy gyengéd érintéses módszer – nem gyógyszer, '
              'nem helyettesíti az orvost. Házhoz megyek Veszprém + 30 km."', italic=True)

add_para(doc, '')
add_para(doc, 'CÉLCSOPORT 2: Szorongó gyermek szülei', bold=True)
add_para(doc, 'Hangvétel: nyugtató, biztonságot adó. "\'Nem akarok iskolába menni.\' Ezt hallottad ma reggel? '
              'A szorongás 6-12 éves gyerekeknél gyakran hasfájással, hisztivel, alvászavarral jelentkezik. '
              'Bébiszitterként száz családnál láttam. Az Access Bars 60 perces, fájdalommentes érintés a fejen, '
              'ami sok gyereknél visszahozza a nyugalmat – a saját ágyukban."', italic=True)

add_para(doc, '')
add_para(doc, 'CÉLCSOPORT 3: Alvászavaros gyermek szülei', bold=True)
add_para(doc, 'Hangvétel: gyakorlatias, eredmény-orientált. "Hány órakor aludt el legutóbb a gyermeked '
              'küzdelem nélkül? A 4-14 évesek 30%-a küzd elalvási nehézséggel. Az Access Bars 32 fejen lévő '
              'pontot érint meg. Veszprém + 30 km házhoz."', italic=True)

doc.add_page_break()

# ===== 6. FEJEZET: GO/NO-GO =====
add_heading(doc, '6. Go / No-Go önvizsgálati mátrix', 1, '1F3864')

add_para(doc, 'Tedd fel magadnak ezt a 6 kérdést. Ha 5+ IGEN → érdemes belevágni. Ha 4 vagy kevesebb → '
              'ne kezdd el most.', bold=True)

questions = [
    ('1', 'Van 600 ezer – 1 millió Ft tartalékom (vagy más állandó jövedelmem) az 1. évre?'),
    ('2', 'Folytatom a bébiszitterséget párhuzamosan legalább 12-18 hónapig?'),
    ('3', 'Elfogadom, hogy NEM ígérhetek gyógyhatást (ADHD, szorongás), és csak "ellazulást" kommunikálok?'),
    ('4', 'Beszerzem az erkölcsi bizonyítványt + felelősségbiztosítást + jogi sablonokat (~260 ezer Ft) az indulás előtt?'),
    ('5', 'Mindig szülő jelenlétében dolgozom és írásos beleegyezést kérek?'),
    ('6', 'Vállalom, hogy 18 hónapig türelmesen építem a klientélát ajánlások és organikus tartalom mentén?'),
]
add_table(doc, ['#', 'Kérdés', 'Válaszom (IGEN/NEM)'],
          [[n, q, '□'] for n, q in questions])

add_heading(doc, '6.1. NO-GO jelek (ha látod, ne indulj el / állj le)', 2, 'C00000')
no_go = [
    'Nincs 6 hónapra elég tartalékod (alatta a KATA havi 50.000 Ft is megfojthatja)',
    'Érzelmileg kötődsz az "Access Bars meggyógyítja az ADHD-t" üzenethez',
    'Nem tudod kezelni a szkeptikus reakciókat (Szkeptikus Fórum, McGill-cikk visszaköszön)',
    '6. hónap után < 8 alkalom/hó és nincs növekvő trend',
    '12. hónap után még mindig veszteséges',
    'Ügyfélből < 30% a visszatérő (nem alakul ki retenció)',
]
for n in no_go:
    add_bullet(doc, n)

add_heading(doc, '6.2. Skálázási jelek (BŐVÍTÉS)', 2, '00B050')
go = [
    '6. hónap után stabilan 15+ alkalom/hó, várólista van',
    '70%+ visszatérő ügyfél',
    'Szülők kérdezgetik: "Lehet-e workshop?", "Van-e csomag?"',
    'Iskolai/óvodai együttműködési ajánlat érkezik (SZÜLŐI körön át, nem intézményi!)',
    '→ Ekkor: árképzés emelése, MTVSS tanfolyam, csoportos workshopok',
]
for g in go:
    add_bullet(doc, g)

doc.add_page_break()

# ===== 7. FEJEZET: 30-60-90 NAPOS AKCIÓTERV =====
add_heading(doc, '7. 30 / 60 / 90 napos akcióterv', 1, '1F3864')

add_heading(doc, '0-2. HÉT – Jogi alap', 2)
weeks = [
    'EV bejelentkezés online + 9604 TEÁOR (ingyenes)',
    'Erkölcsi bizonyítvány (333-as) megigénylése',
    'Felelősségbiztosítás megkötése',
    'Ügyvéddel szerződés-sablonok elkészítése',
    'Bébiszitter ügyfeleidnek emaillel/üzenetben felajánlani 5.500 Ft kedvezményes első kezelést',
]
for w in weeks:
    add_bullet(doc, w)

add_heading(doc, '3-4. HÉT – Online jelenlét', 2)
weeks34 = [
    'Google Cégprofil ingyen + 30 km szolgáltatási terület',
    'Egyoldalas weboldal (Wix vagy WordPress) – 60-150 ezer Ft',
    'Facebook + Instagram oldal – "Anya vagyok, X évig bébiszitterkedtem" narratíva',
    'Belépés helyi FB csoportokba (Veszprémimami, Gyerekprogramok Veszprém és környéke)',
    'Első blogposzt + Facebook bemutatkozás',
]
for w in weeks34:
    add_bullet(doc, w)

add_heading(doc, '2-3. HÓNAP – Tartalom és első hirdetés', 2)
m23 = [
    'Heti 1 blogposzt szülői problémákról (DE NEM DIAGNÓZIS!)',
    'Veszprémimami partneri PR-cikk (15-25.000 Ft)',
    'Facebook hirdetés indítása napi 800-1.000 Ft kerettel',
    'Csillagvár Waldorf Óvoda + Fehérlófia Waldorf – ingyenes szülői bemutató workshop ajánlása '
    '(NEM intézményen belül, csak szülői körnek!)',
    'Google Ads kis kampány Veszprém + brand kulcsszavakra',
]
for m in m23:
    add_bullet(doc, m)

add_heading(doc, '4-6. HÓNAP – Skálázás', 2)
m46 = [
    'Lookalike közönség építés Facebook Pixellel',
    'Augusztusi szezonális kampány: "Iskolakezdés stresszmentesen" csomag',
    'Mikroinfluencer együttműködés 1 helyi anyukával (30-50.000 Ft)',
    'Ajánlási rendszer: -20% új ügyfél hozóknak',
    'Ajándékutalvány: karácsony előtti kampány (nov-dec szezonális csúcs)',
]
for m in m46:
    add_bullet(doc, m)

add_heading(doc, '7.1. Szezonalitás – mikor van csúcs és mélypont', 2)
add_table(doc,
    ['Időszak', 'Kereslet'],
    [
        ['Szept-okt (iskolakezdés)', 'CSÚCS – szorongás, alkalmazkodás'],
        ['Nov-dec', 'Magas (téli depri + ajándékutalvány)'],
        ['Jan-feb (féléves vizsgaidőszak)', 'CSÚCS – szülői pánik'],
        ['Márc-ápr', 'Közepes'],
        ['Máj-jún (év végi vizsgák)', 'CSÚCS – év végi szorongás'],
        ['Júl-aug (nyári szünet)', 'MÉLYPONT – családok nyaralnak'],
    ])

doc.add_page_break()

# ===== 8. FEJEZET: ÖSSZEGZÉS =====
add_heading(doc, '8. Végső ajánlás – mit mondanék barátként', 1, '1F3864')

add_para(doc, 'A "feltételes IGEN" 8 feltétele:', bold=True, size=13)

points = [
    ('1', 'Indítsd MELLÉKÁLLÁSBAN, a bébiszitterség folytatása mellett – NE főállásként.'),
    ('2', 'Áldozz 260-330 ezer Ft-ot a jogi alapokra indulás előtt (felelősségbiztosítás, ügyvéd, '
          'erkölcsi bizonyítvány, könyvelő). Ez NEM opció.'),
    ('3', 'Árazd fel: 9.000 Ft / 12.000 Ft (házhoz). A 7-8.000 Ft alulárazott.'),
    ('4', 'A kommunikációd legyen szigorúan "ellazító relaxáció" – SOHA ne diagnózisra (ADHD, autizmus). '
          'Ez nem stilisztika, hanem büntetőjogi védelem.'),
    ('5', 'A bébiszitter háttered az igazi versenyelőnyöd – építsd erre a márkát '
          '("Anya vagyok, X évig bébiszitterkedtem").'),
    ('6', '3 / 6 / 12 hónapos checkpointokat állíts be: ha 6. hónapig nincs 10 alkalom/hó, gondolkodj újra.'),
    ('7', 'A Waldorf közösség (Csillagvár, Fehérlófia) és a meglévő bébiszitter ügyfeleid a leggyorsabb '
          'belépési kapuid – tőlük indulj, nem hideg hirdetéssel.'),
    ('8', 'NE építs iskolai/óvodai programra – Magyarországon ez büntetőjogi bombamező. '
          'Az olasz/spanyol "kísérletek" nem peer-reviewed bizonyítékok.'),
]
for n, t in points:
    p = doc.add_paragraph()
    r1 = p.add_run(f'{n}. ')
    r1.bold = True
    r1.font.color.rgb = RGBColor.from_string('2F5496')
    p.add_run(t)

add_para(doc, '')
add_heading(doc, '8.1. Az igazi versenyelőnyöd', 2, '00B050')
add_para(doc, 'A "házhozmenős + gyerek-specializáció + bébiszitter háttér" hármas valódi differenciáló érték '
              'Veszprém vármegyében. Egyik versenytárs sem rendelkezik mindhárommal. Erre kell felépíteni '
              'a márkát – nem a "Access Bars" technológiára (amit jogilag és tudományosan is kockázatos '
              'kommunikálni), hanem a TE személyes történetedre és a GYEREKEKKEL kapcsolatos tapasztalatodra.')

add_heading(doc, '8.2. Reális első éves várakozás', 2)
add_table(doc,
    ['Mutató', 'Érték'],
    [
        ['Kezelések száma év 1', '150-300 alkalom'],
        ['Bevétel év 1', '1,2-3 millió Ft'],
        ['Megtérülési pont (induló befektetés)', '~10-12. hónap'],
        ['Stabilizálódás (év 2)', '300-500 alkalom, 3-5 M Ft'],
        ['Főállásnyi jövedelem (év 3)', '~225.000 Ft / hó nettó'],
    ])

doc.add_page_break()

# ===== FORRÁSOK =====
add_heading(doc, '9. Kulcs források', 1, '1F3864')

add_heading(doc, '9.1. Demográfia és statisztika', 2)
sources = [
    'KSH STADAT 22.1.2.1 – lakónépesség vármegye: ksh.hu/stadat_files/nep/hu/nep0034.html',
    'KSH 50 legnépesebb település 2025: ksh.hu/stadat_files/fol/hu/fol0014.html',
    'KSH Veszprém vármegye számokban: ksh.hu/docs/hun/xftp/idoszaki/regiok/mesz/19_ve.pdf',
    'HR Portál nettó átlagkereset vármegyék',
]
for s in sources:
    add_bullet(doc, s)

add_heading(doc, '9.2. Versenytársak (Veszprém)', 2)
comp = [
    'Csodavilág Fejlesztőközpont: csodavilagfejlesztokozpont.hu',
    'Veszprém Bowen: veszprembowen.hu/access-bars-feszultsegoldo-fejkezeles/',
    'Kántás Kata: avegtelenbeestovabb.hu',
    'Teremts Velem: teremtsvelem.hu/access-bars-tanfolyam/',
    'Geiszt Johanna gyermekpszichológus: geisztjohanna.hu/rendeles-arak/',
    'PszichoFészek árak: pszichofeszek.hu/arak.html',
]
for c in comp:
    add_bullet(doc, c)

add_heading(doc, '9.3. Jogszabályok', 2)
laws_src = [
    '11/1997. (V. 28.) NM rendelet: net.jogtar.hu/jogszabaly?docid=99700011.nm',
    '40/1997. (III. 5.) Korm. rendelet: net.jogtar.hu/jogszabaly?docid=99700040.kor',
    '1997. évi CLIV. (Eütv.): net.jogtar.hu/jogszabaly?docid=99700154.tv',
    'Btk. 187. § Kuruzslás: lorik.hu/bunteto-ugyek/kuruzslas.html',
    'TEÁOR 9604: teaorszamok.hu/9604/',
    'NAV Átalányadózás 2026 információs füzet',
    'KATA 2026 szabályai: katakonyveles.hu/kata-valtozas-2026/',
]
for l in laws_src:
    add_bullet(doc, l)

add_heading(doc, '9.4. Külföldi szolgáltatók (referencia)', 2)
foreign = [
    'Danielle Tooley (AU): danielletooley.com/kids-access-consciousness/',
    'Gentle Touch Bars (UK): gentletouchbars.wordpress.com/access-bars-for-children/',
    'Access Joyful Body (UK – London/Croydon): accessjoyfulbody.com/bars-for-kids/',
    'Intuitive Understanding (CA): intuitiveunderstanding.com/access-bars/',
    'Kate L. McCarthy (USA): katelmccarthy.com/bars-for-kids/',
]
for f in foreign:
    add_bullet(doc, f)

add_heading(doc, '9.5. Kritikai források', 2)
crit = [
    'Science-Based Medicine: sciencebasedmedicine.org/access-consciousness-a-new-version-of-phrenology/',
    'McGill University OSS: mcgill.ca/oss/article/critical-thinking/rasputin-phrenology-and-dark-allegations-madness-access-consciousness',
    'Edzard Ernst: edzardernst.com/2021/12/access-consciousness-alternative-medicine-or-cult/',
    'Szkeptikus Fórum: forum.szkeptikus.hu/viewtopic.php?t=987',
    'Hoxa.hu Access Bars vélemények: hoxa.hu/access-bars-velemenyek-forum',
    'Karizmatikus.hu kritika: karizmatikus.hu/hitvedelem/teveszme-kritika-oesszefoglalo-irasok/9922-access-bars-nagyon-nem-ajanljuk/',
]
for c in crit:
    add_bullet(doc, c)

# Footer
doc.add_paragraph()
footer = doc.add_paragraph()
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = footer.add_run('— A jelentés vége —')
r.italic = True
r.font.color.rgb = RGBColor.from_string('595959')

footer2 = doc.add_paragraph()
footer2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = footer2.add_run('Készítette: 6 specializált AI kutatási ügynök párhuzamos elemzése\n'
                    '2026. május 11.')
r.italic = True
r.font.size = Pt(9)
r.font.color.rgb = RGBColor.from_string('808080')

output_path = '/home/user/agency-agents-stob/piackutatas/Piackutatas_AccessBars_Veszprem.docx'
doc.save(output_path)
print(f'OK: {output_path}')
