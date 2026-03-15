#!/usr/bin/env python3
"""
Ingatlan.com Budapest scraper – Selenium + Chrome (emberi viselkedés utánzása)
Kerületek: I, II, XI (Sasad & Bartók Béla), XII
Feltételek: felújítandó/befejezetlen, ≤120M Ft, ≤1.4M Ft/m², stb.
"""

import json
import csv
import time
import random
import re
import os
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from bs4 import BeautifulSoup

# ── Útvonalak ──────────────────────────────────────────────────────────────────
CHROME_BIN        = "/tmp/chrome-linux64/chrome"
CHROMEDRIVER_PATH = "/tmp/145.0.7632.46/chromedriver/chromedriver-linux64/chromedriver"

# ── Keresési URL-ek ─────────────────────────────────────────────────────────
SEARCH_URLS = [
    {"label": "I. kerület",   "url": "https://ingatlan.com/i-ker/elado+lakas?allapot=felujitando"},
    {"label": "II. kerület",  "url": "https://ingatlan.com/ii-ker/elado+lakas?allapot=felujitando"},
    {"label": "XI. kerület",  "url": "https://ingatlan.com/xi-ker/elado+lakas?allapot=felujitando"},
    {"label": "XII. kerület", "url": "https://ingatlan.com/xii-ker/elado+lakas?allapot=felujitando"},
]

# ── Szűrési feltételek ──────────────────────────────────────────────────────
MAX_PRICE_FT        = 120_000_000
MAX_PRICE_PER_SQM   = 1_400_000
MIN_FLOOR           = 1
ELEVATOR_FROM_FLOOR = 2
BUILD_YEAR_OLD_MAX  = 1950
BUILD_YEAR_NEW_MIN  = 1980
ALLOWED_VIEWS       = {"utcai", "kertre néző", "kertkapcsolatos", "panorámás", "panoráma"}
ALLOWED_CONDITIONS  = {"felújítandó", "befejezetlen"}
XI_AREAS            = ["sasad", "bartók béla"]

OUTPUT_DIR = Path(__file__).parent / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Segédeszközök ───────────────────────────────────────────────────────────

def human_delay(min_s=0.8, max_s=2.5):
    t = random.uniform(min_s, max_s)
    if random.random() < 0.1:
        t *= random.uniform(2, 3.5)
    time.sleep(t)


def human_scroll(driver, steps=5):
    for _ in range(steps):
        amt = random.randint(250, 700)
        driver.execute_script(f"window.scrollBy(0, {amt});")
        time.sleep(random.uniform(0.3, 0.9))


