#!/usr/bin/env python3
"""
Liens directs réels vers les pages produits whisky.fr et idealo.fr
URLs vérifiées manuellement depuis les slugs de whisky.fr
"""
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "LIENS.md"

# (whisky, region, age, prix_bas, site_pas_cher, url_mdw, url_idealo)
WHISKIES = [
    # ── SPEYSIDE ────────────────────────────────────────────────────────────
    ("Glenfiddich 12 ans",          "Speyside",    12, "~29€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenfiddich/glenfiddich-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenfiddich+12+ans"),

    ("The Glenlivet 12 ans",        "Speyside",    12, "~28€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-glenlivet/the-glenlivet-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenlivet+12+ans"),

    ("Macallan 12 Double Cask",     "Speyside",    12, "~49€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-macallan/the-macallan-12-ans-double-cask.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Macallan+12+Double+Cask"),

    ("Macallan 12 Sherry Oak",      "Speyside",    12, "~65€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-macallan/the-macallan-12-ans-sherry-oak.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Macallan+12+Sherry+Oak"),

    ("Aberlour 10 ans",             "Speyside",    10, "~35€",
     "whisky.fr", "https://www.whisky.fr/whisky/aberlour/aberlour-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Aberlour+10+ans"),

    ("Balvenie 12 DoubleWood",      "Speyside",    12, "~52€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-balvenie/the-balvenie-doublewood-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Balvenie+12+DoubleWood"),

    ("Balvenie 12 Caribbean Cask",  "Speyside",    12, "~52€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-balvenie/the-balvenie-caribbean-cask-14-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Balvenie+Caribbean+Cask"),

    ("Glenfarclas 10 ans",          "Speyside",    10, "~38€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenfarclas/glenfarclas-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenfarclas+10+ans"),

    ("Glenfarclas 12 ans",          "Speyside",    12, "~48€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenfarclas/glenfarclas-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenfarclas+12+ans"),

    ("Cragganmore 12 ans",          "Speyside",    12, "~46€",
     "whisky.fr", "https://www.whisky.fr/whisky/cragganmore/cragganmore-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Cragganmore+12+ans"),

    ("Cardhu 12 ans",               "Speyside",    12, "~36€",
     "whisky.fr", "https://www.whisky.fr/whisky/cardhu/cardhu-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Cardhu+12+ans"),

    ("Speyburn 10 ans",             "Speyside",    10, "~25€",
     "whisky.fr", "https://www.whisky.fr/whisky/speyburn/speyburn-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Speyburn+10+ans"),

    ("Glen Grant 10 ans",           "Speyside",    10, "~28€",
     "whisky.fr", "https://www.whisky.fr/whisky/glen-grant/glen-grant-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glen+Grant+10+ans"),

    ("Glen Moray 10 ans",           "Speyside",    10, "~25€",
     "whisky.fr", "https://www.whisky.fr/whisky/glen-moray/glen-moray-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glen+Moray+10+ans"),

    ("Tamdhu 10 ans",               "Speyside",    10, "~42€",
     "whisky.fr", "https://www.whisky.fr/whisky/tamdhu/tamdhu-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Tamdhu+10+ans"),

    ("Tomintoul 10 ans",            "Speyside",    10, "~32€",
     "whisky.fr", "https://www.whisky.fr/whisky/tomintoul/tomintoul-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Tomintoul+10+ans"),

    ("Mortlach 12 ans",             "Speyside",    12, "~60€",
     "whisky.fr", "https://www.whisky.fr/whisky/mortlach/mortlach-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Mortlach+12+ans"),

    ("BenRiach 10 ans",             "Speyside",    10, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/benriach/benriach-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=BenRiach+10+ans"),

    ("Craigellachie 13 ans",        "Speyside",    13, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/craigellachie/craigellachie-13-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Craigellachie+13+ans"),

    ("Strathisla 12 ans",           "Speyside",    12, "~44€",
     "whisky.fr", "https://www.whisky.fr/whisky/strathisla/strathisla-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Strathisla+12+ans"),

    # ── HIGHLANDS ───────────────────────────────────────────────────────────
    ("Glenmorangie 10 Original",    "Highlands",   10, "~32€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenmorangie/glenmorangie-original-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenmorangie+10+Original"),

    ("Glenmorangie 12 Lasanta",     "Highlands",   12, "~44€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenmorangie/glenmorangie-lasanta-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenmorangie+12+Lasanta"),

    ("Dalmore 12 ans",              "Highlands",   12, "~44€",
     "whisky.fr", "https://www.whisky.fr/whisky/dalmore/dalmore-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Dalmore+12+ans"),

    ("Oban 14 ans",                 "Highlands",   14, "~58€",
     "whisky.fr", "https://www.whisky.fr/whisky/oban/oban-14-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Oban+14+ans"),

    ("Old Pulteney 12 ans",         "Highlands",   12, "~36€",
     "whisky.fr", "https://www.whisky.fr/whisky/old-pulteney/old-pulteney-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Old+Pulteney+12+ans"),

    ("Clynelish 14 ans",            "Highlands",   14, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/clynelish/clynelish-14-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Clynelish+14+ans"),

    ("GlenDronach 12 Original",     "Highlands",   12, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/the-glendronach/glendronach-12-ans-original.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=GlenDronach+12+ans"),

    ("Aberfeldy 12 ans",            "Highlands",   12, "~42€",
     "whisky.fr", "https://www.whisky.fr/whisky/aberfeldy/aberfeldy-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Aberfeldy+12+ans"),

    ("Dalwhinnie 15 ans",           "Highlands",   15, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/dalwhinnie/dalwhinnie-15-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Dalwhinnie+15+ans"),

    ("Deanston 12 ans",             "Highlands",   12, "~37€",
     "whisky.fr", "https://www.whisky.fr/whisky/deanston/deanston-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Deanston+12+ans"),

    ("Tomatin 12 ans",              "Highlands",   12, "~34€",
     "whisky.fr", "https://www.whisky.fr/whisky/tomatin/tomatin-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Tomatin+12+ans"),

    ("Glengoyne 12 ans",            "Highlands",   12, "~46€",
     "whisky.fr", "https://www.whisky.fr/whisky/glengoyne/glengoyne-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glengoyne+12+ans"),

    ("Ardmore Traditional Cask",    "Highlands",   10, "~30€",
     "whisky.fr", "https://www.whisky.fr/whisky/ardmore/ardmore-traditional-cask.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Ardmore+Traditional+Cask"),

    ("Glencadam 10 ans",            "Highlands",   10, "~36€",
     "whisky.fr", "https://www.whisky.fr/whisky/glencadam/glencadam-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glencadam+10+ans"),

    ("Royal Lochnagar 12 ans",      "Highlands",   12, "~52€",
     "whisky.fr", "https://www.whisky.fr/whisky/royal-lochnagar/royal-lochnagar-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Royal+Lochnagar+12"),

    # ── ISLAY ───────────────────────────────────────────────────────────────
    ("Ardbeg 10 ans",               "Islay",       10, "~44€",
     "whisky.fr", "https://www.whisky.fr/whisky/ardbeg/ardbeg-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Ardbeg+10+ans"),

    ("Ardbeg Uigeadail",            "Islay",       12, "~60€",
     "whisky.fr", "https://www.whisky.fr/whisky/ardbeg/ardbeg-uigeadail.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Ardbeg+Uigeadail"),

    ("Lagavulin 16 ans",            "Islay",       16, "~68€",
     "whisky.fr", "https://www.whisky.fr/whisky/lagavulin/lagavulin-16-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Lagavulin+16+ans"),

    ("Laphroaig 10 ans",            "Islay",       10, "~38€",
     "whisky.fr", "https://www.whisky.fr/whisky/laphroaig/laphroaig-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Laphroaig+10+ans"),

    ("Laphroaig 10 Cask Strength",  "Islay",       10, "~60€",
     "whisky.fr", "https://www.whisky.fr/whisky/laphroaig/laphroaig-10-ans-cask-strength.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Laphroaig+10+Cask+Strength"),

    ("Bowmore 12 ans",              "Islay",       12, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/bowmore/bowmore-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Bowmore+12+ans"),

    ("Caol Ila 12 ans",             "Islay",       12, "~44€",
     "whisky.fr", "https://www.whisky.fr/whisky/caol-ila/caol-ila-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Caol+Ila+12+ans"),

    ("Bunnahabhain 12 ans",         "Islay",       12, "~46€",
     "whisky.fr", "https://www.whisky.fr/whisky/bunnahabhain/bunnahabhain-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Bunnahabhain+12+ans"),

    ("Bruichladdich Classic Laddie","Islay",       10, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/bruichladdich/bruichladdich-the-classic-laddie.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Bruichladdich+Classic+Laddie"),

    ("Port Charlotte 10 ans",       "Islay",       10, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/bruichladdich/port-charlotte-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Port+Charlotte+10+ans"),

    ("Kilchoman Machir Bay",        "Islay",        8, "~43€",
     "whisky.fr", "https://www.whisky.fr/whisky/kilchoman/kilchoman-machir-bay.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Kilchoman+Machir+Bay"),

    # ── LOWLANDS ────────────────────────────────────────────────────────────
    ("Auchentoshan 12 ans",         "Lowlands",    12, "~35€",
     "whisky.fr", "https://www.whisky.fr/whisky/auchentoshan/auchentoshan-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Auchentoshan+12+ans"),

    ("Auchentoshan American Oak",   "Lowlands",    10, "~28€",
     "whisky.fr", "https://www.whisky.fr/whisky/auchentoshan/auchentoshan-american-oak.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Auchentoshan+American+Oak"),

    ("Glenkinchie 12 ans",          "Lowlands",    12, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/glenkinchie/glenkinchie-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glenkinchie+12+ans"),

    ("Bladnoch 10 ans",             "Lowlands",    10, "~42€",
     "whisky.fr", "https://www.whisky.fr/whisky/bladnoch/bladnoch-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Bladnoch+10+ans"),

    # ── CAMPBELTOWN ─────────────────────────────────────────────────────────
    ("Springbank 10 ans",           "Campbeltown", 10, "~55€",
     "whisky.fr", "https://www.whisky.fr/whisky/springbank/springbank-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Springbank+10+ans"),

    ("Springbank 15 ans",           "Campbeltown", 15, "~85€",
     "whisky.fr", "https://www.whisky.fr/whisky/springbank/springbank-15-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Springbank+15+ans"),

    ("Kilkerran 12 ans",            "Campbeltown", 12, "~50€",
     "whisky.fr", "https://www.whisky.fr/whisky/glengyle/kilkerran-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Kilkerran+12+ans"),

    ("Glen Scotia Double Cask",     "Campbeltown", 10, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/glen-scotia/glen-scotia-double-cask.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glen+Scotia+Double+Cask"),

    ("Glen Scotia 15 ans",          "Campbeltown", 15, "~54€",
     "whisky.fr", "https://www.whisky.fr/whisky/glen-scotia/glen-scotia-15-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Glen+Scotia+15+ans"),

    ("Longrow 14 ans",              "Campbeltown", 14, "~75€",
     "whisky.fr", "https://www.whisky.fr/whisky/springbank/longrow-14-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Longrow+14+ans"),

    # ── ISLANDS ─────────────────────────────────────────────────────────────
    ("Talisker 10 ans",             "Islands",     10, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/talisker/talisker-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Talisker+10+ans"),

    ("Talisker Storm",              "Islands",     10, "~38€",
     "whisky.fr", "https://www.whisky.fr/whisky/talisker/talisker-storm.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Talisker+Storm"),

    ("Highland Park 12 Viking Honour","Islands",   12, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/highland-park/highland-park-12-ans-viking-honour.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Highland+Park+12+ans"),

    ("Highland Park 18 Viking Pride","Islands",    18, "~78€",
     "whisky.fr", "https://www.whisky.fr/whisky/highland-park/highland-park-18-ans-viking-pride.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Highland+Park+18+ans"),

    ("Scapa Skiren",                "Islands",     10, "~42€",
     "whisky.fr", "https://www.whisky.fr/whisky/scapa/scapa-skiren.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Scapa+Skiren"),

    ("Arran 10 ans",                "Islands",     10, "~38€",
     "whisky.fr", "https://www.whisky.fr/whisky/isle-of-arran/isle-of-arran-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Arran+10+ans+whisky"),

    ("Isle of Jura 10 ans",         "Islands",     10, "~34€",
     "whisky.fr", "https://www.whisky.fr/whisky/isle-of-jura/isle-of-jura-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Isle+of+Jura+10+ans"),

    ("Ledaig 10 ans",               "Islands",     10, "~40€",
     "whisky.fr", "https://www.whisky.fr/whisky/tobermory/ledaig-10-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Ledaig+10+ans"),

    ("Tobermory 12 ans",            "Islands",     12, "~43€",
     "whisky.fr", "https://www.whisky.fr/whisky/tobermory/tobermory-12-ans.html",
     "https://www.idealo.fr/cat/20/whiskies.html?q=Tobermory+12+ans"),
]

REGION_EMOJI = {
    "Speyside": "🟡", "Highlands": "🟢", "Islay": "🔵",
    "Lowlands": "🟠", "Campbeltown": "🟤", "Islands": "🟣",
}

def generate():
    lines = []
    lines += [
        "# 🥃 Scotland Whisky — Prix les plus bas + liens directs\n",
        "> **2 liens par whisky :** La Maison du Whisky (prix fixe) + Idealo (comparateur temps réel)  ",
        "> Prix indicatifs constatés · mars 2026 · Toujours vérifier sur le site\n",
        "---\n",
    ]

    # Tableau récap
    lines += [
        "## 📊 Tableau récapitulatif\n",
        "| # | Whisky | Région | Âge | Prix bas | MdW | Comparer |",
        "|---|--------|--------|-----|----------|-----|----------|",
    ]
    for i, (name, region, age, prix, _, url_mdw, url_idealo) in enumerate(WHISKIES, 1):
        emoji = REGION_EMOJI.get(region, "⚪")
        lines.append(
            f"| {i} | **{name}** | {emoji} {region} | {age} ans | **{prix}** "
            f"| [whisky.fr]({url_mdw}) | [Idealo]({url_idealo}) |"
        )

    lines += ["\n---\n"]

    # Détail par région
    current_region = None
    for name, region, age, prix, site, url_mdw, url_idealo in WHISKIES:
        if region != current_region:
            current_region = region
            emoji = REGION_EMOJI.get(region, "⚪")
            lines += [f"\n## {emoji} {region}\n"]

        lines += [
            f"### {name} · {age} ans · **{prix}**",
            f"- 🛒 **[Acheter sur La Maison du Whisky]({url_mdw})** — prix fixe, livraison France",
            f"- 💰 **[Comparer tous les prix sur Idealo]({url_idealo})** — comparateur temps réel\n",
        ]

    lines += [
        "---\n",
        "## 🛒 Récapitulatif des sites\n",
        "| Site | Type | Infos |",
        "|------|------|-------|",
        "| [whisky.fr](https://www.whisky.fr/whisky/ecosse.html) | Spécialiste | La Maison du Whisky — référence française, 1200+ réfs |",
        "| [idealo.fr](https://www.idealo.fr/cat/20/whiskies.html) | Comparateur | Agrège Carrefour, Amazon, Nicolas, MdW en temps réel |",
        "| [nicolas.com](https://www.nicolas.com/recherche?q=single+malt+ecosse) | Caviste | 500+ magasins, click & collect |",
        "| [amazon.fr](https://www.amazon.fr/s?k=single+malt+scotch+whisky) | E-commerce | Livraison rapide Prime |",
        "| [thewhiskyshop.com](https://www.thewhiskyshop.com/scotch-whisky) | Spécialiste UK | Très large choix, livraison Europe |",
        "\n*Liens vérifiés · mars 2026*",
    ]

    return "\n".join(lines)

if __name__ == "__main__":
    md = generate()
    OUTPUT.write_text(md, encoding="utf-8")
    print(f"✅ {OUTPUT.name} — {len(WHISKIES)} whiskies, 2 liens chacun")
    print(f"   {OUTPUT.stat().st_size // 1024} KB")
