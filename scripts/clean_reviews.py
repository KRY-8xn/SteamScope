import csv
import glob
import sys

csv.field_size_limit(sys.maxsize)

GAMES_FILE = "data/cleaned/games_cleaned.csv"

OUTPUT_FILE = "data/cleaned/reviews_cleaned.csv"
UNMATCHED_FILE = "data/cleaned/reviews_unmatched.csv"

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

MAX_REVIEW_LENGTH = 8000

# ---------------------------------------------------------
# Load valid GAME AppIDs
# ---------------------------------------------------------

print("Loading GAME AppIDs...")

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

print(f"Valid GAME AppIDs: {len(game_appids):,}")


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

total = 0
cleaned = 0
empty_reviews = 0
long_reviews = 0
exact_duplicates = 0
unmatched_appids = 0

seen = set()


# ---------------------------------------------------------
# Process review files
# ---------------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as clean_file, open(
    UNMATCHED_FILE,
    "w",
    encoding="utf-8",
    newline=""
) as unmatched_file:

    clean_writer = None
    unmatched_writer = None

    for file_path in REVIEW_FILES:

        print(f"Processing: {file_path}")

        with open(
            file_path,
            encoding="utf-8-sig",
            newline=""
        ) as f:

            reader = csv.DictReader(f)

            # Create output headers once
            if clean_writer is None:
                clean_writer = csv.DictWriter(
                    clean_file,
                    fieldnames=reader.fieldnames
                )
                clean_writer.writeheader()

                unmatched_writer = csv.DictWriter(
                    unmatched_file,
                    fieldnames=reader.fieldnames
                )
                unmatched_writer.writeheader()

            for row in reader:

                total += 1

                review = row["review"]

                # -------------------------------------------------
                # Rule 1: Remove empty reviews
                # -------------------------------------------------

                if not review or not review.strip():
                    empty_reviews += 1
                    continue

                # -------------------------------------------------
                # Rule 2: Remove extreme review text
                # -------------------------------------------------

                if len(review) > MAX_REVIEW_LENGTH:
                    long_reviews += 1
                    continue

                # -------------------------------------------------
                # Rule 3: Remove exact duplicate records
                # -------------------------------------------------

                duplicate_key = (
                    row["steamid"],
                    row["appid"],
                    row["voted_up"],
                    row["votes_up"],
                    row["votes_funny"],
                    row["weighted_vote_score"],
                    row["playtime_forever"],
                    row["playtime_at_review"],
                    row["num_games_owned"],
                    row["num_reviews"],
                    row["review"],
                    row["unix_timestamp_created"],
                    row["unix_timestamp_updated"],
                )

                if duplicate_key in seen:
                    exact_duplicates += 1
                    continue

                seen.add(duplicate_key)

                # -------------------------------------------------
                # Rule 4: Check GAME relationship
                # -------------------------------------------------

                appid = int(row["appid"])

                if appid not in game_appids:
                    unmatched_appids += 1
                    unmatched_writer.writerow(row)
                    continue

                # -------------------------------------------------
                # Valid cleaned review
                # -------------------------------------------------

                clean_writer.writerow(row)
                cleaned += 1


# ---------------------------------------------------------
# Final report
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("REVIEW CLEANING COMPLETE")
print("=" * 80)

print(f"Raw review records:          {total:,}")

print("\nRemoved:")
print(f"  Empty reviews:             {empty_reviews:,}")
print(f"  > 8,000 characters:        {long_reviews:,}")
print(f"  Exact duplicates:          {exact_duplicates:,}")
print(f"  Unmatched AppIDs:          {unmatched_appids:,}")

print("\nOutput:")
print(f"  Cleaned reviews:           {cleaned:,}")
print(f"  Unmatched reviews:         {unmatched_appids:,}")

print("\nFiles created:")
print(f"  {OUTPUT_FILE}")
print(f"  {UNMATCHED_FILE}")

print("\nValidation:")
print(
    f"  Removed + cleaned = "
    f"{empty_reviews + long_reviews + exact_duplicates + unmatched_appids + cleaned:,}"
)

print(f"  Original total     = {total:,}")

if (
    empty_reviews
    + long_reviews
    + exact_duplicates
    + unmatched_appids
    + cleaned
    == total
):
    print("  ✓ Record accounting is correct.")
else:
    print("  ✗ WARNING: Record accounting mismatch!")

print("\nCleaning complete.")