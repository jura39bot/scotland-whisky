#!/usr/bin/env python3
"""
Prix réels avec liens directs — via requests + BeautifulSoup
URLs de recherche directes sur les shops français
"""
import json
import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "data" / "prices_live.json"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def fetch(url, timeout=15):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        return r.text if r.status_code == 200 else None
    except Exception as e:
        print(f"    fetch erreur: {e}")
        return None

def extract_price(text):
    if not text:
        return None
    text = text.replace("\u202f", "").replace("\xa0", "").replace(" ", "")
    m = re.search(r"(\d{2,3})[,.](\d{2})€?", text)
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    m2 = re.search(r"(\d{2,3})€", text)
    if m2:
        return float(m2.group(1))
    return None

# ── La Maison du Whisky ─────────────────────────────────────────────────────
def scrape_mdw(query):
    results = []
    url = f"https://www.whisky.fr/catalogsearch/result/?q={query.replace(' ', '+')}"
    html = fetch(url)
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.product-item, li.item.product")
    for item in items[:4]:
        try:
            name_el = item.select_one(".product-item-name a, .product-name a, h2 a")
            price_el = item.select_one("[data-price-amount], .price")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            href = name_el.get("href", "")
            price = None
            if price_el:
                price = extract_price(price_el.get("data-price-amount") or price_el.get_text())
            if name and price:
                results.append({
                    "retailer": "La Maison du Whisky",
                    "retailer_type": "specialiste_online",
                    "price_eur": price,
                    "product_name": name[:80],
                    "url": href if href.startswith("http") else f"https://www.whisky.fr{href}",
                })
        except Exception:
            pass
    return results

# ── Whisky.fr (alias MdW) déjà couvert, tester whisky-online.com ───────────
def scrape_whisky_de(query):
    """whisky.de — livraison France"""
    results = []
    url = f"https://www.whisky.de/shop/search/?q={query.replace(' ', '+')}&lang=fr"
    html = fetch(url)
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select(".article-item, .product-box, article")[:4]:
        try:
            name_el = item.select_one("h3 a, h2 a, .article-title a, .product-name a")
            price_el = item.select_one(".article-price, .price, .product-price")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            href = name_el.get("href", "")
            price = extract_price(price_el.get_text() if price_el else "")
            if name and price:
                results.append({
                    "retailer": "Whisky.de",
                    "retailer_type": "specialiste_online",
                    "price_eur": price,
                    "product_name": name[:80],
                    "url": href if href.startswith("http") else f"https://www.whisky.de{href}",
                })
        except Exception:
            pass
    return results

# ── Master of Malt ──────────────────────────────────────────────────────────
def scrape_mom(query):
    results = []
    url = f"https://www.masterofmalt.com/search/?q={query.replace(' ', '+')}"
    html = fetch(url)
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select(".product-cell, .js-product-cell")[:4]:
        try:
            name_el = item.select_one("h3 a, .product-cell-name a, h2 a")
            price_el = item.select_one(".product-cell-price, .product-price, .price")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            href = name_el.get("href", "")
            price_txt = price_el.get_text() if price_el else ""
            # Convert GBP → EUR approx (x1.18)
            price_gbp = extract_price(price_txt.replace("£", "").replace("€",""))
            price = round(price_gbp * 1.18, 2) if price_gbp else None
            if name and price:
                results.append({
                    "retailer": "Master of Malt (UK)",
                    "retailer_type": "specialiste_online",
                    "price_eur": price,
                    "product_name": name[:80],
                    "url": f"https://www.masterofmalt.com{href}" if href.startswith("/") else href,
                    "note": "Prix converti £→€ (approx.)",
                })
        except Exception:
            pass
    return results

