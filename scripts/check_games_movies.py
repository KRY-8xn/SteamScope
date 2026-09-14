import csv

file_path = "data/raw/games.csv"

with open(file_path, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)

    header = next(reader)

    print("=" * 80)
    print("GAMES CSV - SCREENSHOTS / MOVIES CHECK")
    print("=" * 80)

    found = 0

    for row_number, row in enumerate(reader, start=1):

        last_fields = row[37:40]

        combined = " ".join(last_fields).lower()

        if ".mp4" in combined or ".webm" in combined:
            print("\n" + "-" * 80)
            print(f"Row: {row_number}")

            for i in range(37, 40):
                print(f"{i + 1}: {row[i]!r}")

            found += 1

            if found >= 5:
                break

    print("\n" + "=" * 80)
    print(f"Movie-containing rows found: {found}")
    print("=" * 80)