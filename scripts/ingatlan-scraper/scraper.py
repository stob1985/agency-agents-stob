#!/usr/bin/env python3
"""
Ingatlan.com Budapest scraper - emberi böngészést utánzó Playwright alapú megoldás
Kerületek: I, II, XI (Sasad & Bartók Béla), XII
Feltételek: felújítandó/befejezetlen, 120M Ft alatt, max 1.4M Ft/nm, stb.
"""

import json
import csv
import time
import random
import math
import re
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from playwright_stealth import stealth_sync

# ── Keresési URL-ek ────────────────────────────────────────────────────────────
SEARCH_URLS = [
    {
        "label": "I. kerület – felújítandó",
        "url": "https://ingatlan.com/i-ker/elado+lakas?allapot=felujitando",
    },
    {
        "label": "II. kerület – felújítandó",
        "url": "https://ingatlan.com/ii-ker/elado+lakas?allapot=felujitando",
    },
    {
        "label": "XI. kerület – felújítandó",
        "url": "https://ingatlan.com/xi-ker/elado+lakas?allapot=felujitando",
    },
    {
        "label": "XII. kerület – felújítandó",
        "url": "https://ingatlan.com/xii-ker/elado+lakas?allapot=felujitando",
    },
]

# ── Szűrési kritériumok ────────────────────────────────────────────────────────
MAX_PRICE_M_FT     = 120      # 120 millió Ft
MAX_PRICE_PER_SQM  = 1_400_000  # 1.4M Ft/nm
MIN_FLOOR          = 1        # legalább 1. emelet
# Ha emelet >= 2, csak liftes ház fogadható el
ELEVATOR_REQUIRED_FROM_FLOOR = 2
# Épület kora: 1950 előtt VAGY 1980 után
BUILD_YEAR_OLD_MAX = 1950
BUILD_YEAR_NEW_MIN = 1980
# Kilátás: utcai, kertre néző, panorámás
ALLOWED_VIEWS = {"utcai", "kertre néző", "kertkapcsolatos", "panorámás", "panoráma"}
# Állapot (lakás): felújítandó, befejezetlen
ALLOWED_CONDITIONS = {"felújítandó", "befejezetlen", "felújítandó-befejezetlen"}
# Kerületen belül csak ezek az utcák/területek érdekelnek a XI-ben
XI_ALLOWED_AREAS = ["sasad", "bartók béla"]

OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)


# ── Emberi késés segédeszközök ─────────────────────────────────────────────────

def human_delay(min_s: float = 0.8, max_s: float = 2.5) -> None:
    """Véletlenszerű, emberi szünet."""
    time.sleep(random.uniform(min_s, max_s))


def slow_type(page, selector: str, text: str) -> None:
    """Karakterenkénti gépelés véletlenszerű késéssel."""
    page.click(selector)
    for char in text:
        page.type(selector, char, delay=random.randint(60, 180))
        time.sleep(random.uniform(0.02, 0.08))


def human_scroll(page, steps: int = 5) -> None:
    """Emberi görgetést szimulál: lassú, véletlenszerű lépések."""
    for _ in range(steps):
        delta = random.randint(200, 600)
        page.mouse.wheel(0, delta)
        time.sleep(random.uniform(0.3, 0.9))


def random_mouse_move(page) -> None:
    """Véletlenszerű egérmozgás az oldalon."""
    width  = page.viewport_size["width"]
    height = page.viewport_size["height"]
    x = random.randint(100, width - 100)
    y = random.randint(100, height - 100)
    page.mouse.move(x, y)
    time.sleep(random.uniform(0.1, 0.4))


# ── Szűrési logika ─────────────────────────────────────────────────────────────

def parse_price_ft(text: str) -> int | None:
    """'89 900 000 Ft' → 89900000"""
    m = re.sub(r"[^\d]", "", text)
    return int(m) if m else None


def parse_sqm(text: str) -> float | None:
    """'58 m²' → 58.0"""
    m = re.search(r"([\d,\.]+)\s*m", text, re.IGNORECASE)
    if m:
        return float(m.group(1).replace(",", "."))
    return None


