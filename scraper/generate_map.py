#!/usr/bin/env python3
"""
Carte SVG des distilleries d'Écosse avec coordonnées géographiques
"""
from pathlib import Path

OUT = Path(__file__).parent.parent / "maps" / "scotland_distilleries.svg"
OUT.parent.mkdir(exist_ok=True)

# Coordonnées approximatives (latitude/longitude → transformées en SVG x/y)
# Écosse : lat 55.0–58.7, lon -7.5 à -1.5
# SVG : 600×800px

def geo_to_svg(lat, lon, w=600, h=800):
    """Projection simple : lat/lon → x/y SVG"""
    lon_min, lon_max = -7.6, -1.3
    lat_min, lat_max = 54.8, 58.9
    x = (lon - lon_min) / (lon_max - lon_min) * (w - 80) + 40
    y = (lat_max - lat) / (lat_max - lat_min) * (h - 80) + 40
    return round(x, 1), round(y, 1)


REGION_COLORS = {
    "Speyside":    "#F4C430",
    "Highlands":   "#2E8B57",
    "Islay":       "#1E3A5F",
    "Lowlands":    "#E8A87C",
    "Campbeltown": "#8B4513",
    "Islands":     "#6A5ACD",
}

DISTILLERIES = [
    # Speyside
    ("Glenfiddich",   57.452, -3.137, "Speyside"),
    ("Macallan",      57.481, -3.199, "Speyside"),
    ("The Glenlivet", 57.283, -3.370, "Speyside"),
    ("Aberlour",      57.468, -3.229, "Speyside"),
    ("Balvenie",      57.451, -3.136, "Speyside"),
    ("Glenfarclas",   57.435, -3.227, "Speyside"),
    ("Cragganmore",   57.393, -3.315, "Speyside"),
    ("Cardhu",        57.391, -3.351, "Speyside"),
    ("Speyburn",      57.543, -3.302, "Speyside"),
    ("Glen Grant",    57.538, -3.261, "Speyside"),
    ("Glen Moray",    57.643, -3.319, "Speyside"),
    ("Tamdhu",        57.402, -3.371, "Speyside"),
    ("Mortlach",      57.449, -3.119, "Speyside"),
    ("Craigellachie", 57.466, -3.224, "Speyside"),
    ("Knockando",     57.395, -3.399, "Speyside"),
    ("Strathisla",    57.535, -2.994, "Speyside"),
    ("Tomintoul",     57.249, -3.395, "Speyside"),
    ("BenRiach",      57.647, -3.285, "Speyside"),
    ("Aultmore",      57.565, -2.966, "Speyside"),
    ("Dufftown",      57.449, -3.120, "Speyside"),
    # Highlands - Nord
    ("Old Pulteney",  58.435, -3.094, "Highlands"),
    ("Clynelish",     57.990, -3.943, "Highlands"),
    ("Balblair",      57.810, -4.168, "Highlands"),
    ("Glenmorangie",  57.795, -4.096, "Highlands"),
    ("Dalmore",       57.675, -4.234, "Highlands"),
    ("Glen Ord",      57.516, -4.419, "Highlands"),
    # Highlands - Central
    ("Dalwhinnie",    56.944, -4.249, "Highlands"),
    ("Blair Athol",   56.714, -3.740, "Highlands"),
    ("Edradour",      56.721, -3.736, "Highlands"),
    ("Aberfeldy",     56.624, -3.877, "Highlands"),
    ("Royal Lochnagar",57.060,-3.389, "Highlands"),
    # Highlands - Est
    ("GlenDronach",   57.476, -2.742, "Highlands"),
    ("Glencadam",     56.718, -2.783, "Highlands"),
    # Highlands - Ouest
    ("Oban",          56.415, -5.472, "Highlands"),
    ("Ben Nevis",     56.824, -5.113, "Highlands"),
    ("Ardmore",       57.336, -2.847, "Highlands"),
    # Highlands - Général
    ("Tomatin",       57.324, -4.007, "Highlands"),
    ("Glengoyne",     56.031, -4.251, "Highlands"),
    ("Deanston",      56.185, -4.050, "Highlands"),
    ("Tullibardine",  56.280, -3.730, "Highlands"),
    # Islay
    ("Ardbeg",        55.641, -6.117, "Islay"),
    ("Lagavulin",     55.636, -6.128, "Islay"),
    ("Laphroaig",     55.632, -6.147, "Islay"),
    ("Bowmore",       55.758, -6.284, "Islay"),
    ("Caol Ila",      55.866, -6.091, "Islay"),
    ("Bunnahabhain",  55.897, -6.108, "Islay"),
    ("Bruichladdich", 55.762, -6.362, "Islay"),
    ("Kilchoman",     55.778, -6.452, "Islay"),
    ("Ardnahoe",      55.857, -6.098, "Islay"),
    # Lowlands
    ("Auchentoshan",  55.923, -4.493, "Lowlands"),
    ("Glenkinchie",   55.880, -2.929, "Lowlands"),
    ("Bladnoch",      54.835, -4.420, "Lowlands"),
    ("Lindores Abbey",56.326, -3.261, "Lowlands"),
    ("Annandale",     55.005, -3.266, "Lowlands"),
    ("Daftmill",      56.235, -3.264, "Lowlands"),
    # Campbeltown
    ("Springbank",    55.427, -5.602, "Campbeltown"),
    ("Glengyle",      55.427, -5.603, "Campbeltown"),
    ("Glen Scotia",   55.427, -5.601, "Campbeltown"),
    # Islands
    ("Talisker",      57.296, -6.356, "Islands"),   # Skye
    ("Torabhaig",     57.213, -5.960, "Islands"),   # Skye
    ("Highland Park", 58.970, -2.967, "Islands"),   # Orkney
    ("Scapa",         58.965, -3.004, "Islands"),   # Orkney
    ("Tobermory",     56.624, -6.065, "Islands"),   # Mull
    ("Isle of Jura",  55.868, -5.991, "Islands"),   # Jura
    ("Arran",         55.584, -5.186, "Islands"),   # Arran
    ("Abhainn Dearg", 58.210, -6.905, "Islands"),   # Lewis
]


