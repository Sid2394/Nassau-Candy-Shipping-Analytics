
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 6.1: DATA VISUALIZATIONS
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"
CHART_DIR = BASE_DIR / "outputs" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

# General chart settings
sns.set_theme(style="whitegrid")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# ============================================================
# CHART 1: SHIPPING MODE DISTRIBUTION
# ============================================================

mode_counts = df["Ship Mode"].value_counts()

plt.figure(figsize=(9, 6))

sns.barplot(
    x=mode_counts.index,
    y=mode_counts.values
)

plt.title("Shipping Mode Distribution", fontsize=16)
plt.xlabel("Shipping Mode")
plt.ylabel("Number of Records")
plt.xticks(rotation=15)

for i, value in enumerate(mode_counts.values):
    plt.text(i, value + 50, str(value), ha="center")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "01_shipping_mode_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# CHART 2: REGIONAL SALES
# ============================================================

region_sales = df.groupby("Region")["Sales"].sum().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=region_sales.index,
    y=region_sales.values
)

plt.title("Total Sales by Region", fontsize=16)
plt.xlabel("Region")
plt.ylabel("Total Sales ($)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "02_regional_sales.png",
    dpi=300
)

plt.close()

# ============================================================
# CHART 3: REGIONAL SHIPPING MODE HEATMAP
# ============================================================

region_mode_percentage = pd.crosstab(
    df["Region"],
    df["Ship Mode"],
    normalize="index"
) * 100

plt.figure(figsize=(10, 6))

sns.heatmap(
    region_mode_percentage,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu"
)

plt.title("Shipping Mode Distribution Across Regions", fontsize=16)
plt.xlabel("Shipping Mode")
plt.ylabel("Region")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "03_region_shipping_heatmap.png",
    dpi=300
)

plt.close()

# ============================================================
# CHART 4: SHIPPING MODE PROFIT
# ============================================================

mode_profit = df.groupby("Ship Mode")["Gross Profit"].sum().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

sns.barplot(
    x=mode_profit.index,
    y=mode_profit.values
)

plt.title("Gross Profit by Shipping Mode", fontsize=16)
plt.xlabel("Shipping Mode")
plt.ylabel("Gross Profit ($)")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "04_shipping_mode_profit.png",
    dpi=300
)

plt.close()

# ============================================================
# CHART 5: TOP 10 CITIES BY SALES
# ============================================================

city_sales = df.groupby(
    ["City", "State/Province"]
)["Sales"].sum().sort_values(
    ascending=False
).head(10)

city_labels = [
    f"{city}, {state}"
    for city, state in city_sales.index
]

plt.figure(figsize=(11, 7))

sns.barplot(
    x=city_sales.values,
    y=city_labels
)

plt.title("Top 10 Destinations by Sales", fontsize=16)
plt.xlabel("Total Sales ($)")
plt.ylabel("Destination City")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "05_top_10_cities.png",
    dpi=300
)

plt.close()

# ============================================================
# CHART 6: REGIONAL PROFIT CONTRIBUTION
# ============================================================

region_profit = df.groupby("Region")["Gross Profit"].sum().sort_values(
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.pie(
    region_profit.values,
    labels=region_profit.index,
    autopct="%1.2f%%",
    startangle=90
)

plt.title("Regional Gross Profit Contribution", fontsize=16)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "06_regional_profit_contribution.png",
    dpi=300
)

plt.close()

# ============================================================
# COMPLETION
# ============================================================

print("\n========== VISUALIZATION COMPLETED ==========\n")

print("Six charts generated successfully.")

for chart in sorted(CHART_DIR.glob("*.png")):
    print(chart.name)

print("\nCharts location:")
print(CHART_DIR)
