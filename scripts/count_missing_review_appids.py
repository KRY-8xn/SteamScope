import csv
import glob
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

GAMES_FILE = "data/cleaned/games_cleaned.csv"
REVIEW_FILES = sorted(glob.glob("data/raw/reviews-*.csv"))

# Load valid game AppIDs
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

missing_counts = Counter()
total_missing_reviews = 0

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
                total_missing_reviews += 1

print("\n" + "=" * 80)
print("MISSING REVIEW APPID ANALYSIS")
print("=" * 80)

print(f"Missing AppIDs:              {len(missing_counts):,}")
print(f"Reviews using missing IDs:   {total_missing_reviews:,}")

print("\nTop 50 missing AppIDs by review count:")
print("-" * 50)

for appid, count in missing_counts.most_common(50):
    print(f"AppID {appid:<10} → {count:,} reviews")

print("\nAnalysis complete.")