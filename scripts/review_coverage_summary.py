import csv
import glob
import sys

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
# Analyze review coverage
# ---------------------------------------------------------

total_reviews = 0
matched_reviews = 0
unmatched_reviews = 0

matched_appids = set()
unmatched_appids = set()

for file_path in REVIEW_FILES:
    print(f"Processing: {file_path}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_reviews += 1

            appid = int(row["appid"])

            if appid in game_appids:
                matched_reviews += 1
                matched_appids.add(appid)
            else:
                unmatched_reviews += 1
                unmatched_appids.add(appid)

# ---------------------------------------------------------
# Calculate percentages
# ---------------------------------------------------------

matched_percentage = (matched_reviews / total_reviews) * 100
unmatched_percentage = (unmatched_reviews / total_reviews) * 100

# ---------------------------------------------------------
# Output
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("REVIEW → GAME COVERAGE SUMMARY")
print("=" * 80)

print(f"Total reviews:              {total_reviews:,}")

print("\nReview records:")
print(f"  Matched to GAME:          {matched_reviews:,}")
print(f"  Unmatched:                 {unmatched_reviews:,}")
print(f"  Matched percentage:        {matched_percentage:.2f}%")
print(f"  Unmatched percentage:      {unmatched_percentage:.2f}%")

print("\nUnique AppIDs:")
print(f"  Game catalog AppIDs:       {len(game_appids):,}")
print(f"  Review AppIDs matched:     {len(matched_appids):,}")
print(f"  Review AppIDs unmatched:   {len(unmatched_appids):,}")

print("\nCoverage analysis complete.")