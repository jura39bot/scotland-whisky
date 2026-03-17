#!/usr/bin/env python3
"""
Scrape des prix réels avec liens directs — Playwright headless
Sources : whisky.fr (La Maison du Whisky), nicolas.com, idealo.fr
"""
import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT = Path(__file__).parent.parent / "data" / "prices_live.json"

SEARCHES = [
    # (nom_query, whisky_canonical, region)
    ("Glenfiddich 12 ans single malt", "Glenfiddich 12", "Speyside"),
    ("Glenlivet 12 ans single malt", "The Glenlivet 12", "Speyside"),
    ("Macallan 12 double cask", "Macallan 12 Double Cask", "Speyside"),
    ("Aberlour 10 ans single malt", "Aberlour 10", "Speyside"),
    ("Speyburn 10 ans single malt", "Speyburn 10", "Speyside"),
    ("Glen Grant 10 ans single malt", "Glen Grant 10", "Speyside"),
    ("Glen Moray 10 ans single malt", "Glen Moray 10", "Speyside"),
    ("Cardhu 12 ans single malt", "Cardhu 12", "Speyside"),
    ("Glenmorangie 10 ans original", "Glenmorangie 10", "Highlands"),
    ("Dalmore 12 ans single malt", "Dalmore 12", "Highlands"),
    ("Talisker 10 ans single malt", "Talisker 10", "Islands"),
    ("Highland Park 12 ans", "Highland Park 12", "Islands"),
    ("Ardbeg 10 ans single malt islay", "Ardbeg 10", "Islay"),
    ("Laphroaig 10 ans islay", "Laphroaig 10", "Islay"),
    ("Lagavulin 16 ans islay", "Lagavulin 16", "Islay"),
    ("Bowmore 12 ans islay", "Bowmore 12", "Islay"),
    ("Caol Ila 12 ans islay", "Caol Ila 12", "Islay"),
    ("Auchentoshan 12 ans lowlands", "Auchentoshan 12", "Lowlands"),
    ("Springbank 10 ans campbeltown", "Springbank 10", "Campbeltown"),
]


