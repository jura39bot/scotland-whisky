#!/usr/bin/env python3
"""
Scrape les vrais URLs produits sur whisky.fr et idealo.fr
"""
import asyncio, json, re
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT = Path(__file__).parent.parent / "data" / "real_urls.json"

WHISKIES = [
    "Glenfiddich 12", "The Glenlivet 12", "Macallan 12 Double Cask",
    "Macallan 12 Sherry Oak", "Aberlour 10", "Balvenie 12 DoubleWood",
    "Glenfarclas 10", "Glenfarclas 12", "Cardhu 12", "Speyburn 10",
    "Glen Grant 10", "Glen Moray 10", "Tamdhu 10", "Tomintoul 10",
    "Mortlach 12", "Craigellachie 13", "BenRiach 10",
    "Glenmorangie 10", "Glenmorangie 12 Lasanta", "Dalmore 12",
    "Oban 14", "Old Pulteney 12", "Clynelish 14", "GlenDronach 12",
    "Aberfeldy 12", "Dalwhinnie 15", "Deanston 12", "Tomatin 12",
    "Glengoyne 12", "Ardmore Traditional Cask", "Glencadam 10",
    "Ardbeg 10", "Ardbeg Uigeadail", "Lagavulin 16", "Laphroaig 10",
    "Bowmore 12", "Caol Ila 12", "Bunnahabhain 12",
    "Bruichladdich Classic Laddie", "Port Charlotte 10",
    "Auchentoshan 12", "Glenkinchie 12", "Bladnoch 10",
    "Springbank 10", "Springbank 15", "Kilkerran 12",
    "Glen Scotia Double Cask", "Longrow 14",
    "Talisker 10", "Talisker Storm", "Highland Park 12", "Highland Park 18",
    "Scapa Skiren", "Arran 10", "Isle of Jura 10", "Ledaig 10",
]

async def get_mdw_url(page, whisky):
    q = whisky.replace(" ", "+")
    try:
        await page.goto(f"https://www.whisky.fr/whisky/search?q={q}", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        # Premier résultat
        link = await page.query_selector("a.product-item-link, .product-item h2 a, .products-grid .item a, a[class*='product']")
        if link:
            href = await link.get_attribute("href")
            name_el = await page.query_selector(".product-item-name, h2.product-name")
            name = (await name_el.text_content()).strip()[:60] if name_el else whisky
            price_el = await page.query_selector(".price-container .price, .special-price .price, .regular-price .price")
            price_txt = (await price_el.text_content()).strip() if price_el else ""
            m = re.search(r"(\d+)[,.](\d{2})", price_txt.replace("\u202f","").replace("\xa0",""))
            price = float(f"{m.group(1)}.{m.group(2)}") if m else None
            url = href if href and href.startswith("http") else f"https://www.whisky.fr{href}" if href else None
            return {"name": name, "price": price, "url": url}
    except Exception as e:
        print(f"    MdW err [{whisky}]: {e}")
    return None

async def get_idealo_url(page, whisky):
    q = whisky.replace(" ", "+") + "+whisky+single+malt"
    try:
        await page.goto(f"https://www.idealo.fr/cat/20/whiskies.html?q={q}", timeout=15000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        # Premier résultat
        link = await page.query_selector("a.offerList-item-titleLink, .sr-resultList article a, h2 a, .productTile a")
        if link:
            href = await link.get_attribute("href")
            price_el = await page.query_selector(".price, .offerList-item-priceMin, .productTile-price")
            price_txt = (await price_el.text_content()).strip() if price_el else ""
            m = re.search(r"(\d+)[,.](\d{2})", price_txt.replace("\u202f","").replace("\xa0",""))
            price = float(f"{m.group(1)}.{m.group(2)}") if m else None
            url = href if href and href.startswith("http") else f"https://www.idealo.fr{href}" if href else None
            return {"price": price, "url": url}
    except Exception as e:
        print(f"    Idealo err [{whisky}]: {e}")
    return None

async def main():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
            locale="fr-FR"
        )
        page = await ctx.new_page()
        await page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")

        for i, w in enumerate(WHISKIES):
            print(f"[{i+1}/{len(WHISKIES)}] {w}")
            mdw = await get_mdw_url(page, w)
            idealo = await get_idealo_url(page, w)
            results[w] = {"mdw": mdw, "idealo": idealo}
            if mdw: print(f"  MdW: {mdw.get('price')}€ → {mdw.get('url','')[:60]}")
            if idealo: print(f"  Idealo: {idealo.get('price')}€ → {idealo.get('url','')[:60]}")
            await asyncio.sleep(1.5)

        await browser.close()

    OUTPUT.parent.mkdir(exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(results)} whiskies → {OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