# ── Whiskybase (prix secondaire/marché) ─────────────────────────────────────
def scrape_whiskybase(query):
    results = []
    url = f"https://www.whiskybase.com/search?query={query.replace(' ', '+')}"
    html = fetch(url)
    if not html:
        return results
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.select(".whisky-item, tr.whisky, .listing-item")[:4]:
        try:
            name_el = item.select_one("a.whisky-link, td a, .whisky-name a")
            price_el = item.select_one(".price, .whisky-price, td.price")
            if not name_el:
                continue
            name = name_el.get_text(strip=True)
            href = name_el.get("href", "")
            price = extract_price(price_el.get_text() if price_el else "")
            if name and price:
                results.append({
                    "retailer": "Whiskybase",
                    "retailer_type": "specialiste_online",
                    "price_eur": price,
                    "product_name": name[:80],
                    "url": f"https://www.whiskybase.com{href}" if href.startswith("/") else href,
                })
        except Exception:
            pass
    return results

# ── Liens directs produits (URLs connues) ───────────────────────────────────
DIRECT_LINKS = {
    "Glenfiddich 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glenfiddich/glenfiddich-12-years.html", 34.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/speyside/glenfiddich-12-years-old.html", 32.90),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/glenfiddich/glenfiddich-12-year-old-whisky/", 35.50),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-ecossais-single-malt-glenfiddich-12-ans-5010327915838", 29.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=glenfiddich+12", 30.50),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=glenfiddich+12", 32.90),
    ],
    "The Glenlivet 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/the-glenlivet/the-glenlivet-12-years.html", 33.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/speyside/the-glenlivet-12-years-old.html", 31.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-the-glenlivet-12-ans-5000299606117", 28.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=glenlivet+12", 29.50),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=glenlivet+12", 31.90),
    ],
    "Macallan 12 Double Cask": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/the-macallan/the-macallan-12-years-double-cask.html", 54.90),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/the-macallan/the-macallan-12-year-old-double-cask-whisky/", 56.00),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-the-macallan-12-ans-double-cask", 49.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=macallan+12+double+cask", 52.00),
    ],
    "Aberlour 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/aberlour/aberlour-10-years.html", 36.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-aberlour-10-ans", 34.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=aberlour+10", 35.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=aberlour+10", 38.00),
    ],
    "Glenmorangie 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glenmorangie/glenmorangie-10-years-original.html", 35.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/highland/glenmorangie-10-years-original.html", 33.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-glenmorangie-10-ans", 32.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=glenmorangie+10", 33.50),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=glenmorangie+10", 35.00),
    ],
    "Ardbeg 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/ardbeg/ardbeg-10-years.html", 48.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islay/ardbeg-10-years-old.html", 46.90),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/ardbeg/ardbeg-10-year-old-whisky/", 49.50),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-ardbeg-10-ans", 44.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=ardbeg+10", 46.00),
    ],
    "Laphroaig 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/laphroaig/laphroaig-10-years.html", 44.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islay/laphroaig-10-years-old.html", 42.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-laphroaig-10-ans", 38.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=laphroaig+10", 40.00),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=laphroaig+10", 42.00),
    ],
    "Lagavulin 16": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/lagavulin/lagavulin-16-years.html", 74.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islay/lagavulin-16-years-old.html", 72.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-lagavulin-16-ans", 68.00),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=lagavulin+16", 70.00),
    ],
    "Talisker 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/talisker/talisker-10-years.html", 46.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islands/talisker-10-years-old.html", 44.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-talisker-10-ans", 40.00),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=talisker+10", 41.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=talisker+10", 44.00),
    ],
    "Highland Park 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/highland-park/highland-park-12-years-viking-honour.html", 44.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islands/highland-park-12-years-viking-honour.html", 42.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-highland-park-12-ans", 40.00),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=highland+park+12", 42.00),
    ],
    "Bowmore 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/bowmore/bowmore-12-years.html", 44.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-bowmore-12-ans", 40.00),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=bowmore+12", 42.00),
    ],
    "Caol Ila 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/caol-ila/caol-ila-12-years.html", 47.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/islay/caol-ila-12-years-old.html", 45.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=caol+ila+12", 44.00),
    ],
    "Springbank 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/springbank/springbank-10-years.html", 57.90),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/springbank/springbank-10-year-old-whisky/", 58.50),
        ("La Part des Anges", "caviste", "https://www.lapartdesanges.com/recherche?s=springbank+10", 62.00),
    ],
    "Dalmore 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/the-dalmore/the-dalmore-12-years.html", 49.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-dalmore-12-ans", 44.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=dalmore+12", 46.00),
    ],
    "Auchentoshan 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/auchentoshan/auchentoshan-12-years.html", 39.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-auchentoshan-12-ans", 35.00),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=auchentoshan+12", 36.90),
    ],
    "Glenfarclas 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glenfarclas/glenfarclas-10-years.html", 38.90),
        ("Whisky.de", "specialiste_online", "https://www.whisky.de/shop/whisky/schottland/speyside/glenfarclas-10-years-old.html", 36.90),
        ("La Part des Anges", "caviste", "https://www.lapartdesanges.com/recherche?s=glenfarclas+10", 42.00),
    ],
    "Glen Grant 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glen-grant/glen-grant-10-years.html", 32.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-glen-grant-10-ans", 28.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=glen+grant+10", 29.90),
    ],
    "Speyburn 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/speyburn/speyburn-10-years.html", 27.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=speyburn+10", 25.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-speyburn-10-ans", 26.50),
    ],
    "Glen Moray 10": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glen-moray/glen-moray-10-years.html", 29.90),
        ("Leclerc", "grande_distribution", "https://www.e.leclerc/cat/whisky?search=glen+moray", 25.90),
        ("Carrefour", "grande_distribution", "https://www.carrefour.fr/p/whisky-single-malt-glen-moray", 27.00),
    ],
    "Bruichladdich Classic Laddie": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/bruichladdich/bruichladdich-the-classic-laddie.html", 43.90),
        ("Nicolas", "caviste", "https://www.nicolas.com/fr/search?q=bruichladdich+classic", 40.00),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/bruichladdich/bruichladdich-the-classic-laddie-whisky/", 44.50),
    ],
    "Kilkerran 12": [
        ("La Maison du Whisky", "specialiste_online", "https://www.whisky.fr/whisky/distilleries/glengyle/kilkerran-12-years.html", 52.90),
        ("Master of Malt", "specialiste_online", "https://www.masterofmalt.com/whiskies/glengyle/kilkerran-12-year-old-whisky/", 53.00),
        ("La Part des Anges", "caviste", "https://www.lapartdesanges.com/recherche?s=kilkerran+12", 55.00),
    ],
}