async def scrape_mdw(page, query: str) -> list:
    """La Maison du Whisky"""
    results = []
    try:
        url = f"https://www.whisky.fr/whisky/search?q={query.replace(' ', '+')}"
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2500)

        items = await page.query_selector_all(".product-item, .item, article.product")
        for item in items[:3]:
            try:
                name_el = await item.query_selector("h2, h3, .product-name, .name")
                price_el = await item.query_selector(".price, .product-price, [data-price-amount]")
                link_el = await item.query_selector("a[href]")

                name = (await name_el.text_content()).strip() if name_el else ""
                price_txt = (await price_el.text_content()).strip() if price_el else ""
                href = await link_el.get_attribute("href") if link_el else ""

                m = re.search(r"(\d+)[,.](\d{2})", price_txt.replace("\u202f", "").replace("\xa0", ""))
                if m and name:
                    price = float(f"{m.group(1)}.{m.group(2)}")
                    link = href if href.startswith("http") else f"https://www.whisky.fr{href}"
                    results.append({
                        "retailer": "La Maison du Whisky",
                        "retailer_type": "specialiste_online",
                        "price_eur": price,
                        "product_name": name[:80],
                        "url": link,
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"    MdW erreur: {e}")
    return results


async def scrape_nicolas(page, query: str) -> list:
    """Nicolas caviste"""
    results = []
    try:
        url = f"https://www.nicolas.com/recherche?q={query.replace(' ', '+')}"
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        items = await page.query_selector_all(".product-card, .product-item, .product")
        for item in items[:3]:
            try:
                name_el = await item.query_selector("h2, h3, .product-name, .title")
                price_el = await item.query_selector(".price, .product-price, .amount")
                link_el = await item.query_selector("a[href]")

                name = (await name_el.text_content()).strip() if name_el else ""
                price_txt = (await price_el.text_content()).strip() if price_el else ""
                href = await link_el.get_attribute("href") if link_el else ""

                m = re.search(r"(\d+)[,.](\d{2})", price_txt.replace("\u202f", "").replace("\xa0", ""))
                if m and name:
                    price = float(f"{m.group(1)}.{m.group(2)}")
                    link = href if href.startswith("http") else f"https://www.nicolas.com{href}"
                    results.append({
                        "retailer": "Nicolas",
                        "retailer_type": "caviste",
                        "price_eur": price,
                        "product_name": name[:80],
                        "url": link,
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"    Nicolas erreur: {e}")
    return results


async def scrape_idealo(page, query: str) -> list:
    """Idealo — comparateur multi-shops"""
    results = []
    try:
        url = f"https://www.idealo.fr/cat/20/whiskies.html?q={query.replace(' ', '+')}"
        await page.goto(url, timeout=20000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        items = await page.query_selector_all("article.offerList-item, .sr-resultList article, .productTile")
        for item in items[:8]:
            try:
                name_el = await item.query_selector("h3, .offerList-item-title, .productTile-title")
                price_el = await item.query_selector(".price, .offerList-item-priceMin, .productTile-price")
                shop_el  = await item.query_selector(".shop-name, .offerList-item-shopName, .productTile-shopName")
                link_el  = await item.query_selector("a[href]")

                name     = (await name_el.text_content()).strip() if name_el else ""
                price_txt = (await price_el.text_content()).strip() if price_el else ""
                shop     = (await shop_el.text_content()).strip() if shop_el else "?"
                href     = await link_el.get_attribute("href") if link_el else ""

                m = re.search(r"(\d+)[,.](\d{2})", price_txt.replace("\u202f","").replace("\xa0",""))
                if m and name:
                    price = float(f"{m.group(1)}.{m.group(2)}")
                    link = href if href.startswith("http") else f"https://www.idealo.fr{href}"

                    # Classifier le type de shop
                    shop_lower = shop.lower()
                    if any(s in shop_lower for s in ["carrefour", "leclerc", "auchan", "casino", "intermarché", "monoprix"]):
                        rtype = "grande_distribution"
                    elif any(s in shop_lower for s in ["nicolas", "lavinia", "anges", "distilleries", "whisky"]):
                        rtype = "caviste"
                    else:
                        rtype = "ecommerce"

                    results.append({
                        "retailer": shop,
                        "retailer_type": rtype,
                        "price_eur": price,
                        "product_name": name[:80],
                        "url": link,
                    })
            except Exception:
                pass
    except Exception as e:
        print(f"    Idealo erreur: {e}")
    return results


async def main():
    all_data = {}
    print(f"🔍 Scraping prix réels pour {len(SEARCHES)} whiskies...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="fr-FR",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()
        # Masquer webdriver
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        for query, canonical, region in SEARCHES:
            print(f"[{canonical}]")
            results = []

            r1 = await scrape_mdw(page, query)
            results.extend(r1)
            print(f"  MdW: {len(r1)} résultat(s)")

            r2 = await scrape_nicolas(page, query)
            results.extend(r2)
            print(f"  Nicolas: {len(r2)} résultat(s)")

            r3 = await scrape_idealo(page, query)
            results.extend(r3)
            print(f"  Idealo: {len(r3)} résultat(s)")

            # Trier par prix
            results.sort(key=lambda x: x["price_eur"])

            if results:
                all_data[canonical] = {
                    "region": region,
                    "prix_min": results[0]["price_eur"],
                    "prix_max": results[-1]["price_eur"],
                    "offres": results,
                }
                print(f"  → {results[0]['price_eur']}€ ({results[0]['retailer']}) → {results[-1]['price_eur']}€")
            else:
                print(f"  → Aucun résultat scraped")

            await asyncio.sleep(2)

        await browser.close()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    total = sum(len(v["offres"]) for v in all_data.values())
    print(f"\n✅ {total} offres scrapées pour {len(all_data)} whiskies → {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
