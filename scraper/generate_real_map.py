#!/usr/bin/env python3
"""
Vraie carte interactive des distilleries écossaises via Folium (OpenStreetMap)
"""
import folium
from folium.plugins import MarkerCluster, MiniMap, Fullscreen
from pathlib import Path

MAPS_DIR = Path(__file__).parent.parent / "maps"
MAPS_DIR.mkdir(exist_ok=True)

REGION_COLORS = {
    "Speyside":    "#F4A800",
    "Highlands":   "#2E8B57",
    "Islay":       "#1E3A8A",
    "Lowlands":    "#E07B39",
    "Campbeltown": "#8B2500",
    "Islands":     "#6A3ACD",
}

REGION_ICONS = {
    "Speyside":    "star",
    "Highlands":   "tree-conifer",
    "Islay":       "tint",
    "Lowlands":    "leaf",
    "Campbeltown": "fire",
    "Islands":     "cloud",
}

# (nom, lat, lon, région, expression_phare, notes, prix_moyen)
DISTILLERIES = [
    # ── Speyside ──────────────────────────────────────────────────────────
    ("Glenfiddich",     57.4450, -3.1280, "Speyside",    "12 ans",           "Poire fraîche, vanille, chêne doux", "~34€"),
    ("The Macallan",    57.4800, -3.2000, "Speyside",    "12 DC / Sherry",   "Caramel, orange confite, fruits secs", "~55-70€"),
    ("The Glenlivet",   57.3070, -3.3520, "Speyside",    "12 ans",           "Ananas, agrumes, miel floral", "~33€"),
    ("Aberlour",        57.4630, -3.2280, "Speyside",    "10 ans",           "Caramel, fruits rouges, épices", "~38€"),
    ("Balvenie",        57.4450, -3.1300, "Speyside",    "12 DoubleWood",    "Miel, vanille, fruits d'été", "~55€"),
    ("Glenfarclas",     57.4270, -3.1790, "Speyside",    "10 ans",           "Sherry, noix, fruits secs", "~40€"),
    ("Cragganmore",     57.4170, -3.3100, "Speyside",    "12 ans",           "Floral, fruits à noyau, herbes", "~48€"),
    ("Cardhu",          57.4070, -3.3380, "Speyside",    "12 ans",           "Miel, bruyère, fruits doux", "~39€"),
    ("Speyburn",        57.6200, -3.3690, "Speyside",    "10 ans",           "Herbes fraîches, pomme, miel léger", "~27€"),
    ("Glen Grant",      57.6180, -3.3430, "Speyside",    "10 ans",           "Floral, pomme verte, noisette", "~30€"),
    ("Glen Moray",      57.6460, -3.3530, "Speyside",    "10 ans",           "Vanille, caramel, céréales", "~27€"),
    ("Tamdhu",          57.4130, -3.2900, "Speyside",    "10 ans",           "Fruits rouges, épices, chocolat au lait", "~44€"),
    ("Mortlach",        57.4400, -3.1280, "Speyside",    "12 ans",           "Viande, cuir, fruits secs, sherry", "~62€"),
    ("Tomintoul",       57.2450, -3.3750, "Speyside",    "10 ans",           "Doux, miel, fruits blancs", "~33€"),
    ("Knockando",       57.4130, -3.2980, "Speyside",    "12 ans",           "Floral, herbes, poire, douceur", "~40€"),
    ("Strathisla",      57.4840, -2.9000, "Speyside",    "12 ans",           "Fruits, miel, légèrement épicé", "~45€"),
    ("BenRiach",        57.4330, -3.1410, "Speyside",    "10 ans",           "Fruits à noyau, miel, orge malté", "~42€"),
    ("Glenrothes",      57.6180, -3.3430, "Speyside",    "Vintage 2012",     "Fruits tropicaux, vanille, brioche", "~50€"),
    ("Craigellachie",   57.4550, -3.2300, "Speyside",    "13 ans",           "Pomme cuite, agrumes, poivre", "~55€"),
    ("Aultmore",        57.4990, -2.8600, "Speyside",    "12 ans",           "Pêche, ananas, brioche, miel", "~45€"),
    ("Dufftown",        57.4400, -3.1280, "Speyside",    "12 ans",           "Malt sucré, poire, herbacé", "~45€"),
    # ── Highlands ─────────────────────────────────────────────────────────
    ("Glenmorangie",    57.8340, -4.0490, "Highlands",   "10 ans Original",  "Pêche, fleurs, vanille, miel", "~36€"),
    ("Dalmore",         57.6750, -4.1760, "Highlands",   "12 ans",           "Orange confite, chocolat, cannelle", "~49€"),
    ("Oban",            56.4150, -5.4710, "Highlands",   "14 ans",           "Maritime, sel, tourbe légère, miel", "~62€"),
    ("Old Pulteney",    58.4340, -3.0920, "Highlands",   "12 ans",           "Sel, iodé léger, miel, orange", "~38€"),
    ("Clynelish",       57.9980, -3.9200, "Highlands",   "14 ans",           "Cire d'abeille, agrumes, épices", "~52€"),
    ("GlenDronach",     57.3850, -2.6880, "Highlands",   "12 ans",           "Sherry, raisins, épices, orange", "~52€"),
    ("Aberfeldy",       56.6240, -3.8630, "Highlands",   "12 ans",           "Miel, bruyère, orange douce", "~44€"),
    ("Dalwhinnie",      56.9390, -4.2430, "Highlands",   "15 ans",           "Miel doux, lavande, bruyère", "~53€"),
    ("Deanston",        56.1780, -4.0540, "Highlands",   "12 ans",           "Miel, caramel, noix, orge", "~39€"),
    ("Tomatin",         57.3370, -4.0020, "Highlands",   "12 ans",           "Fruité, légèrement toasté, vanille", "~35€"),
    ("Glengoyne",       56.0270, -4.3050, "Highlands",   "12 ans",           "Pomme fraîche, herbes, malt doux", "~47€"),
    ("Balblair",        57.7930, -4.1870, "Highlands",   "2009 (~10 ans)",   "Fruits à noyau, agrumes, vanille", "~55€"),
    ("Glencadam",       56.6630, -2.7260, "Highlands",   "10 ans",           "Pêche, brioche, floral, doux", "~37€"),
    ("Ardmore",         57.3120, -2.6690, "Highlands",   "Traditional Cask", "Tourbé, fumé, fruits noirs", "~31€"),
    ("Royal Lochnagar", 57.0400, -3.1000, "Highlands",   "12 ans",           "Fruits rouges, épices, chêne", "~55€"),
    ("Blair Athol",     56.7100, -3.8400, "Highlands",   "12 ans",           "Fruits rouges, épices, miel", "~50€"),
    ("Edradour",        56.7300, -3.7900, "Highlands",   "10 ans",           "Crème, vanille, sherry léger", "~45€"),
    ("Wolfburn",        58.5900, -3.5200, "Highlands",   "Morven",           "Fruits doux, céréales, légère tourbe", "~45€"),
    ("Glen Ord",        57.5000, -4.4200, "Highlands",   "12 ans",           "Malt riche, toffee, fruits secs", "~45€"),
    # ── Islay ─────────────────────────────────────────────────────────────
    ("Ardbeg",          55.6400, -6.1000, "Islay",       "10 ans",           "Phénolique intense, fumée, citron, anis", "~48€"),
    ("Lagavulin",       55.6360, -6.1250, "Islay",       "16 ans",           "Tourbe profonde, sherry, fruits secs", "~73€"),
    ("Laphroaig",       55.6370, -6.1530, "Islay",       "10 ans",           "Tourbe médicinale, iode, sel, vanille", "~42€"),
    ("Bowmore",         55.7570, -6.2890, "Islay",       "12 ans",           "Tourbe équilibrée, fleurs, chocolat", "~43€"),
    ("Caol Ila",        55.8400, -6.0790, "Islay",       "12 ans",           "Fumée douce, agrumes, sel", "~47€"),
    ("Bunnahabhain",    55.8820, -6.1200, "Islay",       "12 ans",           "Peu tourbé ! Noix, fruits secs, sel", "~48€"),
    ("Bruichladdich",   55.7620, -6.3610, "Islay",       "Classic Laddie",   "Non tourbé. Agrumes, herbes, sel marin", "~44€"),
    ("Port Charlotte",  55.7370, -6.3900, "Islay",       "10 ans",           "Très tourbé. Fumée, iodé, fruits noirs", "~52€"),
    ("Kilchoman",       55.7930, -6.4490, "Islay",       "Machir Bay",       "Farm distillery. Tourbe, citron, vanille", "~45€"),
    ("Ardnahoe",        55.8900, -6.0800, "Islay",       "NAS",              "Île d'Islay, nouvelle distillerie (2019)", "~55€"),
    # ── Lowlands ──────────────────────────────────────────────────────────
    ("Auchentoshan",    55.9200, -4.4400, "Lowlands",    "12 ans",           "Triple distillé. Floral, citron, très doux", "~38€"),
    ("Glenkinchie",     55.8790, -2.9610, "Lowlands",    "12 ans",           "Floral, herbes, légèrement sucré", "~43€"),
    ("Bladnoch",        54.8280, -4.4300, "Lowlands",    "10 ans",           "Fruité, floral, légèrement épicé", "~44€"),
    ("Lindores Abbey",  56.3600, -3.1960, "Lowlands",    "MCDXCIV",          "Historique (1494). Malt doux, fruits", "~55€"),
    ("Annandale",       55.0700, -3.2600, "Lowlands",    "Man O' Words",     "Non tourbé. Fruits, malt, céréales", "~60€"),
    ("Daftmill",        56.2700, -3.1700, "Lowlands",    "Summer Batch",     "Fruits à noyau, herbes, très élégant", "~120€"),
    # ── Campbeltown ───────────────────────────────────────────────────────
    ("Springbank",      55.4260, -5.6040, "Campbeltown", "10 / 15 ans",      "Sel, tourbe légère, fruits exotiques, cire", "~58-90€"),
    ("Glen Scotia",     55.4250, -5.6040, "Campbeltown", "Double Cask",      "Maritime, sel, tourbe légère, vanille", "~41€"),
    ("Glengyle",        55.4270, -5.6040, "Campbeltown", "Kilkerran 12",     "Tourbe légère, fruits, épices, sel", "~52€"),
    # ── Islands ───────────────────────────────────────────────────────────
    ("Talisker",        57.2980, -6.3500, "Islands",     "10 ans",           "Poivre noir, tourbe, sel marin, fruits rouges", "~45€"),
    ("Highland Park",   58.9620, -2.9710, "Islands",     "12 / 18 ans",      "Tourbe douce, miel de bruyère, fumée douce", "~44-83€"),
    ("Scapa",           58.9610, -3.0000, "Islands",     "Skiren",           "Non tourbé. Miel, orange, sel léger", "~43€"),
    ("Tobermory",       56.6220, -6.0620, "Islands",     "12 ans",           "Non tourbé. Fruité, poivre, herbes marines", "~45€"),
    ("Ledaig",          56.6220, -6.0620, "Islands",     "10 ans",           "Tourbé (Tobermory). Fumée, algues, fruits noirs", "~43€"),
    ("Arran",           55.5900, -5.2020, "Islands",     "10 ans",           "Fruits tropicaux, vanille, miel", "~40€"),
    ("Isle of Jura",    55.8360, -5.8170, "Islands",     "10 ans",           "Léger, floral, légèrement tourbé, miel", "~37€"),
    ("Torabhaig",       57.1850, -5.7180, "Islands",     "Allt Gleann",      "Tourbé, fruits, malt doux, fumée légère", "~50€"),
]


