import csv

file_path = "data/raw/games.csv"

with open(file_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    header = next(reader)

    print("=" * 80)
    print("GAMES CSV - LAST FIELDS CHECK")
    print("=" * 80)

    print("\nHeader mapping:")
    for i in range(len(header) - 7, len(header)):
        print(f"{i + 1}: {header[i]!r}")

    print("\nFirst 10 data rows - last 7 fields:")

    for row_number, row in enumerate(reader, start=1):
        if row_number > 10:
            break

        print("\n" + "-" * 80)
        print(f"Row {row_number}")

        for i in range(len(row) - 7, len(row)):
            print(f"{i + 1}: {row[i]!r}")