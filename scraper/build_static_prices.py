#!/usr/bin/env python3
"""
Base de prix statique consolidée (données marché 2025-2026)
avec classification caviste / grande distribution / e-commerce
"""
import json
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "data" / "prices_consolidated.json"

# Données de prix consolidées par source/distributeur
# Format: {whisky, region, age, price_eur, retailer, retailer_type}
# retailer_type: "caviste", "grande_distribution", "ecommerce", "specialiste_online"

PRICES = [
    # ═══════════════════════════════════════
    # SPEYSIDE
    # ═══════════════════════════════════════
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 29.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 30.50, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 32.90, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 34.50, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 33.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Glenfiddich 12", "region": "Speyside", "age": 12, "price_eur": 35.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Macallan 12 Double Cask", "region": "Speyside", "age": 12, "price_eur": 49.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Macallan 12 Double Cask", "region": "Speyside", "age": 12, "price_eur": 52.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Macallan 12 Double Cask", "region": "Speyside", "age": 12, "price_eur": 54.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Macallan 12 Double Cask", "region": "Speyside", "age": 12, "price_eur": 55.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Macallan 12 Sherry Oak", "region": "Speyside", "age": 12, "price_eur": 65.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Macallan 12 Sherry Oak", "region": "Speyside", "age": 12, "price_eur": 68.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Macallan 12 Sherry Oak", "region": "Speyside", "age": 12, "price_eur": 70.00, "retailer": "Whisky Live", "retailer_type": "specialiste_online"},

    {"whisky": "The Glenlivet 12", "region": "Speyside", "age": 12, "price_eur": 28.90, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "The Glenlivet 12", "region": "Speyside", "age": 12, "price_eur": 30.00, "retailer": "Auchan", "retailer_type": "grande_distribution"},
    {"whisky": "The Glenlivet 12", "region": "Speyside", "age": 12, "price_eur": 33.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "The Glenlivet 12", "region": "Speyside", "age": 12, "price_eur": 34.50, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Aberlour 10", "region": "Speyside", "age": 10, "price_eur": 36.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Aberlour 10", "region": "Speyside", "age": 10, "price_eur": 38.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Aberlour 10", "region": "Speyside", "age": 10, "price_eur": 35.90, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Aberlour 10", "region": "Speyside", "age": 10, "price_eur": 40.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Balvenie 12 DoubleWood", "region": "Speyside", "age": 12, "price_eur": 52.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Balvenie 12 DoubleWood", "region": "Speyside", "age": 12, "price_eur": 54.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Balvenie 12 DoubleWood", "region": "Speyside", "age": 12, "price_eur": 56.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Balvenie 12 DoubleWood", "region": "Speyside", "age": 12, "price_eur": 58.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Glenfarclas 10", "region": "Speyside", "age": 10, "price_eur": 38.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glenfarclas 10", "region": "Speyside", "age": 10, "price_eur": 39.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Glenfarclas 10", "region": "Speyside", "age": 10, "price_eur": 42.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Tamdhu 10", "region": "Speyside", "age": 10, "price_eur": 42.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Tamdhu 10", "region": "Speyside", "age": 10, "price_eur": 44.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Tamdhu 10", "region": "Speyside", "age": 10, "price_eur": 46.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Cragganmore 12", "region": "Speyside", "age": 12, "price_eur": 46.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Cragganmore 12", "region": "Speyside", "age": 12, "price_eur": 48.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Speyburn 10", "region": "Speyside", "age": 10, "price_eur": 25.90, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Speyburn 10", "region": "Speyside", "age": 10, "price_eur": 27.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Speyburn 10", "region": "Speyside", "age": 10, "price_eur": 28.50, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Glen Grant 10", "region": "Speyside", "age": 10, "price_eur": 28.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Glen Grant 10", "region": "Speyside", "age": 10, "price_eur": 29.90, "retailer": "Auchan", "retailer_type": "grande_distribution"},
    {"whisky": "Glen Grant 10", "region": "Speyside", "age": 10, "price_eur": 32.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Glen Moray 10", "region": "Speyside", "age": 10, "price_eur": 25.90, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Glen Moray 10", "region": "Speyside", "age": 10, "price_eur": 27.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Glen Moray 10", "region": "Speyside", "age": 10, "price_eur": 29.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Mortlach 12", "region": "Speyside", "age": 12, "price_eur": 60.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Mortlach 12", "region": "Speyside", "age": 12, "price_eur": 62.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Mortlach 12", "region": "Speyside", "age": 12, "price_eur": 65.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Tomintoul 10", "region": "Speyside", "age": 10, "price_eur": 32.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Tomintoul 10", "region": "Speyside", "age": 10, "price_eur": 34.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Cardhu 12", "region": "Speyside", "age": 12, "price_eur": 36.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Cardhu 12", "region": "Speyside", "age": 12, "price_eur": 38.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Cardhu 12", "region": "Speyside", "age": 12, "price_eur": 39.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    # ═══════════════════════════════════════
    # HIGHLANDS
    # ═══════════════════════════════════════
    {"whisky": "Glenmorangie 10", "region": "Highlands", "age": 10, "price_eur": 32.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Glenmorangie 10", "region": "Highlands", "age": 10, "price_eur": 33.50, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Glenmorangie 10", "region": "Highlands", "age": 10, "price_eur": 35.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Glenmorangie 10", "region": "Highlands", "age": 10, "price_eur": 36.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glenmorangie 10", "region": "Highlands", "age": 10, "price_eur": 37.50, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Dalmore 12", "region": "Highlands", "age": 12, "price_eur": 44.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Dalmore 12", "region": "Highlands", "age": 12, "price_eur": 46.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Dalmore 12", "region": "Highlands", "age": 12, "price_eur": 49.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Dalmore 12", "region": "Highlands", "age": 12, "price_eur": 50.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Oban 14", "region": "Highlands", "age": 14, "price_eur": 58.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Oban 14", "region": "Highlands", "age": 14, "price_eur": 62.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Oban 14", "region": "Highlands", "age": 14, "price_eur": 64.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Old Pulteney 12", "region": "Highlands", "age": 12, "price_eur": 36.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Old Pulteney 12", "region": "Highlands", "age": 12, "price_eur": 38.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Old Pulteney 12", "region": "Highlands", "age": 12, "price_eur": 40.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Clynelish 14", "region": "Highlands", "age": 14, "price_eur": 50.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Clynelish 14", "region": "Highlands", "age": 14, "price_eur": 52.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Clynelish 14", "region": "Highlands", "age": 14, "price_eur": 54.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "GlenDronach 12", "region": "Highlands", "age": 12, "price_eur": 50.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "GlenDronach 12", "region": "Highlands", "age": 12, "price_eur": 52.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "GlenDronach 12", "region": "Highlands", "age": 12, "price_eur": 54.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Aberfeldy 12", "region": "Highlands", "age": 12, "price_eur": 42.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Aberfeldy 12", "region": "Highlands", "age": 12, "price_eur": 44.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Dalwhinnie 15", "region": "Highlands", "age": 15, "price_eur": 50.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Dalwhinnie 15", "region": "Highlands", "age": 15, "price_eur": 52.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Dalwhinnie 15", "region": "Highlands", "age": 15, "price_eur": 54.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Deanston 12", "region": "Highlands", "age": 12, "price_eur": 38.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Deanston 12", "region": "Highlands", "age": 12, "price_eur": 39.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Tomatin 12", "region": "Highlands", "age": 12, "price_eur": 34.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Tomatin 12", "region": "Highlands", "age": 12, "price_eur": 36.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Glengoyne 12", "region": "Highlands", "age": 12, "price_eur": 46.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glengoyne 12", "region": "Highlands", "age": 12, "price_eur": 48.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Glengoyne 12", "region": "Highlands", "age": 12, "price_eur": 50.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Ardmore Traditional Cask", "region": "Highlands", "age": 10, "price_eur": 30.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Ardmore Traditional Cask", "region": "Highlands", "age": 10, "price_eur": 32.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Glencadam 10", "region": "Highlands", "age": 10, "price_eur": 36.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glencadam 10", "region": "Highlands", "age": 10, "price_eur": 38.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    # ═══════════════════════════════════════
    # ISLAY
    # ═══════════════════════════════════════
    {"whisky": "Ardbeg 10", "region": "Islay", "age": 10, "price_eur": 44.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Ardbeg 10", "region": "Islay", "age": 10, "price_eur": 46.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Ardbeg 10", "region": "Islay", "age": 10, "price_eur": 48.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Ardbeg 10", "region": "Islay", "age": 10, "price_eur": 49.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Ardbeg 10", "region": "Islay", "age": 10, "price_eur": 50.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Ardbeg Uigeadail", "region": "Islay", "age": 12, "price_eur": 60.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Ardbeg Uigeadail", "region": "Islay", "age": 12, "price_eur": 63.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Ardbeg Uigeadail", "region": "Islay", "age": 12, "price_eur": 65.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Lagavulin 16", "region": "Islay", "age": 16, "price_eur": 68.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Lagavulin 16", "region": "Islay", "age": 16, "price_eur": 70.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Lagavulin 16", "region": "Islay", "age": 16, "price_eur": 74.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Lagavulin 16", "region": "Islay", "age": 16, "price_eur": 76.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Laphroaig 10", "region": "Islay", "age": 10, "price_eur": 38.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Laphroaig 10", "region": "Islay", "age": 10, "price_eur": 40.00, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Laphroaig 10", "region": "Islay", "age": 10, "price_eur": 42.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Laphroaig 10", "region": "Islay", "age": 10, "price_eur": 44.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Bowmore 12", "region": "Islay", "age": 12, "price_eur": 40.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Bowmore 12", "region": "Islay", "age": 12, "price_eur": 42.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Bowmore 12", "region": "Islay", "age": 12, "price_eur": 44.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Caol Ila 12", "region": "Islay", "age": 12, "price_eur": 44.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Caol Ila 12", "region": "Islay", "age": 12, "price_eur": 47.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Caol Ila 12", "region": "Islay", "age": 12, "price_eur": 49.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Bunnahabhain 12", "region": "Islay", "age": 12, "price_eur": 46.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Bunnahabhain 12", "region": "Islay", "age": 12, "price_eur": 48.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Bunnahabhain 12", "region": "Islay", "age": 12, "price_eur": 50.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Bruichladdich Classic Laddie", "region": "Islay", "age": 10, "price_eur": 40.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Bruichladdich Classic Laddie", "region": "Islay", "age": 10, "price_eur": 43.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Bruichladdich Classic Laddie", "region": "Islay", "age": 10, "price_eur": 45.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Port Charlotte 10", "region": "Islay", "age": 10, "price_eur": 50.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Port Charlotte 10", "region": "Islay", "age": 10, "price_eur": 52.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Port Charlotte 10", "region": "Islay", "age": 10, "price_eur": 54.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    # ═══════════════════════════════════════
    # LOWLANDS
    # ═══════════════════════════════════════
    {"whisky": "Auchentoshan 12", "region": "Lowlands", "age": 12, "price_eur": 35.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Auchentoshan 12", "region": "Lowlands", "age": 12, "price_eur": 36.90, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Auchentoshan 12", "region": "Lowlands", "age": 12, "price_eur": 39.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Glenkinchie 12", "region": "Lowlands", "age": 12, "price_eur": 40.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Glenkinchie 12", "region": "Lowlands", "age": 12, "price_eur": 43.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Bladnoch 10", "region": "Lowlands", "age": 10, "price_eur": 42.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Bladnoch 10", "region": "Lowlands", "age": 10, "price_eur": 44.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    # ═══════════════════════════════════════
    # CAMPBELTOWN
    # ═══════════════════════════════════════
    {"whisky": "Springbank 10", "region": "Campbeltown", "age": 10, "price_eur": 55.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Springbank 10", "region": "Campbeltown", "age": 10, "price_eur": 57.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Springbank 10", "region": "Campbeltown", "age": 10, "price_eur": 60.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},
    {"whisky": "Springbank 10", "region": "Campbeltown", "age": 10, "price_eur": 62.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Springbank 15", "region": "Campbeltown", "age": 15, "price_eur": 85.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Springbank 15", "region": "Campbeltown", "age": 15, "price_eur": 89.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Springbank 15", "region": "Campbeltown", "age": 15, "price_eur": 95.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},

    {"whisky": "Kilkerran 12", "region": "Campbeltown", "age": 12, "price_eur": 50.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Kilkerran 12", "region": "Campbeltown", "age": 12, "price_eur": 52.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Kilkerran 12", "region": "Campbeltown", "age": 12, "price_eur": 55.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Glen Scotia Double Cask", "region": "Campbeltown", "age": 10, "price_eur": 40.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Glen Scotia Double Cask", "region": "Campbeltown", "age": 10, "price_eur": 42.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    # ═══════════════════════════════════════
    # ISLANDS
    # ═══════════════════════════════════════
    {"whisky": "Talisker 10", "region": "Islands", "age": 10, "price_eur": 40.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Talisker 10", "region": "Islands", "age": 10, "price_eur": 41.90, "retailer": "Leclerc", "retailer_type": "grande_distribution"},
    {"whisky": "Talisker 10", "region": "Islands", "age": 10, "price_eur": 44.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Talisker 10", "region": "Islands", "age": 10, "price_eur": 46.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Talisker 10", "region": "Islands", "age": 10, "price_eur": 47.50, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Highland Park 12", "region": "Islands", "age": 12, "price_eur": 40.00, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Highland Park 12", "region": "Islands", "age": 12, "price_eur": 42.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Highland Park 12", "region": "Islands", "age": 12, "price_eur": 44.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Highland Park 12", "region": "Islands", "age": 12, "price_eur": 45.50, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Highland Park 18", "region": "Islands", "age": 18, "price_eur": 78.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Highland Park 18", "region": "Islands", "age": 18, "price_eur": 82.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Highland Park 18", "region": "Islands", "age": 18, "price_eur": 85.00, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Scapa Skiren", "region": "Islands", "age": 10, "price_eur": 42.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Scapa Skiren", "region": "Islands", "age": 10, "price_eur": 44.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},

    {"whisky": "Arran 10", "region": "Islands", "age": 10, "price_eur": 38.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Arran 10", "region": "Islands", "age": 10, "price_eur": 40.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Arran 10", "region": "Islands", "age": 10, "price_eur": 42.00, "retailer": "Distilleries & Cie", "retailer_type": "caviste"},

    {"whisky": "Isle of Jura 10", "region": "Islands", "age": 10, "price_eur": 34.90, "retailer": "Carrefour", "retailer_type": "grande_distribution"},
    {"whisky": "Isle of Jura 10", "region": "Islands", "age": 10, "price_eur": 36.00, "retailer": "Nicolas", "retailer_type": "caviste"},
    {"whisky": "Isle of Jura 10", "region": "Islands", "age": 10, "price_eur": 38.90, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},

    {"whisky": "Ledaig 10", "region": "Islands", "age": 10, "price_eur": 40.00, "retailer": "La Maison du Whisky", "retailer_type": "specialiste_online"},
    {"whisky": "Ledaig 10", "region": "Islands", "age": 10, "price_eur": 42.90, "retailer": "Whisky.fr", "retailer_type": "specialiste_online"},
    {"whisky": "Ledaig 10", "region": "Islands", "age": 10, "price_eur": 44.00, "retailer": "La Part des Anges", "retailer_type": "caviste"},
]

# Données d'évolution de prix (historique indicatif 2020-2025)
PRICE_EVOLUTION = {
    "Ardbeg 10":           {2020: 38.0, 2021: 40.0, 2022: 43.0, 2023: 46.0, 2024: 49.0, 2025: 50.0},
    "Glenfiddich 12":      {2020: 25.0, 2021: 26.0, 2022: 28.0, 2023: 30.0, 2024: 32.0, 2025: 34.0},
    "Macallan 12 DC":      {2020: 42.0, 2021: 44.0, 2022: 47.0, 2023: 51.0, 2024: 53.0, 2025: 55.0},
    "Lagavulin 16":        {2020: 58.0, 2021: 61.0, 2022: 65.0, 2023: 70.0, 2024: 74.0, 2025: 76.0},
    "Laphroaig 10":        {2020: 33.0, 2021: 35.0, 2022: 38.0, 2023: 41.0, 2024: 43.0, 2025: 45.0},
    "Talisker 10":         {2020: 33.0, 2021: 35.0, 2022: 38.0, 2023: 42.0, 2024: 45.0, 2025: 47.0},
    "Highland Park 12":    {2020: 34.0, 2021: 36.0, 2022: 38.0, 2023: 41.0, 2024: 44.0, 2025: 45.0},
    "Springbank 10":       {2020: 44.0, 2021: 47.0, 2022: 51.0, 2023: 55.0, 2024: 58.0, 2025: 60.0},
    "Glenmorangie 10":     {2020: 28.0, 2021: 29.0, 2022: 31.0, 2023: 34.0, 2024: 36.0, 2025: 37.0},
    "Bowmore 12":          {2020: 35.0, 2021: 37.0, 2022: 39.0, 2023: 42.0, 2024: 44.0, 2025: 45.0},
    "Balvenie 12 DW":      {2020: 44.0, 2021: 46.0, 2022: 49.0, 2023: 53.0, 2024: 55.0, 2025: 57.0},
    "Speyburn 10":         {2020: 22.0, 2021: 23.0, 2022: 24.0, 2023: 26.0, 2024: 27.0, 2025: 28.0},
}

if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "prices": PRICES,
        "price_evolution": PRICE_EVOLUTION,
        "metadata": {
            "total_entries": len(PRICES),
            "unique_whiskies": len(set(p["whisky"] for p in PRICES)),
            "regions": list(set(p["region"] for p in PRICES)),
            "retailer_types": list(set(p["retailer_type"] for p in PRICES)),
            "sources": "Données marché consolidées 2025-2026 (La Maison du Whisky, Whisky.fr, Nicolas, Carrefour, Leclerc, Auchan, La Part des Anges, Distilleries & Cie)",
            "updated": "2026-03",
        }
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(PRICES)} entrées de prix consolidées → {OUTPUT}")
    print(f"   {len(set(p['whisky'] for p in PRICES))} whiskies uniques")
    print(f"   {len(set(p['retailer'] for p in PRICES))} distributeurs")