def generate_interactive_map():
    # Centrage sur l'Écosse
    m = folium.Map(
        location=[57.0, -4.5],
        zoom_start=7,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    # Couche satellite optionnelle
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        overlay=False,
        control=True,
    ).add_to(m)

    # Plugins
    Fullscreen().add_to(m)
    MiniMap(toggle_display=True).add_to(m)

    # Groupes par région
    region_groups = {}
    for region in REGION_COLORS:
        fg = folium.FeatureGroup(name=f"<span style='color:{REGION_COLORS[region]}'><b>{region}</b></span>")
        region_groups[region] = fg
        fg.add_to(m)

    for name, lat, lon, region, expression, notes, prix in DISTILLERIES:
        color = REGION_COLORS[region]

        popup_html = f"""
        <div style='font-family: Arial, sans-serif; min-width:220px; max-width:280px;'>
          <h3 style='color:{color}; margin:0 0 6px 0; border-bottom:2px solid {color}; padding-bottom:4px;'>
            🥃 {name}
          </h3>
          <table style='width:100%; font-size:12px;'>
            <tr><td><b>Région</b></td><td>{region}</td></tr>
            <tr><td><b>Expression</b></td><td>{expression}</td></tr>
            <tr><td><b>Prix ~</b></td><td style='color:#c00; font-weight:bold;'>{prix}</td></tr>
          </table>
          <p style='font-size:11px; color:#555; margin:6px 0 4px 0; font-style:italic;'>
            {notes}
          </p>
          <a href='https://www.whisky.fr/whisky/search?q={name.replace(" ", "+")}' 
             target='_blank' 
             style='font-size:11px; color:#1a73e8;'>
            🔍 Voir prix La Maison du Whisky →
          </a><br/>
          <a href='https://www.idealo.fr/cat/20/whiskies.html?q={name.replace(" ", "+")}+whisky' 
             target='_blank' 
             style='font-size:11px; color:#1a73e8;'>
            💰 Comparer les prix Idealo →
          </a>
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=9,
            color="white",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=folium.Tooltip(
                f"<b>{name}</b><br>{region} — {expression}<br><span style='color:#c00;'>{prix}</span>",
                sticky=True,
            ),
        ).add_to(region_groups[region])

    # Légende
    legend_html = """
    <div style='position: fixed; bottom: 40px; left: 40px; z-index: 1000;
                background: white; padding: 12px 16px; border-radius: 8px;
                border: 1px solid #ccc; box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
                font-family: Arial, sans-serif; font-size: 13px;'>
      <b style='font-size:14px;'>🗺️ Régions</b><br><br>
      <span style='color:#F4A800;'>●</span> Speyside (21 distilleries)<br>
      <span style='color:#2E8B57;'>●</span> Highlands (19 distilleries)<br>
      <span style='color:#1E3A8A;'>●</span> Islay (10 distilleries)<br>
      <span style='color:#E07B39;'>●</span> Lowlands (6 distilleries)<br>
      <span style='color:#8B2500;'>●</span> Campbeltown (3 distilleries)<br>
      <span style='color:#6A3ACD;'>●</span> Islands (8 distilleries)<br>
      <br><small>Cliquer sur un point pour les détails + liens prix</small>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Titre
    title_html = """
    <div style='position: fixed; top: 12px; left: 50%; transform: translateX(-50%);
                z-index: 1000; background: rgba(255,255,255,0.95);
                padding: 8px 20px; border-radius: 8px; border: 1px solid #ddd;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.15); font-family: Arial;'>
      <h3 style='margin:0; font-size:16px; color:#333;'>
        🥃 Carte des Distilleries de Whisky en Écosse — Single Malts ~10 ans
      </h3>
      <p style='margin:2px 0 0; font-size:11px; color:#888; text-align:center;'>
        67 distilleries · 6 régions · Cliquer pour prix et liens
      </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    folium.LayerControl(collapsed=False).add_to(m)

    out = MAPS_DIR / "scotland_distilleries_interactive.html"
    m.save(str(out))
    print(f"  ✓ {out.name} ({out.stat().st_size // 1024} KB)")
    return out


if __name__ == "__main__":
    print("🗺️  Génération de la carte interactive (OpenStreetMap)...\n")
    out = generate_interactive_map()
    print(f"\n✅ Carte interactive générée : {out}")
    print("   Ouvrir dans un navigateur pour voir la vraie carte Écosse")
