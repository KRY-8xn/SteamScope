import csv
import glob
import os
import sys
import heapq


csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

# Keep only the 10 longest reviews
longest_reviews = []

for file_path in REVIEW_FILES:

    print(f"Scanning: {os.path.basename(file_path)}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        for row in reader:

            review = row["review"]

            if not review:
                continue

            length = len(review)

            item = (
                length,
                row["steamid"],
                row["appid"],
                review
            )

            if len(longest_reviews) < 10:
                heapq.heappush(longest_reviews, item)

            elif length > longest_reviews[0][0]:
                heapq.heapreplace(longest_reviews, item)


longest_reviews.sort(reverse=True)

print("\n" + "=" * 80)
print("10 LONGEST REVIEWS")
print("=" * 80)

for rank, item in enumerate(longest_reviews, start=1):

    length, steamid, appid, review = item

    print("\n" + "-" * 80)
    print(f"Rank: {rank}")
    print(f"AppID: {appid}")
    print(f"SteamID: {steamid}")
    print(f"Review length: {length:,} characters")

    # Don't print millions of characters.
    preview = review[:500].replace("\n", "\\n")

    print(f"Preview: {preview!r}")