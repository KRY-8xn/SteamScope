import csv
import os
import pandas as pd


RAW_FILE = "data/raw/games.csv"
OUTPUT_FILE = "data/cleaned/games_cleaned.csv"


print("=" * 80)
print("STEAMSCOPE - GAMES DATA CLEANING")
print("=" * 80)


# -------------------------------------------------------------------
# 1. Read raw CSV
# -------------------------------------------------------------------

print("\n[1/7] Reading raw dataset...")

rows = []

with open(RAW_FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    header = next(reader)

    for row in reader:
        # Every raw row has one extra empty field at the end.
        row = row[:len(header)]
        rows.append(row)

print(f"Raw rows read: {len(rows):,}")
print(f"Columns: {len(header)}")


# -------------------------------------------------------------------
# 2. Create DataFrame
# -------------------------------------------------------------------

print("\n[2/7] Creating DataFrame...")

df = pd.DataFrame(rows, columns=header)

print(f"DataFrame shape: {df.shape}")


# -------------------------------------------------------------------
# 3. Normalize column names
# -------------------------------------------------------------------

print("\n[3/7] Normalizing column names...")

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("Column names normalized.")


# -------------------------------------------------------------------
# 4. Convert empty strings to missing values
# -------------------------------------------------------------------

print("\n[4/7] Handling empty values...")

df = df.replace(r"^\s*$", pd.NA, regex=True)

print("Empty strings converted to NULL-compatible values.")

# Remove records with missing mandatory game name
missing_name_count = df["name"].isna().sum()

if missing_name_count > 0:
    print(f"Removing {missing_name_count} row(s) with missing game name.")
    df = df[df["name"].notna()].copy()
# -------------------------------------------------------------------
# 5. Convert data types
# -------------------------------------------------------------------

print("\n[5/7] Converting data types...")

numeric_columns = [
    "appid",
    "peak_ccu",
    "required_age",
    "price",
    "discountdlc_count",
    "metacritic_score",
    "user_score",
    "positive",
    "negative",
    "score_rank",
    "achievements",
    "recommendations",
    "average_playtimeforever",
    "average_playtime_two_weeks",
    "median_playtime_forever",
    "median_playtime_two_weeks",
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


boolean_columns = [
    "windows",
    "mac",
    "linux",
]

for column in boolean_columns:
    if column in df.columns:
        df[column] = df[column].map({
            "True": True,
            "False": False,
            "true": True,
            "false": False,
        })


# Release date
if "release_date" in df.columns:
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    ).dt.date


# -------------------------------------------------------------------
# 6. Check duplicate AppIDs
# -------------------------------------------------------------------

print("\n[6/7] Checking duplicate AppIDs...")

duplicate_appids = df["appid"].duplicated().sum()

print(f"Duplicate AppIDs: {duplicate_appids:,}")

if duplicate_appids > 0:
    print("WARNING: Duplicate AppIDs found.")
else:
    print("No duplicate AppIDs found.")


# -------------------------------------------------------------------
# 7. Save cleaned dataset
# -------------------------------------------------------------------

print("\n[7/7] Saving cleaned dataset...")

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print(f"Saved to: {OUTPUT_FILE}")


# -------------------------------------------------------------------
# Cleaning summary
# -------------------------------------------------------------------

print("\n" + "=" * 80)
print("CLEANING SUMMARY")
print("=" * 80)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Duplicate AppIDs: {duplicate_appids:,}")

print("\nMissing values in important columns:")

important_columns = [
    "appid",
    "name",
    "release_date",
    "developers",
    "publishers",
    "genres",
    "tags",
]

for column in important_columns:
    if column in df.columns:
        missing = df[column].isna().sum()
        print(f"  {column}: {missing:,}")

print("\nCleaning completed.")