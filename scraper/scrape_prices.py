#!/usr/bin/env python3
"""
Scraper de prix pour whiskies écossais ~10 ans
Sources : La Maison du Whisky, Whisky.de, Master of Malt, Distillerie-online, Idealo
Via Playwright (headless Chromium)
"""

import asyncio
import json
import re
import time
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT = Path(__file__).parent.parent / "data" / "prices_raw.json"
OUTPUT.mkdir(parents=True, exist_ok=True) if not OUTPUT.parent.exists() else None

WHISKIES = [
    # Speyside
    "Glenfiddich 12",
    "Macallan 12 Double Cask",
    "Macallan 12 Sherry Oak",
    "The Glenlivet 12",
    "Aberlour 10",
    "Glenfarclas 10",
    "Balvenie 12 DoubleWood",
    "Craigellachie 13",
    "Speyburn 10",
    "Glen Grant 10",
    "Glen Moray 10",
    "Tamdhu 10",
    "Cragganmore 12",
    "Cardhu 12",
    "Tomintoul 10",
    "Mortlach 12",
    # Highlands
    "Glenmorangie 10",
    "Dalmore 12",
    "Oban 14",
    "Old Pulteney 12",
    "Clynelish 14",
    "GlenDronach 12",
    "Aberfeldy 12",
    "Dalwhinnie 15",
    "Deanston 12",
    "Tomatin 12",
    "Glengoyne 12",
    "Ardmore Traditional Cask",
    "Balblair 2009",
    # Islay
    "Ardbeg 10",
    "Ardbeg Uigeadail",
    "Lagavulin 16",
    "Laphroaig 10",
    "Bowmore 12",
    "Caol Ila 12",
    "Bunnahabhain 12",
    "Bruichladdich Classic Laddie",
    "Port Charlotte 10",
    # Lowlands
    "Auchentoshan 12",
    "Glenkinchie 12",
    "Bladnoch 10",
    # Campbeltown
    "Springbank 10",
    "Springbank 15",
    "Kilkerran 12",
    "Glen Scotia Double Cask",
    # Islands
    "Talisker 10",
    "Highland Park 12",
    "Highland Park 18",
    "Scapa Skiren",
    "Arran 10",
    "Isle of Jura 10",
    "Ledaig 10",
]

SOURCES = {
    "maison_du_whisky": {
        "url": "https://www.whisky.fr/whisky/search?q={query}",
        "name_sel": ".product-item-name, .product-name, h2.name",
        "price_sel": ".price, .product-price, span[data-price-amount]",
    },
    "master_of_malt": {
        "url": "https://www.masterofmalt.com/search/?q={query}",
        "name_sel": ".product-name, h3.name",
        "price_sel": ".price, .productPrice",
    },
    "whisky_de": {
        "url": "https://www.whisky.de/shop/search/?q={query}&lang=fr",
        "name_sel": ".product-name, .articleName",
        "price_sel": ".price, .articlePrice",
    },
}


async def scrape_source(page, whisky: str, source_name: str, source_cfg: dict) -> list:
    results = []
    query = whisky.replace(" ", "+")
    url = source_cfg["url"].format(query=query)
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # Extraire noms + prix
        names = await page.query_selector_all(source_cfg["name_sel"])
        prices = await page.query_selector_all(source_cfg["price_sel"])

        for i, (n, p) in enumerate(zip(names[:5], prices[:5])):
            name_txt = (await n.text_content() or "").strip()
            price_txt = (await p.text_content() or "").strip()
            # Extraire valeur numérique du prix
            price_match = re.search(r"(\d+[.,]\d{2})", price_txt.replace("\u202f", "").replace("\xa0", ""))
            price_val = float(price_match.group(1).replace(",", ".")) if price_match else None

            if name_txt and price_val:
                results.append({
                    "whisky_query": whisky,
                    "product_name": name_txt[:80],
                    "price_eur": price_val,
                    "source": source_name,
                    "url": url,
                })
    except Exception as e:
        print(f"  ⚠ {source_name} / {whisky}: {e}")
    return results


async def scrape_idealo(page, whisky: str) -> list:
    """Scrape Idealo (comparateur) pour avoir plusieurs distributeurs d'un coup"""
    results = []
    query = whisky.replace(" ", "+") + "+whisky"
    url = f"https://www.idealo.fr/cat/20/whiskies.html?q={query}"
    try:
        await page.goto(url, timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        items = await page.query_selector_all(".sr-resultList article, .offerList-item")
        for item in items[:8]:
            try:
                name_el = await item.query_selector("h3, .productName, .offerName")
                price_el = await item.query_selector(".price, .offerPrice")
                shop_el = await item.query_selector(".shop-name, .shopName, .offerShop")

                name_txt = (await name_el.text_content()).strip() if name_el else ""
                price_txt = (await price_el.text_content()).strip() if price_el else ""
                shop_txt = (await shop_el.text_content()).strip() if shop_el else "inconnu"

                price_match = re.search(r"(\d+[.,]\d{2})", price_txt.replace("\u202f", "").replace("\xa0", ""))
                price_val = float(price_match.group(1).replace(",", ".")) if price_match else None

                if name_txt and price_val:
                    results.append({
                        "whisky_query": whisky,
                        "product_name": name_txt[:80],
                        "price_eur": price_val,
                        "source": f"idealo/{shop_txt}",
                        "url": url,
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"  ⚠ idealo / {whisky}: {e}")
    return results


async def main():
    all_results = []
    print(f"🔍 Scraping {len(WHISKIES)} whiskies sur {len(SOURCES)+1} sources...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            locale="fr-FR",
        )
        page = await context.new_page()

        for i, whisky in enumerate(WHISKIES):
            print(f"[{i+1}/{len(WHISKIES)}] {whisky}")

            # Maison du Whisky
            r = await scrape_source(page, whisky, "maison_du_whisky", SOURCES["maison_du_whisky"])
            all_results.extend(r)
            print(f"  → MdW: {len(r)} résultats")

            # Idealo (comparateur multi-shops)
            r2 = await scrape_idealo(page, whisky)
            all_results.extend(r2)
            print(f"  → Idealo: {len(r2)} résultats")

            await asyncio.sleep(1.5)

        await browser.close()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(all_results)} prix collectés → {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