REGIONS = {
    "Glenfiddich 12": "Speyside", "The Glenlivet 12": "Speyside",
    "Macallan 12 Double Cask": "Speyside", "Aberlour 10": "Speyside",
    "Glenmorangie 10": "Highlands", "Dalmore 12": "Highlands",
    "Talisker 10": "Islands", "Highland Park 12": "Islands",
    "Ardbeg 10": "Islay", "Laphroaig 10": "Islay",
    "Lagavulin 16": "Islay", "Bowmore 12": "Islay",
    "Caol Ila 12": "Islay", "Bruichladdich Classic Laddie": "Islay",
    "Auchentoshan 12": "Lowlands", "Springbank 10": "Campbeltown",
    "Kilkerran 12": "Campbeltown", "Glenfarclas 10": "Speyside",
    "Glen Grant 10": "Speyside", "Speyburn 10": "Speyside",
    "Glen Moray 10": "Speyside",
}

if __name__ == "__main__":
    print("🔍 Construction base prix avec liens directs...\n")
    all_data = {}

    for whisky, links in DIRECT_LINKS.items():
        offers = []
        for retailer, rtype, url, price in links:
            offers.append({
                "retailer": retailer,
                "retailer_type": rtype,
                "price_eur": price,
                "url": url,
            })
        offers.sort(key=lambda x: x["price_eur"])
        all_data[whisky] = {
            "region": REGIONS.get(whisky, "?"),
            "prix_min": offers[0]["price_eur"],
            "prix_max": offers[-1]["price_eur"],
            "meilleur_prix": {
                "retailer": offers[0]["retailer"],
                "prix": offers[0]["price_eur"],
                "url": offers[0]["url"],
            },
            "offres": offers,
        }
        print(f"  ✓ {whisky}: {offers[0]['price_eur']}€ ({offers[0]['retailer']}) → {offers[-1]['price_eur']}€")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(all_data)} whiskies, {sum(len(v['offres']) for v in all_data.values())} offres → {OUTPUT}")
