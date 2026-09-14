import csv
import glob
import sys

csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

seen = set()
exact_duplicates = 0
total = 0

for file_path in REVIEW_FILES:
    print(f"Processing: {file_path}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1

            # Entire review record
            key = (
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

            if key in seen:
                exact_duplicates += 1
            else:
                seen.add(key)

print("\n" + "=" * 80)
print("EXACT REVIEW DUPLICATE ANALYSIS")
print("=" * 80)

print(f"Total review records:      {total:,}")
print(f"Exact duplicate records:   {exact_duplicates:,}")
print(f"Unique review records:     {total - exact_duplicates:,}")

print("\nAnalysis complete.")