
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 4: DATA VALIDATION AND DATE CORRECTION
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------
# 1. Define paths
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 2. Load original dataset
# ------------------------------------------------------------

print("\n========== LOADING ORIGINAL DATASET ==========\n")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# ------------------------------------------------------------
# 3. Correct date formats
# ------------------------------------------------------------

print("\n========== DATE CORRECTION ==========\n")

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

print("Order Date Range:")
print("Minimum:", df["Order Date"].min())
print("Maximum:", df["Order Date"].max())

print("\nShip Date Range:")
print("Minimum:", df["Ship Date"].min())
print("Maximum:", df["Ship Date"].max())

print("\nInvalid Order Dates:", df["Order Date"].isna().sum())
print("Invalid Ship Dates:", df["Ship Date"].isna().sum())

# ------------------------------------------------------------
# 4. Calculate shipping duration
# ------------------------------------------------------------

print("\n========== SHIPPING DURATION ==========\n")

df["Shipping Duration Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print(df["Shipping Duration Days"].describe())

# ------------------------------------------------------------
# 5. Check shipment date consistency
# ------------------------------------------------------------

print("\n========== DATE CONSISTENCY CHECK ==========\n")

invalid_date_order = df[
    df["Ship Date"] < df["Order Date"]
]

print(
    "Ship dates before order dates:",
    len(invalid_date_order)
)

print(
    "Orders with missing or invalid dates:",
    df[["Order Date", "Ship Date"]].isna().any(axis=1).sum()
)

# Flag unusually long shipping durations.
# This is an investigation flag, NOT an automatic deletion rule.

df["Shipping Duration Flag"] = np.select(
    [
        df["Shipping Duration Days"].isna(),
        df["Shipping Duration Days"] < 0,
        df["Shipping Duration Days"] > 30
    ],
    [
        "Invalid Date",
        "Ship Date Before Order",
        "Over 30 Days - Investigate"
    ],
    default="Within 30 Days"
)

print("\nShipping Duration Flags:")
print(df["Shipping Duration Flag"].value_counts())

# ------------------------------------------------------------
# 6. Check Row ID uniqueness
# ------------------------------------------------------------

print("\n========== ROW ID VALIDATION ==========\n")

print("Unique Row IDs:", df["Row ID"].nunique())
print("Total Rows:", len(df))

print(
    "Duplicate Row IDs:",
    df["Row ID"].duplicated().sum()
)

# ------------------------------------------------------------
# 7. Check Order ID repetition
# ------------------------------------------------------------

print("\n========== ORDER ID VALIDATION ==========\n")

print("Unique Order IDs:", df["Order ID"].nunique())

print(
    "Repeated Order ID records:",
    df["Order ID"].duplicated().sum()
)

print("\nOrders with most product records:")

print(
    df["Order ID"].value_counts().head(10)
)

# Repeated Order IDs are not automatically errors.
# An order can contain multiple product lines.

# ------------------------------------------------------------
# 8. Validate financial calculations
# ------------------------------------------------------------

print("\n========== FINANCIAL VALIDATION ==========\n")

df["Calculated Sales"] = (
    df["Cost"] + df["Gross Profit"]
)

df["Financial Difference"] = (
    df["Sales"] - df["Calculated Sales"]
)

financial_mismatch = df[
    df["Financial Difference"].abs() > 0.01
]

print("Financial mismatches:", len(financial_mismatch))

print(
    "Maximum financial difference:",
    df["Financial Difference"].abs().max()
)

# ------------------------------------------------------------
# 9. Check negative and zero values
# ------------------------------------------------------------

print("\n========== NUMERIC VALIDATION ==========\n")

numeric_columns = [
    "Sales",
    "Cost",
    "Gross Profit",
    "Units"
]

for column in numeric_columns:

    print(f"\nColumn: {column}")

    print("Negative values:", (df[column] < 0).sum())

    print("Zero values:", (df[column] == 0).sum())

# ------------------------------------------------------------
# 10. Check categorical values
# ------------------------------------------------------------

print("\n========== CATEGORICAL VALIDATION ==========\n")

categorical_columns = [
    "Ship Mode",
    "Country/Region",
    "Division",
    "Region",
    "Product Name"
]

for column in categorical_columns:

    print(f"\n{column}")

    print("Unique values:", df[column].nunique())

    print(df[column].value_counts().head(10))

# ------------------------------------------------------------
# 11. Create data quality summary
# ------------------------------------------------------------

quality_summary = pd.DataFrame({

    "Check": [
        "Total Records",
        "Total Columns",
        "Missing Values",
        "Exact Duplicate Rows",
        "Duplicate Row IDs",
        "Unique Order IDs",
        "Invalid Order Dates",
        "Invalid Ship Dates",
        "Ship Before Order",
        "Financial Mismatches",
        "Negative Sales",
        "Negative Cost",
        "Negative Gross Profit",
        "Negative Units",
        "Zero Units"
    ],

    "Result": [
        len(df),
        len(df.columns) - 2,
        int(df.isnull().sum().sum()),
        int(df.duplicated().sum()),
        int(df["Row ID"].duplicated().sum()),
        int(df["Order ID"].nunique()),
        int(df["Order Date"].isna().sum()),
        int(df["Ship Date"].isna().sum()),
        len(invalid_date_order),
        len(financial_mismatch),
        int((df["Sales"] < 0).sum()),
        int((df["Cost"] < 0).sum()),
        int((df["Gross Profit"] < 0).sum()),
        int((df["Units"] < 0).sum()),
        int((df["Units"] == 0).sum())
    ]

})

print("\n========== DATA QUALITY SUMMARY ==========\n")

print(quality_summary.to_string(index=False))

# ------------------------------------------------------------
# 12. Save validated dataset
# ------------------------------------------------------------

VALIDATED_PATH = (
    PROCESSED_DIR / "nassau_candy_validated.csv"
)

df.to_csv(VALIDATED_PATH, index=False)

print("\nValidated dataset saved:")
print(VALIDATED_PATH)

# ------------------------------------------------------------
# 13. Save quality report
# ------------------------------------------------------------

REPORT_PATH = OUTPUT_DIR / "data_quality_report.csv"

quality_summary.to_csv(REPORT_PATH, index=False)

# Save suspicious records separately for investigation.

SUSPICIOUS_PATH = OUTPUT_DIR / "suspicious_shipping_records.csv"

suspicious_records = df[
    df["Shipping Duration Flag"] != "Within 30 Days"
]

suspicious_records.to_csv(SUSPICIOUS_PATH, index=False)

print("\n========== STEP 4 COMPLETED ==========\n")

print("Quality report:", REPORT_PATH)
print("Suspicious records:", SUSPICIOUS_PATH)
print("Validated dataset:", VALIDATED_PATH)
