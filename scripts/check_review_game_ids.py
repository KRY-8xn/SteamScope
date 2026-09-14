import csv
import glob
import sys

csv.field_size_limit(sys.maxsize)

GAMES_FILE = "data/cleaned/games_cleaned.csv"

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

# Load valid AppIDs from the cleaned games dataset
game_appids = set()

print(f"Loading game AppIDs from: {GAMES_FILE}")

with open(
    GAMES_FILE,
    encoding="utf-8-sig",
    newline=""
) as f:
    reader = csv.DictReader(f)

    for row in reader:
        appid = row["appid"]

        if appid:
            game_appids.add(int(appid))

print(f"Game AppIDs loaded: {len(game_appids):,}")

# Check review AppIDs
total_reviews = 0
unique_review_appids = set()
missing_appids = set()

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
            unique_review_appids.add(appid)

            if appid not in game_appids:
                missing_appids.add(appid)

print("\n" + "=" * 80)
print("REVIEW → GAME APPID VALIDATION")
print("=" * 80)

print(f"Total review records:       {total_reviews:,}")
print(f"Unique review AppIDs:       {len(unique_review_appids):,}")
print(f"Game AppIDs:                {len(game_appids):,}")
print(f"Missing review AppIDs:      {len(missing_appids):,}")

if missing_appids:
    print("\nSample missing AppIDs:")

    for appid in sorted(missing_appids)[:50]:
        print(f"  {appid}")

    print("\nThese review records cannot directly reference GAME")
    print("through a foreign key until we decide how to handle them.")
else:
    print("\nExcellent! Every review AppID exists in the games dataset.")
    print("The REVIEW → GAME foreign-key relationship is consistent.")

print("\nValidation complete.")