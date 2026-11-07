
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 4.6: SHIPPING DATE INVESTIGATION
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# 1. Load original dataset

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# 2. Parse dates correctly

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

# 4. Display sample records

print("\n========== SAMPLE DATE RECORDS ==========\n")

print(
    df[
        ["Row ID", "Order ID", "Order Date",
         "Ship Date", "Shipping Duration Days"]
    ].head(20).to_string(index=False)
)

# 5. Analyse shipping duration

print("\n========== SHIPPING DURATION ANALYSIS ==========\n")

print(df["Shipping Duration Days"].describe())

print("\nMost frequent shipping durations:")

print(
    df["Shipping Duration Days"]
    .value_counts()
    .head(15)
)

# 6. Group shipping duration by order year

print("\n========== DURATION BY ORDER YEAR ==========\n")

df["Order Year"] = df["Order Date"].dt.year

year_analysis = df.groupby("Order Year")[
    "Shipping Duration Days"
].agg(["count", "mean", "median", "min", "max"])

print(year_analysis)

year_analysis.to_csv(
    OUTPUT_DIR / "shipping_duration_by_order_year.csv"
)

# 7. Check shipping date distribution

print("\n========== SHIP YEAR DISTRIBUTION ==========\n")

df["Ship Year"] = df["Ship Date"].dt.year

print(df["Ship Year"].value_counts().sort_index())

# 8. Check relationship between order date and duration

print("\n========== DATE RELATIONSHIP ANALYSIS ==========\n")

df["Order Date Numeric"] = (
    df["Order Date"] - pd.Timestamp("2000-01-01")
).dt.days

correlation = df[
    ["Order Date Numeric", "Shipping Duration Days"]
].corr().iloc[0, 1]

print("Correlation between order date and shipping duration:")
print(correlation)

# Estimate the linear relationship.
# This is diagnostic only, not a date correction.

slope, intercept = np.polyfit(
    df["Order Date Numeric"],
    df["Shipping Duration Days"],
    1
)

print("\nEstimated duration trend:")
print("Slope:", slope)
print("Intercept:", intercept)

# 9. Check repeated Order IDs and their dates

print("\n========== ORDER DATE CONSISTENCY ==========\n")

order_analysis = df.groupby("Order ID").agg(
    Order_Date_Count=("Order Date", "nunique"),
    Ship_Date_Count=("Ship Date", "nunique"),
    Product_Lines=("Row ID", "count")
)

print("Orders with multiple order dates:")
print((order_analysis["Order_Date_Count"] > 1).sum())

print("Orders with multiple ship dates:")
print((order_analysis["Ship_Date_Count"] > 1).sum())

# 10. Save detailed investigation report

report_columns = [
    "Row ID",
    "Order ID",
    "Order Date",
    "Ship Date",
    "Shipping Duration Days",
    "Order Year",
    "Ship Year"
]

df[report_columns].to_csv(
    OUTPUT_DIR / "shipping_date_investigation.csv",
    index=False
)

print("\n========== INVESTIGATION COMPLETED ==========\n")

print("Saved: outputs/shipping_date_investigation.csv")
print("Saved: outputs/shipping_duration_by_order_year.csv")
