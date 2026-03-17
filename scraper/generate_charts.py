#!/usr/bin/env python3
"""
Génération des graphiques de prix :
1. Prix par région (boxplot)
2. Prix par distributeur (type)
3. Évolution des prix 2020-2025 (line chart)
4. Classement top whiskies Q/P (bar chart)
5. Carte de chaleur prix × âge × région (heatmap)
"""

import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path(__file__).parent.parent / "data" / "prices_consolidated.json"
CHARTS_DIR = Path(__file__).parent.parent / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

# Palette par région
REGION_COLORS = {
    "Speyside":    "#F4C430",   # or
    "Highlands":   "#2E8B57",   # vert forêt
    "Islay":       "#1E3A5F",   # bleu nuit
    "Lowlands":    "#E8A87C",   # saumon
    "Campbeltown": "#8B4513",   # brun
    "Islands":     "#6A5ACD",   # violet ardoise
}

RETAILER_COLORS = {
    "grande_distribution": "#4CAF50",
    "caviste":             "#FF9800",
    "specialiste_online":  "#2196F3",
    "ecommerce":           "#9C27B0",
}

RETAILER_LABELS = {
    "grande_distribution": "Grande distribution",
    "caviste":             "Caviste",
    "specialiste_online":  "Spécialiste online",
    "ecommerce":           "E-commerce",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
    "axes.grid": True,
    "grid.alpha": 0.4,
})


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


# ─── GRAPHIQUE 1 : Boxplot prix par région ───────────────────────────────────
def chart_prix_region(prices):
    regions = list(REGION_COLORS.keys())
    data_by_region = defaultdict(list)
    for p in prices:
        data_by_region[p["region"]].append(p["price_eur"])

    fig, ax = plt.subplots(figsize=(12, 7))
    bp = ax.boxplot(
        [data_by_region[r] for r in regions],
        labels=regions,
        patch_artist=True,
        notch=False,
        widths=0.5,
        medianprops={"color": "white", "linewidth": 2.5},
    )
    for patch, region in zip(bp["boxes"], regions):
        patch.set_facecolor(REGION_COLORS[region])
        patch.set_alpha(0.85)

    # Overlay scatter
    for i, region in enumerate(regions):
        y = data_by_region[region]
        x = np.random.normal(i + 1, 0.07, len(y))
        ax.scatter(x, y, alpha=0.5, s=18, color=REGION_COLORS[region], zorder=3)

    ax.set_title("🥃 Distribution des prix par région — Single Malts Écossais ~10 ans", fontweight="bold", pad=15)
    ax.set_ylabel("Prix (€)")
    ax.set_xlabel("Région")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}€"))
    fig.tight_layout()
    out = CHARTS_DIR / "01_prix_par_region.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ─── GRAPHIQUE 2 : Prix moyen par type de distributeur ───────────────────────