def parse_floor(text: str) -> int | None:
    """
    'földszint' → 0
    '2. emelet' → 2
    '4/3. emelet' → 3  (épület/emelet)
    """
    text = text.lower().strip()
    if "földszint" in text:
        return 0
    m = re.search(r"(\d+)\.\s*emelet", text)
    if m:
        return int(m.group(1))
    # pl. "4/3" → 3
    m2 = re.search(r"\d+/(\d+)", text)
    if m2:
        return int(m2.group(1))
    return None


def passes_xi_area_filter(address: str) -> bool:
    """XI. kerületnél csak Sasad és Bartók Béla út területek."""
    addr_low = address.lower()
    for area in XI_ALLOWED_AREAS:
        if area in addr_low:
            return True
    return False


def listing_passes_filter(listing: dict) -> tuple[bool, str]:
    """
    Visszaad (True, '') ha az ingatlan megfelel a feltételeknek,
    vagy (False, 'ok') ahol ok az elutasítás oka.
    """
    district = listing.get("district", "")
    address  = listing.get("address", "")

    # XI. ker.: csak Sasad / Bartók Béla területek
    if "xi" in district.lower() or "11" in district:
        if not passes_xi_area_filter(address):
            return False, f"XI. ker. de nem Sasad/Bartók Béla: {address}"

    # Ár
    price = listing.get("price_ft")
    if price is None:
        return False, "Nincs ár"
    if price > MAX_PRICE_M_FT * 1_000_000:
        return False, f"Túl drága: {price/1e6:.1f}M Ft"

    # Nm ár
    area_sqm = listing.get("area_sqm")
    if area_sqm and area_sqm > 0:
        price_per_sqm = price / area_sqm
        if price_per_sqm > MAX_PRICE_PER_SQM:
            return False, f"Nm ár túl magas: {price_per_sqm/1e6:.2f}M Ft/m²"

    # Emelet
    floor = listing.get("floor")
    if floor is not None:
        if floor < MIN_FLOOR:
            return False, f"Túl alacsony emelet: {floor}"
        if floor >= ELEVATOR_REQUIRED_FROM_FLOOR:
            if not listing.get("has_elevator", False):
                return False, f"{floor}. emelet de nincs lift"

    # Épület kora
    year = listing.get("build_year")
    if year:
        if not (year < BUILD_YEAR_OLD_MAX or year > BUILD_YEAR_NEW_MIN):
            return False, f"Épület kora nem megfelelő: {year}"

    # Kilátás (opcionális – ha nincs adat, nem szűrjük ki)
    view = listing.get("view", "").lower()
    if view and not any(v in view for v in ALLOWED_VIEWS):
        return False, f"Nem megfelelő kilátás: {view}"

    # Állapot
    condition = listing.get("condition", "").lower()
    if condition and not any(c in condition for c in ALLOWED_CONDITIONS):
        return False, f"Nem megfelelő állapot: {condition}"

    return True, ""


# ── Adatkinyerés egy listázó kártyából ────────────────────────────────────────

