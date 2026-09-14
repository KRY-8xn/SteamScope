import csv
import glob
import sys
from collections import defaultdict

csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

# Store only the suspected duplicate keys.
# We will keep a small sample of records for inspection.
seen = {}
duplicates = []

for file_path in REVIEW_FILES:
    print(f"Processing: {file_path}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            key = (
                row["steamid"],
                row["appid"],
                row["review"]
            )

            if key in seen:
                duplicates.append({
                    "steamid": row["steamid"],
                    "appid": row["appid"],
                    "review": row["review"],
                    "first_file": seen[key]["file"],
                    "second_file": file_path,
                    "first_timestamp_created": seen[key]["timestamp_created"],
                    "second_timestamp_created": row["unix_timestamp_created"],
                    "first_timestamp_updated": seen[key]["timestamp_updated"],
                    "second_timestamp_updated": row["unix_timestamp_updated"],
                    "first_votes_up": seen[key]["votes_up"],
                    "second_votes_up": row["votes_up"],
                    "first_votes_funny": seen[key]["votes_funny"],
                    "second_votes_funny": row["votes_funny"],
                    "first_playtime": seen[key]["playtime_forever"],
                    "second_playtime": row["playtime_forever"],
                })

                # We only need a manageable sample.
                if len(duplicates) >= 20:
                    break

            else:
                seen[key] = {
                    "file": file_path,
                    "timestamp_created": row["unix_timestamp_created"],
                    "timestamp_updated": row["unix_timestamp_updated"],
                    "votes_up": row["votes_up"],
                    "votes_funny": row["votes_funny"],
                    "playtime_forever": row["playtime_forever"],
                }

        if len(duplicates) >= 20:
            break


print("\n" + "=" * 100)
print("SAMPLE OF SUSPECTED DUPLICATE REVIEWS")
print("=" * 100)

for i, d in enumerate(duplicates, start=1):
    print(f"\nDuplicate #{i}")
    print("-" * 60)
    print(f"SteamID: {d['steamid']}")
    print(f"AppID: {d['appid']}")

    review = d["review"].replace("\n", " ")
    print(f"Review: {review[:300]}")

    print("\nFirst record:")
    print(f"  File:              {d['first_file']}")
    print(f"  Created timestamp: {d['first_timestamp_created']}")
    print(f"  Updated timestamp: {d['first_timestamp_updated']}")
    print(f"  Votes up:          {d['first_votes_up']}")
    print(f"  Votes funny:       {d['first_votes_funny']}")
    print(f"  Playtime:          {d['first_playtime']}")

    print("\nSecond record:")
    print(f"  File:              {d['second_file']}")
    print(f"  Created timestamp: {d['second_timestamp_created']}")
    print(f"  Updated timestamp: {d['second_timestamp_updated']}")
    print(f"  Votes up:          {d['second_votes_up']}")
    print(f"  Votes funny:       {d['second_votes_funny']}")
    print(f"  Playtime:          {d['second_playtime']}")

print("\n" + "=" * 100)
print(f"Displayed suspected duplicates: {len(duplicates)}")
print("=" * 100)