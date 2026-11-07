
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 5.2: SHIPPING DISTRIBUTION ANALYSIS
# ============================================================

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# 1. Load dataset
df = pd.read_csv(DATA_PATH)

print("\nDataset loaded:", df.shape)

# 2. Shipping mode distribution
print("\n========== SHIPPING MODE DISTRIBUTION ==========\n")

mode_distribution = df["Ship Mode"].value_counts().to_frame(
    name="Records"
)

mode_distribution["Percentage"] = (
    mode_distribution["Records"] / len(df) * 100
).round(2)

print(mode_distribution)

mode_distribution.to_csv(
    OUTPUT_DIR / "shipping_mode_distribution.csv"
)

# 3. Shipping mode distribution by region
print("\n========== REGION-WISE SHIPPING MODE COUNTS ==========\n")

region_mode_counts = pd.crosstab(
    df["Region"],
    df["Ship Mode"]
)

print(region_mode_counts)

region_mode_counts.to_csv(
    OUTPUT_DIR / "region_shipping_mode_counts.csv"
)

# 4. Shipping mode percentages within each region
print("\n========== REGION-WISE SHIPPING MODE PERCENTAGES ==========\n")

region_mode_percentage = pd.crosstab(
    df["Region"],
    df["Ship Mode"],
    normalize="index"
) * 100

region_mode_percentage = region_mode_percentage.round(2)

print(region_mode_percentage)

region_mode_percentage.to_csv(
    OUTPUT_DIR / "region_shipping_mode_percentages.csv"
)

# 5. Shipping mode financial contribution
print("\n========== SHIPPING MODE CONTRIBUTION ==========\n")

mode_financial = df.groupby("Ship Mode").agg(
    Records=("Row ID", "count"),
    Sales=("Sales", "sum"),
    Cost=("Cost", "sum"),
    Gross_Profit=("Gross Profit", "sum"),
    Units=("Units", "sum")
)

mode_financial["Sales_Contribution_Percent"] = (
    mode_financial["Sales"] / df["Sales"].sum() * 100
)

mode_financial["Profit_Contribution_Percent"] = (
    mode_financial["Gross_Profit"] /
    df["Gross Profit"].sum() * 100
)

mode_financial["Overall_Profit_Margin_Percent"] = (
    mode_financial["Gross_Profit"] /
    mode_financial["Sales"] * 100
)

mode_financial = mode_financial.round(2)

print(mode_financial)

mode_financial.to_csv(
    OUTPUT_DIR / "shipping_mode_contribution.csv"
)

# 6. Top 20 destination cities by sales
print("\n========== TOP 20 CITIES BY SALES ==========\n")

city_sales = df.groupby(
    ["Country/Region", "State/Province", "City"]
).agg(
    Records=("Row ID", "count"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).sort_values(
    "Total_Sales",
    ascending=False
).head(20).round(2)

print(city_sales)

city_sales.to_csv(
    OUTPUT_DIR / "top_20_cities_by_sales.csv"
)

# 7. Top 20 destinations by record volume
print("\n========== TOP 20 CITIES BY RECORD VOLUME ==========\n")

city_volume = df.groupby(
    ["Country/Region", "State/Province", "City"]
).agg(
    Records=("Row ID", "count"),
    Total_Sales=("Sales", "sum")
).sort_values(
    "Records",
    ascending=False
).head(20).round(2)

print(city_volume)

city_volume.to_csv(
    OUTPUT_DIR / "top_20_cities_by_volume.csv"
)

# 8. Region-wise contribution to total sales
print("\n========== REGION SALES CONTRIBUTION ==========\n")

region_sales = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Records=("Row ID", "count")
)

region_sales["Sales_Contribution_Percent"] = (
    region_sales["Total_Sales"] / df["Sales"].sum() * 100
)

region_sales["Profit_Contribution_Percent"] = (
    region_sales["Total_Profit"] /
    df["Gross Profit"].sum() * 100
)

region_sales = region_sales.round(2)

print(region_sales)

region_sales.to_csv(
    OUTPUT_DIR / "region_sales_contribution.csv"
)

print("\n========== STEP 5.2 COMPLETED ==========\n")

print("All shipping distribution reports saved in outputs/")
