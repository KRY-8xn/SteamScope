import csv
import glob
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

GAMES_FILE = "data/cleaned/games_cleaned.csv"
REVIEW_FILES = sorted(glob.glob("data/raw/reviews-*.csv"))

# ---------------------------------------------------------
# Load game AppIDs
# ---------------------------------------------------------

game_appids = set()

with open(
    GAMES_FILE,
    encoding="utf-8-sig",
    newline=""
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row["appid"]:
            game_appids.add(int(row["appid"]))


# ---------------------------------------------------------
# Find missing AppIDs and review counts
# ---------------------------------------------------------

missing_counts = Counter()

for file_path in REVIEW_FILES:
    print(f"Processing: {file_path}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            appid = int(row["appid"])

            if appid not in game_appids:
                missing_counts[appid] += 1


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("MISSING GAME APPID SUMMARY")
print("=" * 80)

print(f"Missing AppIDs: {len(missing_counts):,}")

print("\nTop 100 missing AppIDs:")
print("-" * 80)

for appid, count in missing_counts.most_common(100):
    print(f"AppID {appid:<10} | Reviews: {count:,}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"Unique missing AppIDs: {len(missing_counts):,}")
print(f"Total reviews affected: {sum(missing_counts.values()):,}")

print("\nAnalysis complete.")