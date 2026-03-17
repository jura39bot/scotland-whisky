#!/usr/bin/env python3
"""
Génère LIENS.md avec liens directs vers chaque whisky sur tous les sites
"""
from pathlib import Path
import urllib.parse

OUTPUT = Path(__file__).parent.parent / "LIENS.md"

# Tous les whiskies avec prix indicatifs consolidés
WHISKIES = [
    # (nom, region, age, prix_gdist, prix_caviste, prix_online)
    # ── Speyside ────────────────────────────────────────────────────────
    ("Glenfiddich 12",              "Speyside",    12, "29-31€",  "32-35€",  "33-35€"),
    ("The Glenlivet 12",            "Speyside",    12, "28-30€",  "32-34€",  "33-35€"),
    ("Macallan 12 Double Cask",     "Speyside",    12, "49-52€",  "52-55€",  "54-56€"),
    ("Macallan 12 Sherry Oak",      "Speyside",    12, "—",       "65-68€",  "68-70€"),
    ("Aberlour 10",                 "Speyside",    10, "35-37€",  "38-40€",  "37-40€"),
    ("Balvenie 12 DoubleWood",      "Speyside",    12, "—",       "52-56€",  "54-58€"),
    ("Balvenie 12 Caribbean Cask",  "Speyside",    12, "—",       "52-56€",  "54-58€"),
    ("Glenfarclas 10",              "Speyside",    10, "—",       "40-42€",  "38-42€"),
    ("Glenfarclas 12",              "Speyside",    12, "—",       "48-52€",  "48-52€"),
    ("Cragganmore 12",              "Speyside",    12, "—",       "46-50€",  "48-52€"),
    ("Cardhu 12",                   "Speyside",    12, "36-38€",  "38-42€",  "39-42€"),
    ("Knockando 12",                "Speyside",    12, "36-38€",  "38-42€",  "40-44€"),
    ("Speyburn 10",                 "Speyside",    10, "25-27€",  "—",       "27-29€"),
    ("Glen Grant 10",               "Speyside",    10, "28-30€",  "—",       "30-33€"),
    ("Glen Moray 10",               "Speyside",    10, "25-27€",  "—",       "27-30€"),
    ("Tamdhu 10",                   "Speyside",    10, "—",       "44-46€",  "42-46€"),
    ("Tomintoul 10",                "Speyside",    10, "—",       "—",       "32-35€"),
    ("Mortlach 12",                 "Speyside",    12, "—",       "62-65€",  "60-65€"),
    ("Strathisla 12",               "Speyside",    12, "—",       "44-48€",  "44-48€"),
    ("BenRiach 10",                 "Speyside",    10, "—",       "42-45€",  "40-44€"),
    ("Aultmore 12",                 "Speyside",    12, "—",       "44-48€",  "44-48€"),
    ("Craigellachie 13",            "Speyside",    13, "—",       "54-58€",  "52-58€"),
    ("Glenrothes 2012",             "Speyside",    12, "—",       "50-54€",  "48-55€"),
    ("Dailuaine 16",                "Speyside",    16, "—",       "62-68€",  "62-68€"),
    # ── Highlands ───────────────────────────────────────────────────────
    ("Glenmorangie 10 Original",    "Highlands",   10, "32-34€",  "35-38€",  "36-38€"),
    ("Glenmorangie 12 Lasanta",     "Highlands",   12, "—",       "44-48€",  "44-48€"),
    ("Dalmore 12",                  "Highlands",   12, "44-46€",  "46-50€",  "48-52€"),
    ("Dalmore 15",                  "Highlands",   15, "—",       "78-85€",  "78-85€"),
    ("Oban 14",                     "Highlands",   14, "—",       "58-64€",  "60-65€"),
    ("Old Pulteney 12",             "Highlands",   12, "—",       "38-42€",  "36-42€"),
    ("Clynelish 14",                "Highlands",   14, "—",       "52-56€",  "50-55€"),
    ("GlenDronach 10",              "Highlands",   10, "—",       "44-48€",  "42-48€"),
    ("GlenDronach 12",              "Highlands",   12, "—",       "52-56€",  "50-55€"),
    ("Aberfeldy 12",                "Highlands",   12, "—",       "43-48€",  "42-46€"),
    ("Dalwhinnie 15",               "Highlands",   15, "50-52€",  "52-56€",  "52-56€"),
    ("Deanston 12",                 "Highlands",   12, "—",       "38-42€",  "37-41€"),
    ("Tomatin 12",                  "Highlands",   12, "—",       "36-40€",  "34-38€"),
    ("Glengoyne 10",                "Highlands",   10, "—",       "38-42€",  "37-41€"),
    ("Glengoyne 12",                "Highlands",   12, "—",       "48-52€",  "46-50€"),
    ("Balblair 2009",               "Highlands",   10, "—",       "54-58€",  "52-57€"),
    ("Glencadam 10",                "Highlands",   10, "—",       "38-42€",  "36-40€"),
    ("Ardmore Traditional Cask",    "Highlands",   10, "—",       "32-36€",  "30-34€"),
    ("Royal Lochnagar 12",          "Highlands",   12, "—",       "54-58€",  "52-58€"),
    ("Edradour 10",                 "Highlands",   10, "—",       "44-48€",  "43-47€"),
    ("Blair Athol 12",              "Highlands",   12, "—",       "48-52€",  "47-52€"),
    ("Glen Ord 12",                 "Highlands",   12, "—",       "44-48€",  "43-47€"),
    # ── Islay ───────────────────────────────────────────────────────────
    ("Ardbeg 10",                   "Islay",       10, "44-46€",  "46-50€",  "48-52€"),
    ("Ardbeg Uigeadail",            "Islay",       12, "—",       "60-65€",  "62-67€"),
    ("Lagavulin 16",                "Islay",       16, "68-72€",  "70-75€",  "73-77€"),
    ("Laphroaig 10",                "Islay",       10, "38-42€",  "42-46€",  "42-46€"),
    ("Laphroaig 10 Cask Strength",  "Islay",       10, "—",       "62-68€",  "60-68€"),
    ("Bowmore 12",                  "Islay",       12, "40-42€",  "42-46€",  "43-46€"),
    ("Caol Ila 12",                 "Islay",       12, "—",       "44-48€",  "46-50€"),
    ("Caol Ila Moch",               "Islay",       10, "—",       "43-47€",  "43-47€"),
    ("Bunnahabhain 12",             "Islay",       12, "—",       "48-52€",  "46-52€"),
    ("Bruichladdich Classic Laddie","Islay",       10, "—",       "40-45€",  "43-47€"),
    ("Port Charlotte 10",           "Islay",       10, "—",       "52-56€",  "50-55€"),
    ("Kilchoman Machir Bay",        "Islay",        8, "—",       "44-48€",  "43-47€"),
    # ── Lowlands ────────────────────────────────────────────────────────
    ("Auchentoshan 12",             "Lowlands",    12, "35-37€",  "36-40€",  "38-42€"),
    ("Auchentoshan American Oak",   "Lowlands",    10, "28-32€",  "32-36€",  "31-35€"),
    ("Glenkinchie 12",              "Lowlands",    12, "—",       "40-44€",  "42-46€"),
    ("Bladnoch 10",                 "Lowlands",    10, "—",       "42-46€",  "42-46€"),
    # ── Campbeltown ─────────────────────────────────────────────────────
    ("Springbank 10",               "Campbeltown", 10, "—",       "58-62€",  "55-60€"),
    ("Springbank 15",               "Campbeltown", 15, "—",       "88-95€",  "85-92€"),
    ("Kilkerran 12",                "Campbeltown", 12, "—",       "52-56€",  "50-55€"),
    ("Glen Scotia Double Cask",     "Campbeltown", 10, "—",       "42-46€",  "40-45€"),
    ("Glen Scotia 15",              "Campbeltown", 15, "—",       "54-58€",  "52-57€"),
    ("Longrow 14",                  "Campbeltown", 14, "—",       "78-85€",  "75-82€"),
    # ── Islands ─────────────────────────────────────────────────────────
    ("Talisker 10",                 "Islands",     10, "40-42€",  "44-48€",  "45-49€"),
    ("Talisker Storm",              "Islands",     10, "38-42€",  "40-45€",  "40-45€"),
    ("Highland Park 12",            "Islands",     12, "40-42€",  "42-46€",  "43-47€"),
    ("Highland Park 18",            "Islands",     18, "—",       "78-85€",  "82-88€"),
    ("Scapa Skiren",                "Islands",     10, "—",       "42-46€",  "42-46€"),
    ("Arran 10",                    "Islands",     10, "—",       "40-44€",  "38-43€"),
    ("Arran 14",                    "Islands",     14, "—",       "54-58€",  "52-57€"),
    ("Isle of Jura 10",             "Islands",     10, "34-36€",  "36-40€",  "37-41€"),
    ("Ledaig 10",                   "Islands",     10, "—",       "42-46€",  "40-45€"),
    ("Tobermory 12",                "Islands",     12, "—",       "44-48€",  "43-48€"),
]

