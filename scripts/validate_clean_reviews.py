import csv
import sys

csv.field_size_limit(sys.maxsize)

CLEAN_REVIEWS = "data/cleaned/reviews_cleaned.csv"
GAMES_FILE = "data/cleaned/games_cleaned.csv"

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

print(f"GAME AppIDs loaded: {len(game_appids):,}")


# ---------------------------------------------------------
# Validate cleaned reviews
# ---------------------------------------------------------

total = 0
empty_reviews = 0
long_reviews = 0
invalid_appids = 0
missing_game_appids = set()
duplicate_records = 0

seen = set()

expected_columns = [
    "steamid",
    "appid",
    "voted_up",
    "votes_up",
    "votes_funny",
    "weighted_vote_score",
    "playtime_forever",
    "playtime_at_review",
    "num_games_owned",
    "num_reviews",
    "review",
    "unix_timestamp_created",
    "unix_timestamp_updated",
]


with open(
    CLEAN_REVIEWS,
    encoding="utf-8-sig",
    newline=""
) as f:

    reader = csv.DictReader(f)

    # -----------------------------------------------------
    # Check column structure
    # -----------------------------------------------------

    if reader.fieldnames != expected_columns:
        print("\nWARNING: Column structure does not match expected structure.")
        print("Actual columns:")
        print(reader.fieldnames)
    else:
        print("Column structure: OK")

    # -----------------------------------------------------
    # Process records
    # -----------------------------------------------------

    for row in reader:

        total += 1

        # Empty review
        review = row["review"]

        if not review or not review.strip():
            empty_reviews += 1

        # Review length
        if review and len(review) > 8000:
            long_reviews += 1

        # AppID validity
        try:
            appid = int(row["appid"])
        except (ValueError, TypeError):
            invalid_appids += 1
            continue

        # GAME relationship
        if appid not in game_appids:
            missing_game_appids.add(appid)

        # Exact duplicate
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
            duplicate_records += 1
        else:
            seen.add(duplicate_key)


# ---------------------------------------------------------
# Final report
# ---------------------------------------------------------

print("\n" + "=" * 80)
print("CLEANED REVIEW VALIDATION")
print("=" * 80)

print(f"Cleaned review records:       {total:,}")

print("\nQuality checks:")
print(f"  Empty reviews:               {empty_reviews:,}")
print(f"  > 8,000 characters:          {long_reviews:,}")
print(f"  Invalid AppIDs:              {invalid_appids:,}")
print(f"  AppIDs missing from GAME:    {len(missing_game_appids):,}")
print(f"  Exact duplicate records:     {duplicate_records:,}")

print("\nExpected:")
print("  Empty reviews:               0")
print("  > 8,000 characters:          0")
print("  Invalid AppIDs:              0")
print("  Missing GAME AppIDs:         0")
print("  Exact duplicates:            0")

print("\n" + "=" * 80)

if (
    total == 15043047
    and empty_reviews == 0
    and long_reviews == 0
    and invalid_appids == 0
    and len(missing_game_appids) == 0
    and duplicate_records == 0
):
    print("✓ ALL CLEANED REVIEW VALIDATION CHECKS PASSED")
else:
    print("⚠ SOME VALIDATION CHECKS FAILED")

print("=" * 80)