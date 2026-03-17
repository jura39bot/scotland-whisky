#!/usr/bin/env python3
"""
Carte des distilleries écossaises avec matplotlib
(coordonnées GPS réelles)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

MAPS_DIR = Path(__file__).parent.parent / "maps"
MAPS_DIR.mkdir(exist_ok=True)

REGION_COLORS = {
    "Speyside":    "#F4C430",
    "Highlands":   "#2E8B57",
    "Islay":       "#1E3A5F",
    "Lowlands":    "#E8A87C",
    "Campbeltown": "#8B4513",
    "Islands":     "#6A5ACD",
}

# (nom, lon, lat, region)
DISTILLERIES = [
    # Speyside
    ("Glenfiddich",   -3.128, 57.445, "Speyside"),
    ("The Macallan",  -3.200, 57.480, "Speyside"),
    ("The Glenlivet", -3.352, 57.307, "Speyside"),
    ("Aberlour",      -3.228, 57.463, "Speyside"),
    ("Balvenie",      -3.128, 57.445, "Speyside"),
    ("Glenfarclas",   -3.179, 57.427, "Speyside"),
    ("Cragganmore",   -3.310, 57.417, "Speyside"),
    ("Cardhu",        -3.338, 57.407, "Speyside"),
    ("Speyburn",      -3.369, 57.620, "Speyside"),
    ("Glen Grant",    -3.343, 57.618, "Speyside"),
    ("Glen Moray",    -3.353, 57.646, "Speyside"),
    ("Tamdhu",        -3.290, 57.413, "Speyside"),
    ("Mortlach",      -3.128, 57.440, "Speyside"),
    ("Tomintoul",     -3.375, 57.245, "Speyside"),
    ("Knockando",     -3.298, 57.413, "Speyside"),
    ("Strathisla",    -2.900, 57.484, "Speyside"),
    ("Aultmore",      -2.860, 57.499, "Speyside"),
    ("BenRiach",      -3.141, 57.433, "Speyside"),
    ("Dufftown",      -3.128, 57.440, "Speyside"),
    ("Glenrothes",    -3.343, 57.618, "Speyside"),
    ("Craigellachie", -3.230, 57.455, "Speyside"),
    # Highlands
    ("Glenmorangie",  -4.049, 57.834, "Highlands"),
    ("Dalmore",       -4.176, 57.675, "Highlands"),
    ("Oban",          -5.471, 56.415, "Highlands"),
    ("Old Pulteney",  -3.092, 58.434, "Highlands"),
    ("Clynelish",     -3.920, 57.998, "Highlands"),
    ("GlenDronach",   -2.688, 57.385, "Highlands"),
    ("Aberfeldy",     -3.863, 56.624, "Highlands"),
    ("Dalwhinnie",    -4.243, 56.939, "Highlands"),
    ("Deanston",      -4.054, 56.178, "Highlands"),
    ("Tomatin",       -4.002, 57.337, "Highlands"),
    ("Glengoyne",     -4.305, 56.027, "Highlands"),
    ("Balblair",      -4.187, 57.793, "Highlands"),
    ("Glencadam",     -2.726, 56.663, "Highlands"),
    ("Ardmore",       -2.669, 57.312, "Highlands"),
    ("Royal Lochnagar",-3.100, 57.040, "Highlands"),
    # Islay
    ("Ardbeg",        -6.100, 55.640, "Islay"),
    ("Lagavulin",     -6.125, 55.636, "Islay"),
    ("Laphroaig",     -6.153, 55.637, "Islay"),
    ("Bowmore",       -6.289, 55.757, "Islay"),
    ("Caol Ila",      -6.079, 55.840, "Islay"),
    ("Bunnahabhain",  -6.120, 55.882, "Islay"),
    ("Bruichladdich", -6.361, 55.762, "Islay"),
    ("Port Charlotte", -6.390, 55.737, "Islay"),
    ("Kilchoman",     -6.449, 55.793, "Islay"),
    # Lowlands
    ("Auchentoshan",  -4.440, 55.920, "Lowlands"),
    ("Glenkinchie",   -2.961, 55.879, "Lowlands"),
    ("Bladnoch",      -4.430, 54.828, "Lowlands"),
    ("Lindores Abbey",-3.196, 56.360, "Lowlands"),
    # Campbeltown
    ("Springbank",    -5.604, 55.426, "Campbeltown"),
    ("Glen Scotia",   -5.604, 55.425, "Campbeltown"),
    ("Glengyle",      -5.604, 55.427, "Campbeltown"),
    # Islands
    ("Talisker",      -6.350, 57.298, "Islands"),   # Skye
    ("Highland Park", -2.971, 58.962, "Islands"),   # Orkney
    ("Scapa",         -3.000, 58.961, "Islands"),   # Orkney
    ("Tobermory",     -6.062, 56.622, "Islands"),   # Mull
    ("Arran",         -5.202, 55.590, "Islands"),   # Arran
    ("Isle of Jura",  -5.817, 55.836, "Islands"),   # Jura
    ("Torabhaig",     -5.718, 57.185, "Islands"),   # Skye
]

def draw_scotland_outline(ax):
    """Contour simplifié de l'Écosse (polygone approximatif)"""
    # Mainland Scotland outline (simplifié)
    scotland_x = [-5.0, -4.5, -3.2, -2.0, -1.8, -2.5, -3.5, -4.0, -5.5, -6.0, -5.8, -5.0]
    scotland_y = [54.6, 55.0, 55.5, 55.9, 56.5, 57.2, 57.7, 58.2, 58.6, 58.0, 57.0, 54.6]
    ax.fill(scotland_x, scotland_y, color="#E8F4E8", zorder=0, alpha=0.6)
    ax.plot(scotland_x + [scotland_x[0]], scotland_y + [scotland_y[0]],
            color="#999", linewidth=0.8, zorder=1)

    # Islay
    islay_x = [-6.5, -6.0, -5.9, -6.3, -6.5]
    islay_y = [55.65, 55.60, 55.85, 55.92, 55.65]
    ax.fill(islay_x, islay_y, color="#D0E8FF", zorder=0, alpha=0.7)
    ax.plot(islay_x, islay_y, color="#999", linewidth=0.6)

    # Skye
    skye_x = [-6.7, -6.1, -5.8, -6.1, -6.7]
    skye_y = [57.1, 57.0, 57.4, 57.7, 57.1]
    ax.fill(skye_x, skye_y, color="#D0E8FF", zorder=0, alpha=0.7)
    ax.plot(skye_x, skye_y, color="#999", linewidth=0.6)

    # Arran
    ax.fill([-5.35, -5.1, -5.0, -5.25, -5.35],
            [55.48, 55.50, 55.75, 55.72, 55.48], color="#D0E8FF", alpha=0.7, zorder=0)

    # Jura
    ax.fill([-5.95, -5.65, -5.60, -5.95],
            [55.70, 55.70, 56.00, 56.00], color="#D0E8FF", alpha=0.7, zorder=0)

    # Orkney (simplifié)
    ax.fill([-3.4, -2.8, -2.8, -3.4],
            [58.80, 58.80, 59.10, 59.10], color="#D0E8FF", alpha=0.7, zorder=0)

    # Mull
    ax.fill([-6.3, -5.8, -5.8, -6.3],
            [56.45, 56.45, 56.70, 56.70], color="#D0E8FF", alpha=0.7, zorder=0)


