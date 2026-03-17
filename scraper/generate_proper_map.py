#!/usr/bin/env python3
"""
Carte des distilleries avec le vrai contour de l'Écosse (Natural Earth 10m)
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np
from pathlib import Path as FPath

GEO_FILE  = FPath(__file__).parent.parent / "data/geo/scotland_exact.geojson"
MAPS_DIR  = FPath(__file__).parent.parent / "maps"
MAPS_DIR.mkdir(exist_ok=True)

REGION_COLORS = {
    "Speyside":    "#F4A800",
    "Highlands":   "#3A7D44",
    "Islay":       "#1E3A8A",
    "Lowlands":    "#E07B39",
    "Campbeltown": "#8B2500",
    "Islands":     "#7B3FAB",
}

# (nom, lat, lon, région, prix)
DISTILLERIES = [
    ("Glenfiddich",     57.445, -3.128, "Speyside",    "~34€"),
    ("The Macallan",    57.480, -3.200, "Speyside",    "~55€"),
    ("The Glenlivet",   57.307, -3.352, "Speyside",    "~33€"),
    ("Aberlour",        57.463, -3.228, "Speyside",    "~38€"),
    ("Balvenie",        57.447, -3.131, "Speyside",    "~55€"),
    ("Glenfarclas",     57.427, -3.179, "Speyside",    "~40€"),
    ("Cragganmore",     57.417, -3.310, "Speyside",    "~48€"),
    ("Cardhu",          57.407, -3.338, "Speyside",    "~39€"),
    ("Speyburn",        57.620, -3.369, "Speyside",    "~27€"),
    ("Glen Grant",      57.618, -3.343, "Speyside",    "~30€"),
    ("Glen Moray",      57.646, -3.353, "Speyside",    "~27€"),
    ("Tamdhu",          57.413, -3.290, "Speyside",    "~44€"),
    ("Mortlach",        57.442, -3.130, "Speyside",    "~62€"),
    ("Tomintoul",       57.245, -3.375, "Speyside",    "~33€"),
    ("Strathisla",      57.484, -2.900, "Speyside",    "~45€"),
    ("Glenmorangie",    57.834, -4.049, "Highlands",   "~36€"),
    ("Dalmore",         57.675, -4.176, "Highlands",   "~49€"),
    ("Oban",            56.415, -5.471, "Highlands",   "~62€"),
    ("Old Pulteney",    58.434, -3.092, "Highlands",   "~38€"),
    ("Clynelish",       57.998, -3.920, "Highlands",   "~52€"),
    ("GlenDronach",     57.385, -2.688, "Highlands",   "~52€"),
    ("Aberfeldy",       56.624, -3.863, "Highlands",   "~44€"),
    ("Dalwhinnie",      56.939, -4.243, "Highlands",   "~53€"),
    ("Deanston",        56.178, -4.054, "Highlands",   "~39€"),
    ("Tomatin",         57.337, -4.002, "Highlands",   "~35€"),
    ("Glengoyne",       56.027, -4.305, "Highlands",   "~47€"),
    ("Balblair",        57.793, -4.187, "Highlands",   "~55€"),
    ("Glencadam",       56.663, -2.726, "Highlands",   "~37€"),
    ("Ardmore",         57.312, -2.669, "Highlands",   "~31€"),
    ("Royal Lochnagar", 57.040, -3.100, "Highlands",   "~55€"),
    ("Wolfburn",        58.590, -3.520, "Highlands",   "~45€"),
    ("Ardbeg",          55.640, -6.100, "Islay",       "~48€"),
    ("Lagavulin",       55.636, -6.125, "Islay",       "~73€"),
    ("Laphroaig",       55.637, -6.153, "Islay",       "~42€"),
    ("Bowmore",         55.757, -6.289, "Islay",       "~43€"),
    ("Caol Ila",        55.840, -6.079, "Islay",       "~47€"),
    ("Bunnahabhain",    55.882, -6.120, "Islay",       "~48€"),
    ("Bruichladdich",   55.762, -6.361, "Islay",       "~44€"),
    ("Port Charlotte",  55.737, -6.390, "Islay",       "~52€"),
    ("Kilchoman",       55.793, -6.449, "Islay",       "~45€"),
    ("Auchentoshan",    55.920, -4.440, "Lowlands",    "~38€"),
    ("Glenkinchie",     55.879, -2.961, "Lowlands",    "~43€"),
    ("Bladnoch",        54.828, -4.430, "Lowlands",    "~44€"),
    ("Lindores Abbey",  56.360, -3.196, "Lowlands",    "~55€"),
    ("Springbank",      55.426, -5.604, "Campbeltown", "~58€"),
    ("Glen Scotia",     55.425, -5.605, "Campbeltown", "~41€"),
    ("Glengyle",        55.427, -5.603, "Campbeltown", "~52€"),
    ("Talisker",        57.298, -6.350, "Islands",     "~45€"),
    ("Highland Park",   58.962, -2.971, "Islands",     "~44€"),
    ("Scapa",           58.961, -3.001, "Islands",     "~43€"),
    ("Tobermory",       56.622, -6.062, "Islands",     "~45€"),
    ("Arran",           55.590, -5.202, "Islands",     "~40€"),
    ("Isle of Jura",    55.836, -5.817, "Islands",     "~37€"),
    ("Torabhaig",       57.185, -5.718, "Islands",     "~50€"),
]


def load_scotland_geojson():
    with open(GEO_FILE) as f:
        return json.load(f)


def geojson_to_patches(geojson, color, alpha=0.85):
    patches = []
    for feature in geojson["features"]:
        geom = feature["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]

        for poly in polys:
            for ring in poly:
                coords = np.array(ring)
                if len(coords) < 3:
                    continue
                # lon → x, lat → y
                xs, ys = coords[:, 0], coords[:, 1]
                verts = list(zip(xs, ys)) + [(xs[0], ys[0])]
                codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
                path = Path(verts, codes)
                patch = PathPatch(path, facecolor=color, edgecolor="#4A5240",
                                  linewidth=0.4, alpha=alpha, zorder=2)
                patches.append(patch)
    return patches


def generate_map():
    geojson = load_scotland_geojson()

    fig, ax = plt.subplots(figsize=(14, 20))
    fig.patch.set_facecolor("#C8E8FF")
    ax.set_facecolor("#C8E8FF")

    # --- Contour officiel de l'Écosse ---
    for patch in geojson_to_patches(geojson, color="#2D5016", alpha=0.90):
        ax.add_patch(patch)

    # --- Zones régions (couleurs légères par-dessus) ---
    region_boxes = [
        # (x0, y0, w, h, region)
        (-3.55, 57.15, 0.90, 0.55, "Speyside"),
        (-5.60, 55.30, 0.18, 0.20, "Campbeltown"),
        (-5.00, 54.60, 3.20, 1.30, "Lowlands"),
    ]
    for x0, y0, w, h, region in region_boxes:
        rect = plt.Rectangle((x0, y0), w, h, color=REGION_COLORS[region],
                              alpha=0.15, zorder=3, linewidth=0)
        ax.add_patch(rect)

    # --- Points distilleries ---
    label_positions = {}
    for name, lat, lon, region, prix in DISTILLERIES:
        color = REGION_COLORS[region]
        ax.scatter(lon, lat, c=color, s=60, zorder=6,
                   edgecolors="white", linewidth=1.0)

        # Offset pour les labels (éviter superpositions)
        key = (round(lon, 1), round(lat, 1))
        offset_x = 0.08
        offset_y = 0.05
        if key in label_positions:
            offset_y += label_positions[key] * 0.14
        label_positions[key] = label_positions.get(key, 0) + 1

        ax.annotate(
            f"{name}\n{prix}",
            xy=(lon, lat),
            xytext=(lon + offset_x, lat + offset_y),
            fontsize=5.5,
            color="#111",
            zorder=7,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.80, ec="none"),
            arrowprops=dict(arrowstyle="-", color="#666", lw=0.5) if offset_y > 0.06 else None,
        )

    # --- Étiquettes régions ---
    region_text = [
        (-3.15, 57.38, "SPEYSIDE",    "Speyside"),
        (-4.20, 57.60, "HIGHLANDS",   "Highlands"),
        (-6.20, 55.75, "ISLAY",       "Islay"),
        (-3.80, 55.55, "LOWLANDS",    "Lowlands"),
        (-5.65, 55.20, "CAMPBELTOWN", "Campbeltown"),
        (-5.80, 56.90, "ISLANDS",     "Islands"),
    ]
    for tx, ty, label, region in region_text:
        ax.text(tx, ty, label, fontsize=9, fontweight="bold",
                color=REGION_COLORS[region], alpha=0.85,
                ha="center", zorder=8,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.5, ec="none"))

    # --- Légende ---
    legend_patches = [
        mpatches.Patch(color=c, label=f"{r}  ({sum(1 for d in DISTILLERIES if d[3]==r)} distilleries)")
        for r, c in REGION_COLORS.items()
    ]
    ax.legend(handles=legend_patches, loc="lower left", fontsize=9,
              title="Régions", title_fontsize=10,
              framealpha=0.95, edgecolor="#bbb", fancybox=True)

    # --- Cadre et titre ---
    ax.set_xlim(-7.8, -0.6)
    ax.set_ylim(54.4, 60.9)
    ax.set_aspect("equal")
    ax.set_xlabel("Longitude", fontsize=9, color="#555")
    ax.set_ylabel("Latitude", fontsize=9, color="#555")
    ax.tick_params(colors="#777", labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#aaa")

    ax.set_title(
        "Carte des Distilleries de Whisky en Écosse\nSingle Malts ~10 ans · 54 distilleries · 6 régions",
        fontsize=15, fontweight="bold", pad=20, color="#1a1a1a"
    )

    # Compass rose
    ax.annotate("N", xy=(-0.85, 60.3), fontsize=13, fontweight="bold",
                color="#333", ha="center", zorder=9)
    ax.annotate("", xy=(-0.85, 60.5), xytext=(-0.85, 60.1),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))

    fig.tight_layout(pad=1.5)
    out = MAPS_DIR / "scotland_distilleries_map.png"
    fig.savefig(out, bbox_inches="tight", dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    size_kb = out.stat().st_size // 1024
    print(f"  ✓ {out.name} ({size_kb} KB)")
    return out


if __name__ == "__main__":
    print("Génération de la carte (contour officiel Natural Earth)...\n")
    out = generate_map()
    print(f"\nCarte sauvegardée : {out}")
