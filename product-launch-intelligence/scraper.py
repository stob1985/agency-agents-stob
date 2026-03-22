"""
scraper.py — Shopify product page scraper
Extracts title, price, description, and reviews from a Shopify product URL.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

REQUEST_TIMEOUT = 15  # seconds


@dataclass
class ProductData:
    url: str
    title: str = "Unknown"
    price: str = "Unknown"
    description: str = "No description available"
    reviews: list[dict] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    vendor: str = "Unknown"
    tags: list[str] = field(default_factory=list)
    raw_json: Optional[dict] = field(default=None, repr=False)

    def to_prompt_text(self) -> str:
        """Format product data as a readable block for LLM prompts."""
        lines = [
            f"**Product URL:** {self.url}",
            f"**Title:** {self.title}",
            f"**Vendor:** {self.vendor}",
            f"**Price:** {self.price}",
            f"**Tags:** {', '.join(self.tags) if self.tags else 'None'}",
            "",
            "**Description:**",
            self.description,
        ]

        if self.reviews:
            lines += ["", f"**Customer Reviews ({len(self.reviews)} scraped):**"]
            for i, review in enumerate(self.reviews[:10], 1):
                rating = review.get("rating", "N/A")
                body = review.get("body", "").strip()
                author = review.get("author", "Anonymous")
                if body:
                    lines.append(f"{i}. [{rating}/5] {author}: \"{body}\"")
        else:
            lines += ["", "**Customer Reviews:** None found on page"]

        return "\n".join(lines)


def _extract_json_ld(soup: BeautifulSoup) -> Optional[dict]:
    """Try to extract structured product data from JSON-LD script tags."""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") in ("Product", "product"):
                        return item
            elif data.get("@type") in ("Product", "product"):
                return data
        except (json.JSONDecodeError, AttributeError):
            continue
    return None


def _extract_shopify_product_json(url: str, session: requests.Session) -> Optional[dict]:
    """Fetch the Shopify product JSON endpoint (appending .json to product URL)."""
    # Normalize: strip query params, ensure it's a /products/ path
    base = url.split("?")[0].rstrip("/")
    if "/products/" not in base:
        return None
    json_url = base + ".json"
    try:
        resp = session.get(json_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("product")
    except Exception:
        pass
    return None


def _parse_reviews_from_page(soup: BeautifulSoup) -> list[dict]:
    """
    Attempt to extract reviews from common review widget patterns.
    Covers Shopify Product Reviews app, Judge.me, Stamped.io, Loox (basic).
    """
    reviews = []

    # --- Shopify native review app ---
    for review_el in soup.select(".spr-review"):
        body_el = review_el.select_one(".spr-review-content-body")
        rating_el = review_el.select_one(".spr-starrating")
        author_el = review_el.select_one(".spr-review-header-byline strong")
        if body_el:
            rating = 5
            if rating_el:
                # Count filled stars via aria or class
                title = rating_el.get("title", "")
                m = re.search(r"(\d+(\.\d+)?)", title)
                if m:
                    rating = float(m.group(1))
            reviews.append({
                "author": author_el.get_text(strip=True) if author_el else "Anonymous",
                "rating": rating,
                "body": body_el.get_text(strip=True),
            })

    # --- Judge.me widget ---
    for review_el in soup.select(".jdgm-rev"):
        body_el = review_el.select_one(".jdgm-rev__body")
        rating_el = review_el.select_one("[data-score]")
        author_el = review_el.select_one(".jdgm-rev__author")
        if body_el:
            rating = int(rating_el["data-score"]) if rating_el and rating_el.get("data-score") else 5
            reviews.append({
                "author": author_el.get_text(strip=True) if author_el else "Anonymous",
                "rating": rating,
                "body": body_el.get_text(strip=True),
            })

    # --- Generic star rating + review text pattern ---
    if not reviews:
        for review_el in soup.select("[class*='review'], [class*='Review']"):
            body_candidates = review_el.select(
                "[class*='body'], [class*='content'], [class*='text'], p"
            )
            for bc in body_candidates:
                text = bc.get_text(strip=True)
                if len(text) > 20:
                    reviews.append({"author": "Customer", "rating": 5, "body": text})
                    break

    return reviews[:20]  # cap at 20 reviews


def scrape_product(url: str) -> ProductData:
    """
    Scrape a Shopify product page and return a ProductData object.

    Strategy:
    1. Try the Shopify product JSON API endpoint for structured data.
    2. Fall back to HTML scraping with JSON-LD and BeautifulSoup selectors.
    3. Always attempt to scrape reviews from the HTML.
    """
    session = requests.Session()
    product = ProductData(url=url)

    # ── Step 1: Shopify JSON API ──────────────────────────────────────────────
    shopify_data = _extract_shopify_product_json(url, session)
    if shopify_data:
        product.raw_json = shopify_data
        product.title = shopify_data.get("title", "Unknown")
        product.vendor = shopify_data.get("vendor", "Unknown")
        product.tags = shopify_data.get("tags", [])

        # Price from first variant
        variants = shopify_data.get("variants", [])
        if variants:
            price_val = variants[0].get("price", "")
            compare_at = variants[0].get("compare_at_price")
            product.price = f"${price_val}"
            if compare_at and compare_at != price_val:
                product.price += f" (was ${compare_at})"

        # Description: strip HTML tags from body_html
        body_html = shopify_data.get("body_html", "")
        if body_html:
            desc_soup = BeautifulSoup(body_html, "html.parser")
            product.description = desc_soup.get_text(separator="\n", strip=True)

        # Images
        product.images = [
            img["src"] for img in shopify_data.get("images", []) if img.get("src")
        ][:5]

    # ── Step 2: HTML scraping (always run for reviews + fallback data) ────────
    try:
        resp = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        if product.title == "Unknown":
            raise RuntimeError(f"Failed to fetch page: {e}") from e
        # We have JSON data; just skip HTML parsing
        return product

    # Fallback: JSON-LD
    if product.title == "Unknown":
        ld = _extract_json_ld(soup)
        if ld:
            product.title = ld.get("name", "Unknown")
            product.vendor = ld.get("brand", {}).get("name", "Unknown") if isinstance(ld.get("brand"), dict) else "Unknown"
            offers = ld.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0] if offers else {}
            product.price = f"${offers.get('price', 'Unknown')}" if offers.get("price") else "Unknown"
            if product.description == "No description available":
                product.description = ld.get("description", "No description available")

    # Fallback: HTML selectors for title
    if product.title == "Unknown":
        for selector in [
            "h1.product__title",
            "h1.product-title",
            "h1[class*='product']",
            ".product-single__title",
            "h1",
        ]:
            el = soup.select_one(selector)
            if el:
                product.title = el.get_text(strip=True)
                break

    # Fallback: HTML selectors for price
    if product.price == "Unknown":
        for selector in [
            "[class*='price'] [class*='current']",
            ".price__regular .price-item",
            ".product__price",
            "[class*='product-price']",
            "[class*='price']:not([class*='compare'])",
        ]:
            el = soup.select_one(selector)
            if el:
                text = el.get_text(strip=True)
                if text and any(c.isdigit() for c in text):
                    product.price = text
                    break

    # Fallback: description from meta description
    if product.description == "No description available":
        meta = soup.find("meta", {"name": "description"}) or soup.find("meta", {"property": "og:description"})
        if meta and meta.get("content"):
            product.description = meta["content"]

    # Reviews (always attempt from HTML)
    product.reviews = _parse_reviews_from_page(soup)

    return product
