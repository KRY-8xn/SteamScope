import csv
import glob
import sys
from collections import Counter


csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

total = 0

empty = 0
over_8000 = 0
over_10000 = 0
over_50000 = 0
over_100000 = 0

length_buckets = Counter()

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

            review = row["review"]

            if not review or not review.strip():
                empty += 1
                continue

            length = len(review)

            if length > 8000:
                over_8000 += 1

            if length > 10000:
                over_10000 += 1

            if length > 50000:
                over_50000 += 1

            if length > 100000:
                over_100000 += 1

            if length <= 100:
                length_buckets["0-100"] += 1
            elif length <= 500:
                length_buckets["101-500"] += 1
            elif length <= 1000:
                length_buckets["501-1000"] += 1
            elif length <= 2000:
                length_buckets["1001-2000"] += 1
            elif length <= 4000:
                length_buckets["2001-4000"] += 1
            elif length <= 8000:
                length_buckets["4001-8000"] += 1
            else:
                length_buckets["8000+"] += 1


print("\n" + "=" * 80)
print("REVIEW LENGTH ANALYSIS")
print("=" * 80)

print(f"Total reviews: {total:,}")
print(f"Empty reviews: {empty:,}")

print("\nLength thresholds:")
print(f"> 8,000 characters:   {over_8000:,}")
print(f"> 10,000 characters:  {over_10000:,}")
print(f"> 50,000 characters:  {over_50000:,}")
print(f"> 100,000 characters: {over_100000:,}")

print("\nLength distribution:")

for bucket, count in length_buckets.items():
    print(f"  {bucket:12} : {count:,}")

print("\nAnalysis complete.")