def generate_svg():
    W, H = 620, 820
    lines = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'  <rect width="{W}" height="{H}" fill="#E8F4F8" rx="12"/>',
        # Fond mer
        f'  <rect x="0" y="0" width="{W}" height="{H}" fill="#B8D4E8" rx="12"/>',
        # Fond terre approximatif (rectangle Écosse)
        f'  <rect x="35" y="35" width="550" height="750" fill="#E8E8D8" rx="8" opacity="0.6"/>',
        # Titre
        f'  <text x="{W//2}" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="#1a1a2e">🗺️ Carte des Distilleries de Scotch Whisky (~10 ans)</text>',
    ]

    # Légende régions
    leg_x, leg_y = 15, 50
    for i, (region, color) in enumerate(REGION_COLORS.items()):
        ly = leg_y + i * 22
        lines.append(f'  <rect x="{leg_x}" y="{ly}" width="12" height="12" fill="{color}" rx="2"/>')
        lines.append(f'  <text x="{leg_x+16}" y="{ly+10}" font-family="sans-serif" font-size="9" fill="#333">{region}</text>')

    # Points distilleries
    for name, lat, lon, region in DISTILLERIES:
        x, y = geo_to_svg(lat, lon, W, H)
        color = REGION_COLORS.get(region, "#888888")
        # Cercle
        lines.append(f'  <circle cx="{x}" cy="{y}" r="5" fill="{color}" stroke="white" stroke-width="1.2" opacity="0.9">')
        lines.append(f'    <title>{name} ({region})</title>')
        lines.append(f'  </circle>')
        # Label (décalé pour lisibilité)
        dx = 7
        lines.append(
            f'  <text x="{x+dx}" y="{y+3}" font-family="sans-serif" font-size="7" fill="#222" '
            f'style="text-shadow: 0px 0px 2px white">{name}</text>'
        )

    # Annotations régions
    annotations = [
        (57.5, -3.2, "SPEYSIDE", "#8B6914"),
        (57.3, -4.3, "HIGHLANDS", "#1a5c35"),
        (55.7, -6.2, "ISLAY", "#0d2440"),
        (56.0, -3.7, "LOWLANDS", "#a0673a"),
        (55.4, -5.6, "CAMPBELTOWN", "#5a2d0c"),
        (57.3, -6.1, "ISLANDS", "#3d2b8a"),
    ]
    for lat, lon, label, color in annotations:
        x, y = geo_to_svg(lat, lon, W, H)
        lines.append(
            f'  <text x="{x}" y="{y}" font-family="sans-serif" font-size="11" font-weight="bold" '
            f'fill="{color}" opacity="0.5" text-anchor="middle">{label}</text>'
        )

    # Source
    lines.append(f'  <text x="{W-5}" y="{H-5}" text-anchor="end" font-family="sans-serif" font-size="7" fill="#666">Données : SWA / WhiskyAdvocate / VisitScotland • 2026</text>')
    lines.append('</svg>')

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Carte SVG → {OUT} ({len(DISTILLERIES)} distilleries)")


if __name__ == "__main__":
    generate_svg()