def make_links(name):
    q = urllib.parse.quote_plus(name)
    q_simple = urllib.parse.quote_plus(name.split()[0])  # juste la marque pour GD

    return {
        # Spécialistes whisky
        "mdw":       f"https://www.whisky.fr/whisky/search?q={q}",
        "whiskyshop":f"https://www.thewhiskyshop.com/search?q={q}",
        # Cavistes
        "nicolas":   f"https://www.nicolas.com/recherche?q={q}",
        "lavinia":   f"https://www.laviniagroup.fr/recherche?q={q}",
        # Grande distribution
        "carrefour": f"https://www.carrefour.fr/s?q={q}",
        "leclerc":   f"https://www.e.leclerc/recherche?q={q}",
        "auchan":    f"https://www.auchan.fr/recherche?q={q}",
        # E-commerce généraliste
        "amazon":    f"https://www.amazon.fr/s?k={q}+whisky",
        # Comparateurs
        "idealo":    f"https://www.idealo.fr/cat/20/whiskies.html?q={q}",
    }

def region_emoji(region):
    return {
        "Speyside": "🟡", "Highlands": "🟢", "Islay": "🔵",
        "Lowlands": "🟠", "Campbeltown": "🟤", "Islands": "🟣"
    }.get(region, "⚪")

def generate_md():
    lines = []
    lines.append("# 🔗 Liens directs par whisky — Single Malts Écossais\n")
    lines.append("> Prix indicatifs constatés sur le marché français (mars 2026)  ")
    lines.append("> Cliquer sur un lien pour accéder à la page produit et vérifier le prix en temps réel.\n")
    lines.append("---\n")

    # Tableau récapitulatif
    lines.append("## 📊 Tableau des prix par type de distributeur\n")
    lines.append("| Whisky | Région | Âge | Grande distrib. | Caviste | Spé. online |")
    lines.append("|--------|--------|-----|-----------------|---------|-------------|")
    for name, region, age, gdist, caviste, online in WHISKIES:
        emoji = region_emoji(region)
        lines.append(f"| {name} | {emoji} {region} | {age} ans | {gdist} | {caviste} | {online} |")

    lines.append("\n---\n")

    # Liens par région
    current_region = None
    for name, region, age, gdist, caviste, online in WHISKIES:
        if region != current_region:
            current_region = region
            emoji = region_emoji(region)
            lines.append(f"\n## {emoji} {region}\n")

        links = make_links(name)
        prix_min = gdist if gdist != "—" else caviste

        lines.append(f"### 🥃 {name} ({age} ans)")
        lines.append(f"**Prix minimum constaté :** {prix_min}\n")
        lines.append("| Distributeur | Type | Lien |")
        lines.append("|--------------|------|------|")

        if gdist != "—":
            lines.append(f"| Carrefour | Grande distribution | [Voir prix {gdist}]({links['carrefour']}) |")
            lines.append(f"| E.Leclerc | Grande distribution | [Voir prix {gdist}]({links['leclerc']}) |")
            lines.append(f"| Auchan | Grande distribution | [Voir prix {gdist}]({links['auchan']}) |")

        lines.append(f"| Nicolas | Caviste | [Voir prix {caviste}]({links['nicolas']}) |")
        lines.append(f"| Lavinia | Caviste | [Voir prix {caviste}]({links['lavinia']}) |")
        lines.append(f"| La Maison du Whisky | Spécialiste online | [Voir prix {online}]({links['mdw']}) |")
        lines.append(f"| The Whisky Shop | Spécialiste online | [Voir prix {online}]({links['whiskyshop']}) |")
        lines.append(f"| Amazon.fr | E-commerce | [Comparer sur Amazon]({links['amazon']}) |")
        lines.append(f"| **Idealo** | **Comparateur** | [**Comparer tous les prix**]({links['idealo']}) |")
        lines.append("")

    lines.append("---\n")
    lines.append("## 🛒 Récapitulatif des enseignes\n")
    lines.append("| Enseigne | Type | Avantages | Site |")
    lines.append("|----------|------|-----------|------|")
    lines.append("| **Carrefour** | Grande distribution | Prix bas, dispo en magasin | [carrefour.fr](https://www.carrefour.fr/r/vins-alcools/whisky) |")
    lines.append("| **E.Leclerc** | Grande distribution | Souvent le moins cher | [e.leclerc](https://www.e.leclerc/cat/whisky) |")
    lines.append("| **Auchan** | Grande distribution | Large gamme | [auchan.fr](https://www.auchan.fr/recherche?q=whisky+ecosse) |")
    lines.append("| **Monoprix** | Grande distribution | Villes + livraison | [monoprix.fr](https://www.monoprix.fr/recherche?q=whisky) |")
    lines.append("| **Nicolas** | Caviste | Conseil + 500 magasins | [nicolas.com](https://www.nicolas.com/recherche?q=single+malt+ecosse) |")
    lines.append("| **Lavinia** | Caviste | Large gamme premium | [laviniagroup.fr](https://www.laviniagroup.fr/category/whiskies) |")
    lines.append("| **La Part des Anges** | Caviste | Raretés, Campbeltown | [lapartdesanges.com](https://www.lapartdesanges.com/whisky/) |")
    lines.append("| **La Maison du Whisky** | Spécialiste online | 1200+ références, référence absolue | [whisky.fr](https://www.whisky.fr/whisky/ecosse.html) |")
    lines.append("| **Whisky.fr** | Spécialiste online | Prix compétitifs, notes | [whisky.fr](https://www.whisky.fr) |")
    lines.append("| **The Whisky Shop** | Spécialiste online | UK, très large choix | [thewhiskyshop.com](https://www.thewhiskyshop.com/scotch-whisky) |")
    lines.append("| **Amazon.fr** | E-commerce | Livraison rapide, prix variables | [amazon.fr](https://www.amazon.fr/s?k=single+malt+scotch+whisky) |")
    lines.append("| **Idealo** | Comparateur | Agrège tous les prix en temps réel | [idealo.fr](https://www.idealo.fr/cat/20/whiskies.html) |")
    lines.append("| **Vivino** | App / web | Avis communauté + prix | [vivino.com](https://www.vivino.com/explore?country_code=fr&wine_type_ids=4) |")
    lines.append("\n---\n")
    lines.append("*Liens générés automatiquement — mars 2026*  ")
    lines.append("*Les prix peuvent varier. Toujours vérifier sur le site avant commande.*")

    return "\n".join(lines)


if __name__ == "__main__":
    md = generate_md()
    OUTPUT.write_text(md, encoding="utf-8")
    print(f"✅ {OUTPUT.name} généré — {len(WHISKIES)} whiskies, {len(WHISKIES)*9} liens")
    print(f"   Taille : {OUTPUT.stat().st_size // 1024} KB")
