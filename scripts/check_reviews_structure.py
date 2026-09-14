import csv
import glob
import os
import sys
from collections import Counter


# Allow very large review-text fields
csv.field_size_limit(sys.maxsize)


REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)


print("=" * 80)
print("STEAMSCOPE - REVIEWS DATASET STRUCTURE CHECK")
print("=" * 80)

print(f"\nReview files found: {len(REVIEW_FILES)}")

total_records = 0

expected_columns = None

for file_path in REVIEW_FILES:

    print("\n" + "-" * 80)
    print(f"File: {os.path.basename(file_path)}")

    field_counts = Counter()
    record_count = 0

    try:
        with open(
            file_path,
            encoding="utf-8-sig",
            newline=""
        ) as f:

            reader = csv.reader(f)

            header = next(reader)

            print(f"Columns: {len(header)}")

            if expected_columns is None:
                expected_columns = header

            for row in reader:

                record_count += 1
                field_counts[len(row)] += 1

    except Exception as e:

        print("\nERROR while reading this file!")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        print(f"Records successfully read before error: {record_count:,}")

        total_records += record_count

        print("\nStopping validation so we can inspect this file.")

        break

    total_records += record_count

    print(f"Actual CSV records: {record_count:,}")
    print(f"Field-count distribution: {dict(field_counts)}")

    if set(field_counts.keys()) == {len(header)}:
        print("Structure: OK")
    else:
        print("WARNING: Inconsistent field counts detected!")


print("\n" + "=" * 80)
print("REVIEW DATASET SUMMARY")
print("=" * 80)

print(f"Total records successfully checked: {total_records:,}")

if expected_columns:
    print(f"Columns: {len(expected_columns)}")

    print("\nColumn names:")

    for i, column in enumerate(expected_columns, start=1):
        print(f"  {i}: {column}")

print("\nValidation complete.")