
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 4.7: SHIPPING PATTERN ANALYSIS
# ============================================================

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load dataset
df = pd.read_csv(DATA_PATH)

# 2. Parse dates
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# 3. Calculate shipping duration
df["Shipping Duration Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

# 4. Analyze by shipping mode
print("\n========== SHIPPING MODE ANALYSIS ==========\n")

mode_analysis = df.groupby("Ship Mode").agg(
    Records=("Row ID", "count"),
    Average_Duration=("Shipping Duration Days", "mean"),
    Median_Duration=("Shipping Duration Days", "median"),
    Minimum_Duration=("Shipping Duration Days", "min"),
    Maximum_Duration=("Shipping Duration Days", "max")
).round(2)

print(mode_analysis)

mode_analysis.to_csv(
    OUTPUT_DIR / "shipping_mode_date_analysis.csv"
)

# 5. Analyze by region
print("\n========== REGION ANALYSIS ==========\n")

region_analysis = df.groupby("Region").agg(
    Records=("Row ID", "count"),
    Average_Duration=("Shipping Duration Days", "mean"),
    Median_Duration=("Shipping Duration Days", "median"),
    Minimum_Duration=("Shipping Duration Days", "min"),
    Maximum_Duration=("Shipping Duration Days", "max")
).round(2)

print(region_analysis)

region_analysis.to_csv(
    OUTPUT_DIR / "region_date_analysis.csv"
)

# 6. Analyze by country
print("\n========== COUNTRY ANALYSIS ==========\n")

country_analysis = df.groupby("Country/Region").agg(
    Records=("Row ID", "count"),
    Average_Duration=("Shipping Duration Days", "mean"),
    Median_Duration=("Shipping Duration Days", "median")
).round(2)

print(country_analysis)

# 7. Analyze by division
print("\n========== DIVISION ANALYSIS ==========\n")

division_analysis = df.groupby("Division").agg(
    Records=("Row ID", "count"),
    Average_Duration=("Shipping Duration Days", "mean"),
    Median_Duration=("Shipping Duration Days", "median")
).round(2)

print(division_analysis)

# 8. Check order ID structure
print("\n========== ORDER ID ANALYSIS ==========\n")

print("First 15 Order IDs:")
print(df["Order ID"].head(15).to_string(index=False))

print("\nOrder ID examples and corresponding dates:")

print(
    df[
        ["Order ID", "Order Date", "Ship Date", "Ship Mode"]
    ].drop_duplicates("Order ID").head(15).to_string(index=False)
)

# 9. Check whether identical order dates have different ship dates
print("\n========== DATE PATTERN CHECK ==========\n")

date_pattern = df.groupby("Order Date").agg(
    Unique_Ship_Dates=("Ship Date", "nunique"),
    Unique_Shipping_Modes=("Ship Mode", "nunique"),
    Records=("Row ID", "count")
)

print("Order dates with multiple ship dates:")
print((date_pattern["Unique_Ship_Dates"] > 1).sum())

print("\nOrder dates with multiple shipping modes:")
print((date_pattern["Unique_Shipping_Modes"] > 1).sum())

# 10. Save combined investigation data
df[
    [
        "Row ID",
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Country/Region",
        "City",
        "State/Province",
        "Region",
        "Division",
        "Shipping Duration Days"
    ]
].to_csv(
    OUTPUT_DIR / "shipping_pattern_investigation.csv",
    index=False
)

print("\n========== STEP 4.7 COMPLETED ==========\n")

print("Saved investigation files in outputs/")