def extract_card_data(card, district_label: str) -> dict:
    """Kinyeri az adatokat egy hirdetéskártyából."""
    data = {"district": district_label, "source_url": ""}

    # Cím / URL
    try:
        link = card.query_selector("a[href]")
        if link:
            href = link.get_attribute("href") or ""
            data["source_url"] = "https://ingatlan.com" + href if href.startswith("/") else href
    except Exception:
        pass

    # Cím szöveg
    try:
        addr_el = card.query_selector("[class*='address'], [class*='Address'], h3, h2")
        if addr_el:
            data["address"] = addr_el.inner_text().strip()
    except Exception:
        data["address"] = ""

    # Ár
    try:
        price_el = card.query_selector("[class*='price'], [class*='Price']")
        if price_el:
            price_text = price_el.inner_text().strip()
            data["price_text"] = price_text
            parsed = parse_price_ft(price_text)
            if parsed:
                data["price_ft"] = parsed
    except Exception:
        pass

    # Alapterület
    try:
        for el in card.query_selector_all("[class*='param'], [class*='detail'], li, span"):
            txt = el.inner_text().strip()
            if "m²" in txt or "m2" in txt.lower():
                sqm = parse_sqm(txt)
                if sqm:
                    data["area_sqm"] = sqm
                    break
    except Exception:
        pass

    # Emelet
    try:
        for el in card.query_selector_all("li, span, [class*='param']"):
            txt = el.inner_text().strip().lower()
            if "emelet" in txt or "földszint" in txt:
                fl = parse_floor(txt)
                if fl is not None:
                    data["floor"] = fl
                break
    except Exception:
        pass

    # Lift
    try:
        full_text = card.inner_text().lower()
        data["has_elevator"] = "lift" in full_text and "lifttel" in full_text or "liftes" in full_text
    except Exception:
        data["has_elevator"] = False

    # Épület kora / építési év
    try:
        for el in card.query_selector_all("li, span, [class*='param']"):
            txt = el.inner_text().strip()
            m = re.search(r"\b(18|19|20)\d{2}\b", txt)
            if m:
                yr = int(m.group())
                if 1800 < yr <= 2030:
                    data["build_year"] = yr
                    break
    except Exception:
        pass

    # Kilátás
    try:
        full_text = card.inner_text().lower()
        for v in ALLOWED_VIEWS:
            if v in full_text:
                data["view"] = v
                break
    except Exception:
        pass

    # Állapot
    try:
        full_text = card.inner_text().lower()
        for c in ALLOWED_CONDITIONS:
            if c in full_text:
                data["condition"] = c
                break
    except Exception:
        pass

    return data


# ── Oldalak végigpörgetése ─────────────────────────────────────────────────────

def scrape_search_page(page, url: str, label: str) -> list[dict]:
    """Egyetlen keresési oldalt (+ lapozn) végigkeres és visszaadja a találatokat."""
    results = []
    page_num = 1

    current_url = url
    while True:
        print(f"\n  [{label}] Oldal #{page_num}: {current_url}")
        try:
            page.goto(current_url, wait_until="domcontentloaded", timeout=30_000)
        except PlaywrightTimeout:
            print("  ⚠ Oldalbetöltés timeout, megpróbálom újra...")
            time.sleep(5)
            try:
                page.goto(current_url, wait_until="domcontentloaded", timeout=40_000)
            except PlaywrightTimeout:
                print("  ✗ Sikertelen, következő URL-re lépek.")
                break

        human_delay(2, 4)
        random_mouse_move(page)
        human_scroll(page, steps=random.randint(3, 7))
        human_delay(1, 2)

        # Cookie banner elutasítás (ha van)
        for sel in ["button[id*='reject'], button[id*='decline'], [class*='cookie'] button"]:
            try:
                btn = page.query_selector(sel)
                if btn and btn.is_visible():
                    btn.click()
                    human_delay(0.5, 1.5)
                    break
            except Exception:
                pass

        # Kártyák keresése
        cards = page.query_selector_all(
            "[class*='listing-card'], [class*='ListingCard'], "
            "[class*='property-card'], article[class*='listing'], "
            "div[data-id], [class*='card--property']"
        )
        print(f"  → {len(cards)} kártya találva")

        if not cards:
            # Ha nem találtunk kártyákat, ellenőrizzük, nem vagyunk-e blokkolt
            page_html = page.content()
            if "captcha" in page_html.lower() or "robot" in page_html.lower():
                print("  ⚠ CAPTCHA vagy bot-detektálás! Várok 30 másodpercet...")
                time.sleep(30)
                continue
            break

        for card in cards:
            try:
                listing = extract_card_data(card, label)
                ok, reason = listing_passes_filter(listing)
                listing["passes_filter"] = ok
                listing["filter_reason"] = reason
                results.append(listing)
                if ok:
                    price_m = listing.get("price_ft", 0) / 1e6
                    print(f"    ✓ {listing.get('address', '?')} – {price_m:.1f}M Ft")
            except Exception as e:
                print(f"    ⚠ Kártya feldolgozási hiba: {e}")

        # Lapozás
        human_delay(1, 3)
        next_btn = page.query_selector(
            "a[rel='next'], [class*='pagination'] a[class*='next'], "
            "[aria-label='Next'], [class*='next-page']"
        )
        if next_btn:
            next_href = next_btn.get_attribute("href")
            if next_href:
                current_url = (
                    "https://ingatlan.com" + next_href
                    if next_href.startswith("/")
                    else next_href
                )
                page_num += 1
                # Emberi szünet lapok között
                human_delay(3, 8)
                continue
        break

    return results