def chart_prix_distributeur(prices):
    # Prix moyen par whisky × type de distributeur
    data = defaultdict(lambda: defaultdict(list))
    for p in prices:
        data[p["retailer_type"]][p["whisky"]].append(p["price_eur"])

    types = ["grande_distribution", "caviste", "specialiste_online"]
    means = {t: [] for t in types}
    whiskies_common = None

    for t in types:
        wh = set(data[t].keys())
        whiskies_common = wh if whiskies_common is None else whiskies_common & wh

    whiskies_common = sorted(whiskies_common)
    for t in types:
        for w in whiskies_common:
            means[t].append(np.mean(data[t][w]))

    x = np.arange(len(whiskies_common))
    width = 0.25
    fig, ax = plt.subplots(figsize=(16, 7))

    for i, t in enumerate(types):
        bars = ax.bar(x + i * width, means[t], width, label=RETAILER_LABELS[t],
                      color=RETAILER_COLORS[t], alpha=0.85, edgecolor="white")

    ax.set_title("💰 Comparaison des prix par type de distributeur", fontweight="bold", pad=15)
    ax.set_ylabel("Prix moyen (€)")
    ax.set_xticks(x + width)
    ax.set_xticklabels([w[:22] for w in whiskies_common], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}€"))
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    out = CHARTS_DIR / "02_prix_par_distributeur.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ─── GRAPHIQUE 3 : Évolution des prix 2020-2025 ──────────────────────────────
def chart_evolution(evolution):
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    fig, ax = plt.subplots(figsize=(13, 7))

    # Groupes de whiskies pour la lisibilité
    groups = {
        "Islay (tourbés)":   ["Ardbeg 10", "Laphroaig 10", "Lagavulin 16", "Bowmore 12"],
        "Speyside (fruités)": ["Glenfiddich 12", "Macallan 12 DC", "Balvenie 12 DW", "Speyburn 10"],
        "Autres":             ["Glenmorangie 10", "Talisker 10", "Highland Park 12", "Springbank 10"],
    }

    linestyles = ["-", "--", ":"]
    markers = ["o", "s", "^", "D"]
    cmap = plt.cm.tab20

    idx = 0
    for grp_name, whiskies in groups.items():
        for j, w in enumerate(whiskies):
            if w not in evolution:
                continue
            vals = [evolution[w][str(yr)] if str(yr) in evolution[w] else evolution[w].get(yr) for yr in years]
            pct_increase = ((vals[-1] - vals[0]) / vals[0]) * 100
            label = f"{w} (+{pct_increase:.0f}%)"
            ax.plot(years, vals, marker=markers[j], linestyle=linestyles[list(groups.keys()).index(grp_name)],
                    label=label, color=cmap(idx / 12), linewidth=1.8, markersize=5)
            idx += 1

    ax.set_title("📈 Évolution des prix 2020–2025 — Single Malts Écossais", fontweight="bold", pad=15)
    ax.set_ylabel("Prix constaté (€, source La Maison du Whisky / marché)")
    ax.set_xlabel("Année")
    ax.set_xticks(years)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}€"))
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9, ncol=2)

    # Annotation inflation
    ax.annotate("↑ Inflation + demande mondiale\n+20 à +35% sur 5 ans",
                xy=(2023, 68), fontsize=9, color="#CC0000",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFE4E4", alpha=0.8))

    fig.tight_layout()
    out = CHARTS_DIR / "03_evolution_prix_2020_2025.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ─── GRAPHIQUE 4 : Top Q/P (rapport qualité/prix) ────────────────────────────
def chart_qualite_prix(prices):
    # Prix moyen par whisky
    whisky_prices = defaultdict(list)
    whisky_region = {}
    for p in prices:
        whisky_prices[p["whisky"]].append(p["price_eur"])
        whisky_region[p["whisky"]] = p["region"]

    # Score Q/P subjectif (noté /10, basé sur réputation + prix)
    qp_scores = {
        "Speyburn 10": 9.1, "Glen Moray 10": 8.8, "Glen Grant 10": 8.5,
        "Tomintoul 10": 8.7, "Glenmorangie 10": 9.0, "Ardmore Traditional Cask": 8.9,
        "Glencadam 10": 9.2, "Arran 10": 8.8, "Isle of Jura 10": 8.5,
        "Old Pulteney 12": 8.9, "Aberlour 10": 8.8, "Tomatin 12": 8.7,
        "Deanston 12": 8.6, "Glenfarclas 10": 8.9, "Highland Park 12": 9.1,
        "Bowmore 12": 8.8, "Laphroaig 10": 9.0, "Caol Ila 12": 9.0,
        "Kilkerran 12": 9.2, "Glen Scotia Double Cask": 8.7,
        "Springbank 10": 9.5, "Ardbeg 10": 9.4, "Balvenie 12 DoubleWood": 9.0,
        "GlenDronach 12": 9.1, "Clynelish 14": 9.3,
        "Glenfiddich 12": 8.2, "Glenkinchie 12": 8.0, "Auchentoshan 12": 8.1,
    }

    common = [w for w in qp_scores if w in whisky_prices]
    common.sort(key=lambda w: qp_scores[w], reverse=True)
    top = common[:20]

    avg_prices = [np.mean(whisky_prices[w]) for w in top]
    scores = [qp_scores[w] for w in top]
    colors = [REGION_COLORS.get(whisky_region.get(w, ""), "#999") for w in top]

    fig, ax = plt.subplots(figsize=(13, 8))
    bars = ax.barh(range(len(top)), scores, color=colors, alpha=0.85, edgecolor="white")

    # Annotations prix
    for i, (score, price) in enumerate(zip(scores, avg_prices)):
        ax.text(score + 0.02, i, f"  ~{price:.0f}€", va="center", fontsize=8.5, color="#333")

    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(top)
    ax.set_xlabel("Score Qualité/Prix (/10)")
    ax.set_title("🏆 Top 20 Whiskies — Rapport Qualité/Prix (~10 ans)", fontweight="bold", pad=15)
    ax.set_xlim(7.8, 10.0)

    # Légende régions
    legend_patches = [mpatches.Patch(color=c, label=r) for r, c in REGION_COLORS.items()]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8.5, title="Région", framealpha=0.9)

    fig.tight_layout()
    out = CHARTS_DIR / "04_top_qualite_prix.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ─── GRAPHIQUE 5 : Heatmap prix moyen par région × distributeur ──────────────