def generate_map():
    fig, ax = plt.subplots(figsize=(14, 18))
    ax.set_facecolor("#C8E8FF")  # mer
    fig.patch.set_facecolor("#F8F8F8")

    draw_scotland_outline(ax)

    # Régions colorées (zones approximatives)
    region_zones = {
        "Speyside":    ((-3.5, -2.7, 57.2, 57.6), 0.08),
        "Highlands":   ((-5.5, -2.5, 56.0, 58.5), 0.04),
        "Lowlands":    ((-5.0, -2.0, 54.5, 56.0), 0.06),
    }
    for region, ((x0, x1, y0, y1), alpha) in region_zones.items():
        rect = plt.Rectangle((x0, y0), x1-x0, y1-y0,
                              color=REGION_COLORS[region], alpha=alpha, zorder=1)
        ax.add_patch(rect)

    # Plot distilleries
    plotted_labels = []
    for name, lon, lat, region in DISTILLERIES:
        color = REGION_COLORS[region]
        ax.scatter(lon, lat, c=color, s=55, zorder=5, edgecolors="white", linewidth=0.8)

        # Éviter les labels qui se chevauchent
        offset_x, offset_y = 0.05, 0.04
        too_close = any(abs(lon - px) < 0.25 and abs(lat - py) < 0.18
                        for px, py in plotted_labels)
        if not too_close:
            ax.annotate(name, (lon, lat), xytext=(lon + offset_x, lat + offset_y),
                        fontsize=6.5, color="#222",
                        bbox=dict(boxstyle="round,pad=0.15", fc="white", alpha=0.7, ec="none"),
                        zorder=6)
            plotted_labels.append((lon, lat))

    # Légende
    legend_patches = [mpatches.Patch(color=c, label=r) for r, c in REGION_COLORS.items()]
    ax.legend(handles=legend_patches, loc="lower left", fontsize=10,
              title="Régions", title_fontsize=11, framealpha=0.95,
              edgecolor="#ccc")

    ax.set_xlim(-7.2, -0.8)
    ax.set_ylim(54.4, 59.4)
    ax.set_xlabel("Longitude", fontsize=10)
    ax.set_ylabel("Latitude", fontsize=10)
    ax.set_title("Carte des Distilleries de Whisky en Ecosse\nSingle Malts ~10 ans",
                 fontsize=16, fontweight="bold", pad=18)

    # Étiquettes de régions
    region_labels = [
        (-3.1, 57.35, "SPEYSIDE", "Speyside"),
        (-4.0, 57.5,  "HIGHLANDS", "Highlands"),
        (-6.15, 55.75, "ISLAY", "Islay"),
        (-4.0, 55.5,  "LOWLANDS", "Lowlands"),
        (-5.6, 55.3,  "CAMPBELTOWN", "Campbeltown"),
        (-5.5, 56.8,  "ISLANDS", "Islands"),
    ]
    for lx, ly, label, region in region_labels:
        ax.text(lx, ly, label, fontsize=9, fontweight="bold",
                color=REGION_COLORS[region], alpha=0.7,
                ha="center", zorder=4)

    fig.tight_layout()
    out = MAPS_DIR / "scotland_distilleries_map.png"
    fig.savefig(out, bbox_inches="tight", dpi=180)
    plt.close(fig)
    print(f"  ✓ {out.name}")


if __name__ == "__main__":
    print("🗺️  Génération de la carte...\n")
    generate_map()
    print("\n✅ Carte générée!")
