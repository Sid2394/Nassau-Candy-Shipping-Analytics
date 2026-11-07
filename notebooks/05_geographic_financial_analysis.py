
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 5.1: GEOGRAPHIC AND FINANCIAL ANALYSIS
# ============================================================

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load dataset
df = pd.read_csv(DATA_PATH)

print("\nDataset loaded:", df.shape)

# 2. Create financial indicators
df["Profit Margin (%)"] = (
    df["Gross Profit"] / df["Sales"]
) * 100

df["Cost Percentage (%)"] = (
    df["Cost"] / df["Sales"]
) * 100

df["Profit Per Unit"] = (
    df["Gross Profit"] / df["Units"]
)

df["Sales Per Unit"] = (
    df["Sales"] / df["Units"]
)

# 3. Overall financial summary
print("\n========== OVERALL FINANCIAL SUMMARY ==========\n")

financial_summary = df[
    ["Sales", "Cost", "Gross Profit", "Units"]
].sum()

print(financial_summary)

print("\nAverage Profit Margin:")
print(round(df["Profit Margin (%)"].mean(), 2), "%")

print("\nOverall Profit Margin:")
print(
    round(
        (df["Gross Profit"].sum() / df["Sales"].sum()) * 100,
        2
    ),
    "%"
)

# 4. Region-wise analysis
print("\n========== REGION-WISE ANALYSIS ==========\n")

region_analysis = df.groupby("Region").agg(
    Records=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Average_Sales=("Sales", "mean"),
    Average_Profit_Margin=("Profit Margin (%)", "mean")
).round(2)

region_analysis = region_analysis.sort_values(
    "Total_Sales",
    ascending=False
)

print(region_analysis)

region_analysis.to_csv(
    OUTPUT_DIR / "region_financial_analysis.csv"
)

# 5. State-wise analysis
print("\n========== TOP 15 STATES / PROVINCES ==========\n")

state_analysis = df.groupby(
    ["Country/Region", "State/Province"]
).agg(
    Records=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Units=("Units", "sum")
).round(2)

state_analysis = state_analysis.sort_values(
    "Total_Sales",
    ascending=False
)

print(state_analysis.head(15))

state_analysis.to_csv(
    OUTPUT_DIR / "state_financial_analysis.csv"
)

# 6. City-wise analysis
print("\n========== TOP 15 CITIES ==========\n")

city_analysis = df.groupby(
    ["Country/Region", "State/Province", "City"]
).agg(
    Records=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Units=("Units", "sum")
).round(2)

city_analysis = city_analysis.sort_values(
    "Total_Sales",
    ascending=False
)

print(city_analysis.head(15))

city_analysis.to_csv(
    OUTPUT_DIR / "city_financial_analysis.csv"
)

# 7. Shipping mode financial analysis
print("\n========== SHIPPING MODE FINANCIAL ANALYSIS ==========\n")

mode_analysis = df.groupby("Ship Mode").agg(
    Records=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum"),
    Average_Sales=("Sales", "mean"),
    Average_Profit=("Gross Profit", "mean")
).round(2)

mode_analysis = mode_analysis.sort_values(
    "Total_Sales",
    ascending=False
)

print(mode_analysis)

mode_analysis.to_csv(
    OUTPUT_DIR / "shipping_mode_financial_analysis.csv"
)

# 8. Region and shipping mode relationship
print("\n========== REGION VS SHIPPING MODE ==========\n")

region_mode = pd.crosstab(
    df["Region"],
    df["Ship Mode"]
)

print(region_mode)

region_mode.to_csv(
    OUTPUT_DIR / "region_vs_shipping_mode.csv"
)

# 9. Country-wise analysis
print("\n========== COUNTRY FINANCIAL ANALYSIS ==========\n")

country_analysis = df.groupby("Country/Region").agg(
    Records=("Row ID", "count"),
    Unique_Orders=("Order ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    Total_Cost=("Cost", "sum"),
    Total_Profit=("Gross Profit", "sum"),
    Total_Units=("Units", "sum")
).round(2)

print(country_analysis)

country_analysis.to_csv(
    OUTPUT_DIR / "country_financial_analysis.csv"
)

# 10. Save complete dataset with financial indicators
df.to_csv(
    OUTPUT_DIR / "financial_analysis_dataset.csv",
    index=False
)

print("\n========== STEP 5.1 COMPLETED ==========\n")

print("All financial and geographic analysis files saved in outputs/")
