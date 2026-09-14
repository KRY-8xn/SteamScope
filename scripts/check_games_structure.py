import csv
from collections import Counter

file_path = "data/raw/games.csv"

with open(file_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    header = next(reader)

    counts = Counter()
    examples = {}

    total_rows = 0

    for row in reader:
        total_rows += 1
        field_count = len(row)

        counts[field_count] += 1

        if field_count not in examples:
            examples[field_count] = row

print("=" * 80)
print("GAMES CSV STRUCTURE CHECK")
print("=" * 80)

print(f"Expected fields from header: {len(header)}")
print(f"Total data rows: {total_rows:,}")

print("\nField-count distribution:")

for field_count, row_count in sorted(counts.items()):
    print(f"  {field_count} fields : {row_count:,} rows")

print("\nExample row for each field count:")

for field_count, row in sorted(examples.items()):
    print("\n" + "-" * 80)
    print(f"Fields: {field_count}")

    print("First 10 fields:")
    for i, value in enumerate(row[:10], start=1):
        print(f"  {i}: {value!r}")

    print("Last 5 fields:")
    start = max(0, len(row) - 5)

    for i in range(start, len(row)):
        print(f"  {i + 1}: {row[i]!r}")