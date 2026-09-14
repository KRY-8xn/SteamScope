import pandas as pd

FILE = "data/cleaned/games_cleaned.csv"

df = pd.read_csv(FILE)

print("=" * 80)
print("STEAMSCOPE - MISSING GAME NAME CHECK")
print("=" * 80)

missing_name = df[df["name"].isna()]

print(f"\nGames with missing name: {len(missing_name)}")

if len(missing_name) > 0:
    print("\nDetails:")
    print(
        missing_name[
            [
                "appid",
                "name",
                "release_date",
                "estimated_owners",
                "peak_ccu",
                "price",
                "developers",
                "publishers",
                "genres",
                "tags",
            ]
        ].to_string(index=False)
    )

print("\n" + "=" * 80)
print("DATASET VALIDATION")
print("=" * 80)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Unique AppIDs: {df['appid'].nunique():,}")
print(f"Missing AppIDs: {df['appid'].isna().sum():,}")
print(f"Missing Names: {df['name'].isna().sum():,}")

print("\nValidation complete.")