def chart_heatmap(prices):
    regions = list(REGION_COLORS.keys())
    retailer_types = ["grande_distribution", "caviste", "specialiste_online"]

    matrix = np.zeros((len(regions), len(retailer_types)))
    counts = np.zeros_like(matrix)

    for p in prices:
        r = regions.index(p["region"]) if p["region"] in regions else -1
        t_list = [k for k in retailer_types if k == p["retailer_type"]]
        if r < 0 or not t_list:
            continue
        t = retailer_types.index(t_list[0])
        matrix[r][t] += p["price_eur"]
        counts[r][t] += 1

    with np.errstate(divide="ignore", invalid="ignore"):
        avg_matrix = np.where(counts > 0, matrix / counts, np.nan)

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(avg_matrix, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(retailer_types)))
    ax.set_xticklabels([RETAILER_LABELS[t] for t in retailer_types])
    ax.set_yticks(range(len(regions)))
    ax.set_yticklabels(regions)

    # Valeurs dans chaque cellule
    for i in range(len(regions)):
        for j in range(len(retailer_types)):
            val = avg_matrix[i][j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.0f}€", ha="center", va="center",
                        color="black" if val < 60 else "white", fontweight="bold", fontsize=11)

    plt.colorbar(im, ax=ax, label="Prix moyen (€)")
    ax.set_title("🗺️ Prix moyen par Région × Type de distributeur", fontweight="bold", pad=15)
    fig.tight_layout()
    out = CHARTS_DIR / "05_heatmap_region_distributeur.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


# ─── GRAPHIQUE 6 : Échelle de prix annotée ───────────────────────────────────
def chart_echelle_prix(prices):
    whisky_avg = defaultdict(list)
    whisky_region = {}
    for p in prices:
        whisky_avg[p["whisky"]].append(p["price_eur"])
        whisky_region[p["whisky"]] = p["region"]

    items = [(w, np.mean(v), whisky_region[w]) for w, v in whisky_avg.items()]
    items.sort(key=lambda x: x[1])

    names = [x[0] for x in items]
    avgs  = [x[1] for x in items]
    cols  = [REGION_COLORS.get(x[2], "#888") for x in items]

    fig, ax = plt.subplots(figsize=(14, max(8, len(names) * 0.35)))
    ax.barh(range(len(names)), avgs, color=cols, alpha=0.85, edgecolor="white", height=0.75)

    for i, (name, val, reg) in enumerate(items):
        ax.text(val + 0.5, i, f"{val:.0f}€", va="center", fontsize=7.5)

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Prix moyen toutes sources (€)")
    ax.set_title("📊 Échelle de prix — Single Malts Écossais ~10 ans (du moins cher au plus cher)", fontweight="bold", pad=15)

    # Bandes de prix
    bands = [(0, 35, "#E8F5E9", "Budget\n< 35€"), (35, 50, "#FFF9C4", "Accessible\n35-50€"),
             (50, 65, "#FFE0B2", "Premium\n50-65€"), (65, 200, "#FFCDD2", "Luxe\n> 65€")]
    for xmin, xmax, color, label in bands:
        ax.axvspan(xmin, min(xmax, max(avgs)+5), alpha=0.12, color=color, zorder=0)

    legend_patches = [mpatches.Patch(color=c, label=r) for r, c in REGION_COLORS.items()]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8, title="Région", framealpha=0.9)

    fig.tight_layout()
    out = CHARTS_DIR / "06_echelle_prix_complete.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {out.name}")


if __name__ == "__main__":
    print("📊 Génération des graphiques...\n")
    d = load_data()
    prices = d["prices"]
    evolution = d["price_evolution"]

    chart_prix_region(prices)
    chart_prix_distributeur(prices)
    chart_evolution(evolution)
    chart_qualite_prix(prices)
    chart_heatmap(prices)
    chart_echelle_prix(prices)

    print(f"\n✅ 6 graphiques générés dans {CHARTS_DIR}")