def random_mouse(driver):
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        w = driver.execute_script("return window.innerWidth")
        h = driver.execute_script("return window.innerHeight")
        x = random.randint(100, max(101, w - 100))
        y = random.randint(100, max(101, h - 100))
        ActionChains(driver).move_to_element_with_offset(body, x // 2, y // 2).perform()
        time.sleep(random.uniform(0.1, 0.4))
    except Exception:
        pass


def parse_price(text: str) -> int | None:
    t = text.replace("\xa0", " ").replace(" ", "")
    m = re.search(r"(\d+\.?\d*)\s*millió", t, re.IGNORECASE)
    if m:
        try:
            return int(float(m.group(1).replace(",", ".")) * 1_000_000)
        except ValueError:
            pass
    digits = re.sub(r"[^\d]", "", t)
    if digits:
        v = int(digits)
        if v > 1_000_000:
            return v
        if v > 100:
            return v * 1_000_000
    return None


def parse_sqm(text: str) -> float | None:
    m = re.search(r"([\d\s,\.]+)\s*m[²2]", text, re.IGNORECASE)
    if m:
        raw = m.group(1).replace(" ", "").replace(",", ".")
        try:
            v = float(raw)
            if 5 < v < 1000:
                return v
        except ValueError:
            pass
    return None


def parse_floor(text: str) -> int | None:
    t = text.lower()
    if "földszint" in t:
        return 0
    m = re.search(r"(\d+)\.\s*emelet", t)
    if m:
        return int(m.group(1))
    m2 = re.search(r"\d+\s*/\s*(\d+)", t)
    if m2:
        return int(m2.group(1))
    return None


def parse_year(text: str) -> int | None:
    for yr in re.findall(r"\b(1[89]\d{2}|20[0-2]\d)\b", text):
        y = int(yr)
        if 1800 < y <= 2030:
            return y
    return None


# ── Szűrő ───────────────────────────────────────────────────────────────────

def passes_filter(r: dict) -> tuple[bool, str]:
    district = r.get("district", "")
    address  = r.get("address", "").lower()

    if "xi" in district.lower():
        if not any(a in address for a in XI_AREAS):
            return False, f"XI. ker. de nem Sasad/Bartók: {address}"

    price = r.get("price_ft")
    if price is None:
        return False, "Nincs ár"
    if price > MAX_PRICE_FT:
        return False, f"Túl drága: {price/1e6:.1f}M Ft"

    sqm = r.get("area_sqm")
    if sqm and sqm > 0 and price / sqm > MAX_PRICE_PER_SQM:
        return False, f"Nm ár: {price/sqm/1e6:.2f}M Ft/m²"

    floor = r.get("floor")
    if floor is not None:
        if floor < MIN_FLOOR:
            return False, f"Alacsony emelet: {floor}"
        if floor >= ELEVATOR_FROM_FLOOR and not r.get("has_elevator"):
            return False, f"{floor}. em., nincs lift"

    year = r.get("build_year")
    if year and not (year < BUILD_YEAR_OLD_MAX or year > BUILD_YEAR_NEW_MIN):
        return False, f"Épület kora: {year}"

    view = r.get("view", "").lower()
    if view and not any(v in view for v in ALLOWED_VIEWS):
        return False, f"Kilátás: {view}"

    cond = r.get("condition", "").lower()
    if cond and not any(c in cond for c in ALLOWED_CONDITIONS):
        return False, f"Állapot: {cond}"

    return True, ""


# ── Kártya adatkinyerés ─────────────────────────────────────────────────────

def extract_from_soup(soup: BeautifulSoup, district_label: str) -> list[dict]:
    results = []

    # Hirdetéskártyák megkeresése
    selectors = [
        "div.listing-card",
        "article.listing",
        "div[class*='listing-card']",
        "div[class*='ListingCard']",
        "[data-testid*='listing']",
        "li.listing",
        "div.property-listing",
        "[class*='property-card']",
    ]
    cards = []
    for sel in selectors:
        found = soup.select(sel)
        if found:
            cards = found
            print(f"    Kártya selector: {sel} → {len(found)} db")
            break

    if not cards:
        # Fallback: ingatlan URL-ek alapján
        cards = soup.select("a[href*='/elado-lakas/'], a[href*='/ingatlan/']")
        print(f"    Fallback: {len(cards)} link találat")

    print(f"    Összesen {len(cards)} kártya")

    for card in cards:
        r: dict = {"district": district_label}
        text = card.get_text(" ", strip=True)

        # URL
        link = card.find("a", href=True)
        if link is None and card.name == "a":
            link = card
        if link:
            href = link.get("href", "")
            r["source_url"] = "https://ingatlan.com" + href if href.startswith("/") else href

        # Cím
        for sel in ["[class*='address']", "[class*='Address']", "[class*='title']", "h3", "h2"]:
            el = card.select_one(sel)
            if el:
                r["address"] = el.get_text(strip=True)
                break
        r.setdefault("address", "")

        # Ár
        for sel in ["[class*='price']", "[class*='Price']", "[class*='ar']", "strong"]:
            el = card.select_one(sel)
            if el:
                pt = el.get_text(strip=True)
                p = parse_price(pt)
                if p and p > 1_000_000:
                    r["price_ft"] = p
                    r["price_text"] = pt
                    break
        if "price_ft" not in r:
            m = re.search(r"[\d\s]+(?:millió\s*Ft|M\s*Ft)", text, re.IGNORECASE)
            if m:
                p = parse_price(m.group(0))
                if p:
                    r["price_ft"] = p

        # Terület
        sqm = parse_sqm(text)
        if sqm:
            r["area_sqm"] = sqm

        # Emelet
        fl = parse_floor(text)
        if fl is not None:
            r["floor"] = fl

        # Lift
        r["has_elevator"] = bool(re.search(r"lift(es|tel)?\b", text, re.IGNORECASE))

        # Építési év
        yr = parse_year(text)
        if yr:
            r["build_year"] = yr

        # Kilátás
        for v in ALLOWED_VIEWS:
            if v in text.lower():
                r["view"] = v
                break

        # Állapot
        for c in ALLOWED_CONDITIONS:
            if c in text.lower():
                r["condition"] = c
                break

        r["raw_text"] = text[:400]
        results.append(r)

    return results


# ── Böngésző indítás ────────────────────────────────────────────────────────

def make_driver() -> webdriver.Chrome:
    opts = Options()
    opts.binary_location = CHROME_BIN
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument("--lang=hu-HU")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-software-rasterizer")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/145.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    svc = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=svc, options=opts)

    # Anti-detection JS
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['hu-HU','hu','en-US','en'] });
            window.chrome = { runtime: {} };
        """
    })
    return driver


# ── Egy keresési URL végigpörgetése ─────────────────────────────────────────

def scrape_url(driver, url: str, label: str) -> list[dict]:
    all_results = []
    current_url = url
    page_num = 1
    max_pages = 15

    while current_url and page_num <= max_pages:
        print(f"\n  [{label}] Oldal #{page_num}: {current_url}")
        try:
            driver.get(current_url)
        except WebDriverException as e:
            print(f"  ✗ Betöltési hiba: {e}")
            break

        human_delay(2, 4)
        random_mouse(driver)
        human_scroll(driver, steps=random.randint(3, 6))
        human_delay(1, 2)

        # Cookie banner kezelés
        for sel in [
            "button[id*='reject']", "button[id*='decline']",
            "[class*='cookie'] button", "button[data-testid*='reject']",
            "#CybotCookiebotDialogBodyButtonDecline",
        ]:
            try:
                btns = driver.find_elements(By.CSS_SELECTOR, sel)
                for btn in btns:
                    if btn.is_displayed():
                        btn.click()
                        human_delay(0.5, 1.2)
                        break
            except Exception:
                pass

        # CAPTCHA ellenőrzés
        page_src = driver.page_source
        if "captcha" in page_src.lower() or "robot" in page_src.lower():
            print("  ⚠ CAPTCHA! Várok 60s...")
            time.sleep(60)
            page_src = driver.page_source

        soup = BeautifulSoup(page_src, "lxml")
        listings = extract_from_soup(soup, label)

        if not listings:
            print("  → Nincs több hirdetés / oldalvége.")
            # Debug: mentsük el az oldalt
            debug_path = OUTPUT_DIR / f"debug_{label.replace(' ','_')}_p{page_num}.html"
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(page_src[:50000])
            print(f"  → Debug HTML mentve: {debug_path}")
            break

        for r in listings:
            ok, reason = passes_filter(r)
            r["passes_filter"] = ok
            r["filter_reason"] = reason
            all_results.append(r)
            if ok:
                pft = r.get("price_ft", 0)
                print(f"    ✓ {r.get('address','?')} | {pft/1e6:.1f}M Ft | {r.get('area_sqm','?')}m² | {r.get('source_url','')}")

        # Lapozás
        human_delay(2, 5)
        next_href = None

        # 1. rel=next link keresés
        try:
            nxt = driver.find_element(By.CSS_SELECTOR, "a[rel='next']")
            next_href = nxt.get_attribute("href")
        except NoSuchElementException:
            pass

        # 2. Lapozó gomb szöveg alapján
        if not next_href:
            for sel in ["[class*='pagination'] a", "[class*='Pagination'] a"]:
                try:
                    for a in driver.find_elements(By.CSS_SELECTOR, sel):
                        txt = a.text.strip().lower()
                        if txt in ("következő", "next", "»", ">") or "next" in (a.get_attribute("aria-label") or "").lower():
                            next_href = a.get_attribute("href")
                            break
                    if next_href:
                        break
                except Exception:
                    pass

        if next_href and next_href != current_url:
            current_url = next_href
            page_num += 1
            human_delay(3, 8)
        else:
            break

    return all_results


# ── Fő belépési pont ─────────────────────────────────────────────────────────

def run_scraper():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    all_results: list[dict] = []

    print("→ Chrome indítása...")
    driver = make_driver()

    try:
        # Főoldal meglátogatása (természetesebb belépés)
        print("→ Főoldal meglátogatása...")
        driver.get("https://ingatlan.com")
        human_delay(3, 6)
        human_scroll(driver, steps=random.randint(2, 4))
        random_mouse(driver)
        human_delay(2, 4)

        for i, entry in enumerate(SEARCH_URLS):
            label = entry["label"]
            url   = entry["url"]
            print(f"\n{'='*60}")
            print(f"  {label}")
            print(f"{'='*60}")

            results = scrape_url(driver, url, label)
            all_results.extend(results)

            passed = [r for r in results if r.get("passes_filter")]
            print(f"\n  Összesítés: {len(results)} hirdetés, {len(passed)} megfelel")

            if i < len(SEARCH_URLS) - 1:
                wait = random.uniform(12, 28)
                print(f"\n  Szünet {wait:.0f}s...")
                time.sleep(wait)

    finally:
        driver.quit()

    # ── Mentés ──────────────────────────────────────────────────────────────
    passed_results = [r for r in all_results if r.get("passes_filter")]

    json_path = OUTPUT_DIR / f"ingatlan_{timestamp}.json"
    csv_path  = OUTPUT_DIR / f"ingatlan_{timestamp}.csv"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "scraped_at": timestamp,
            "total": len(all_results),
            "passed": len(passed_results),
            "criteria": {
                "max_price_ft": MAX_PRICE_FT,
                "max_price_per_sqm": MAX_PRICE_PER_SQM,
                "min_floor": MIN_FLOOR,
                "elevator_from_floor": ELEVATOR_FROM_FLOOR,
                "build_year": f"<{BUILD_YEAR_OLD_MAX} or >{BUILD_YEAR_NEW_MIN}",
            },
            "results": all_results,
        }, f, ensure_ascii=False, indent=2)

    fields = [
        "passes_filter", "filter_reason", "district", "address",
        "price_ft", "price_text", "area_sqm", "floor", "has_elevator",
        "build_year", "view", "condition", "source_url", "raw_text"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(all_results)

    print(f"\n{'='*60}")
    print(f"KÉSZ!")
    print(f"  Összes hirdetés : {len(all_results)}")
    print(f"  Megfelel         : {len(passed_results)}")
    print(f"  JSON : {json_path}")
    print(f"  CSV  : {csv_path}")
    print(f"{'='*60}")

    if passed_results:
        print("\n✓ MEGFELELŐ INGATLANOK:")
        for r in passed_results:
            pft  = r.get("price_ft", 0)
            sqm  = r.get("area_sqm")
            fl   = r.get("floor", "?")
            yr   = r.get("build_year", "?")
            url  = r.get("source_url", "")
            nm   = f" | {pft/sqm/1e6:.2f}M Ft/m²" if sqm else ""
            print(f"  [{r['district']}] {r.get('address','?')} | {pft/1e6:.1f}M Ft{nm} | {sqm}m² | {fl}. em. | {yr} | {url}")
    else:
        print("\n⚠ Nincs találat a feltételek alapján.")
        print("   Nézd meg a debug HTML fájlokat és a JSON raw_text mezőit.")

    return passed_results


if __name__ == "__main__":
    run_scraper()
