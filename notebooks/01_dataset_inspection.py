
# ============================================================
# NASSAU CANDY SHIPPING ANALYTICS
# STEP 3: DATASET INSPECTION
# ============================================================

import pandas as pd
import os

# ------------------------------------------------------------
# 1. Define dataset path
# ------------------------------------------------------------

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "Nassau Candy Distributor.csv"
)

# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\n========== LOADING DATASET ==========\n")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")

# ------------------------------------------------------------
# 3. Dataset dimensions
# ------------------------------------------------------------

print("\n========== DATASET SHAPE ==========\n")

print("Number of Rows:", df.shape[0])
print("Number of Columns:", df.shape[1])

# ------------------------------------------------------------
# 4. Display column names
# ------------------------------------------------------------

print("\n========== COLUMN NAMES ==========\n")

for column in df.columns:
    print(column)

# ------------------------------------------------------------
# 5. Display first five records
# ------------------------------------------------------------

print("\n========== FIRST FIVE RECORDS ==========\n")

print(df.head())

# ------------------------------------------------------------
# 6. Display last five records
# ------------------------------------------------------------

print("\n========== LAST FIVE RECORDS ==========\n")

print(df.tail())

# ------------------------------------------------------------
# 7. Dataset information
# ------------------------------------------------------------

print("\n========== DATASET INFORMATION ==========\n")

df.info()

# ------------------------------------------------------------
# 8. Check data types
# ------------------------------------------------------------

print("\n========== DATA TYPES ==========\n")

print(df.dtypes)

# ------------------------------------------------------------
# 9. Check missing values
# ------------------------------------------------------------

print("\n========== MISSING VALUES ==========\n")

missing_values = df.isnull().sum()

print(missing_values)

print("\nTotal Missing Values:", missing_values.sum())

# ------------------------------------------------------------
# 10. Check duplicate records
# ------------------------------------------------------------

print("\n========== DUPLICATE RECORDS ==========\n")

duplicates = df.duplicated().sum()

print("Total Duplicate Rows:", duplicates)

# ------------------------------------------------------------
# 11. Statistical summary
# ------------------------------------------------------------

print("\n========== STATISTICAL SUMMARY ==========\n")

print(df.describe(include="all").T)

# ------------------------------------------------------------
# 12. Check date columns
# ------------------------------------------------------------

print("\n========== DATE COLUMN CANDIDATES ==========\n")

date_columns = [
    col for col in df.columns
    if "date" in col.lower()
]

print("Date Columns Found:", date_columns)

for column in date_columns:
    parsed_dates = pd.to_datetime(df[column], errors="coerce")

    print(f"\nColumn: {column}")
    print("Minimum Date:", parsed_dates.min())
    print("Maximum Date:", parsed_dates.max())
    print("Invalid/Unparsed Dates:", parsed_dates.isna().sum())

# ------------------------------------------------------------
# 13. Save inspection report
# ------------------------------------------------------------

os.makedirs(
    os.path.join(os.path.dirname(__file__), "..", "outputs"),
    exist_ok=True
)

report_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "outputs",
    "dataset_inspection.txt"
)

with open(report_path, "w", encoding="utf-8") as file:

    file.write("NASSAU CANDY DATASET INSPECTION REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Rows: {df.shape[0]}\n")
    file.write(f"Columns: {df.shape[1]}\n\n")

    file.write("COLUMN NAMES:\n")
    file.write(str(df.columns.tolist()) + "\n\n")

    file.write("MISSING VALUES:\n")
    file.write(str(missing_values) + "\n\n")

    file.write(f"Duplicate Rows: {duplicates}\n\n")

    file.write("DATA TYPES:\n")
    file.write(str(df.dtypes) + "\n\n")

    file.write("STATISTICAL SUMMARY:\n")
    file.write(df.describe(include="all").T.to_string())

print("\n========== INSPECTION COMPLETED ==========\n")

print("Inspection report saved in outputs/dataset_inspection.txt")