# ── Fő scraper ─────────────────────────────────────────────────────────────────

def run_scraper():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_results: list[dict] = []
    passed_results: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-size=1366,768",
                "--disable-extensions",
                "--disable-dev-shm-usage",
                "--lang=hu-HU,hu",
            ],
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            locale="hu-HU",
            timezone_id="Europe/Budapest",
            extra_http_headers={
                "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "DNT": "1",
            },
        )

        # Stealth mód – elrejti az automatizálás nyomait
        page = context.new_page()
        stealth_sync(page)

        # JavaScript: navigator.webdriver eltüntetése
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['hu-HU', 'hu', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
        """)

        # Először látogassuk meg a főoldalt (természetesebb viselkedés)
        print("→ Főoldal meglátogatása...")
        try:
            page.goto("https://ingatlan.com", wait_until="domcontentloaded", timeout=30_000)
            human_delay(3, 6)
            human_scroll(page, steps=random.randint(2, 4))
            random_mouse_move(page)
            human_delay(2, 4)
        except Exception as e:
            print(f"  ⚠ Főoldal betöltési hiba: {e}")

        # Minden keresési URL feldolgozása
        for search in SEARCH_URLS:
            label = search["label"]
            url   = search["url"]
            print(f"\n{'='*60}")
            print(f"Kerület: {label}")
            print(f"{'='*60}")

            try:
                results = scrape_search_page(page, url, label)
                all_results.extend(results)
                passed = [r for r in results if r.get("passes_filter")]
                passed_results.extend(passed)
                print(f"\n  Összesen: {len(results)} hirdetés, {len(passed)} megfelel a feltételeknek")
            except Exception as e:
                print(f"  ✗ Hiba a(z) {label} keresésénél: {e}")

            # Természetes szünet kerületek között (10–25 mp)
            if search != SEARCH_URLS[-1]:
                wait = random.uniform(10, 25)
                print(f"\n  Várok {wait:.0f} másodpercet a következő kerület előtt...")
                time.sleep(wait)

        browser.close()

    # ── Eredmények mentése ───────────────────────────────────────────────────────
    json_path = OUTPUT_DIR / f"ingatlan_results_{timestamp}.json"
    csv_path  = OUTPUT_DIR / f"ingatlan_results_{timestamp}.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {"scraped_at": timestamp, "total": len(all_results), "passed": len(passed_results), "results": all_results},
            f, ensure_ascii=False, indent=2
        )

    # CSV fejléc
    fieldnames = [
        "passes_filter", "filter_reason", "district", "address",
        "price_ft", "price_text", "area_sqm", "floor", "has_elevator",
        "build_year", "view", "condition", "source_url"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n{'='*60}")
    print(f"KÉSZ!")
    print(f"  Összes hirdetés: {len(all_results)}")
    print(f"  Megfelel a feltételeknek: {len(passed_results)}")
    print(f"  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")
    print(f"{'='*60}")

    # Megfelelt ingatlanok összefoglalója
    if passed_results:
        print("\n✓ MEGFELELŐ INGATLANOK:")
        for r in passed_results:
            price_m = r.get("price_ft", 0) / 1e6
            area    = r.get("area_sqm", "?")
            floor   = r.get("floor", "?")
            year    = r.get("build_year", "?")
            url     = r.get("source_url", "")
            print(
                f"  [{r['district']}] {r.get('address','?')} | "
                f"{price_m:.1f}M Ft | {area}m² | {floor}. em. | {year} | {url}"
            )
    else:
        print("\n⚠ Egyetlen ingatlan sem felelt meg az összes feltételnek.")

    return passed_results


if __name__ == "__main__":
    run_scraper()
