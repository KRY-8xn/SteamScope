import csv
import glob
import os
import sys
from collections import Counter


csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

print("=" * 80)
print("STEAMSCOPE - REVIEWS DATA PROFILING")
print("=" * 80)

total_records = 0

missing_review = 0
missing_appid = 0
missing_steamid = 0

voted_up_values = Counter()

invalid_appid = 0
invalid_steamid = 0

min_playtime = None
max_playtime = None

min_weighted_score = None
max_weighted_score = None

review_length_min = None
review_length_max = None
review_length_total = 0

duplicate_check = set()
duplicate_count = 0

for file_path in REVIEW_FILES:

    print(f"\nProcessing: {os.path.basename(file_path)}")

    with open(
        file_path,
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        file_records = 0

        for row in reader:

            file_records += 1
            total_records += 1

            # -------------------------------------------------------
            # Missing values
            # -------------------------------------------------------

            steamid = row["steamid"].strip()
            appid = row["appid"].strip()
            review = row["review"]

            if not steamid:
                missing_steamid += 1

            if not appid:
                missing_appid += 1

            if not review or not review.strip():
                missing_review += 1

            # -------------------------------------------------------
            # voted_up values
            # -------------------------------------------------------

            voted_up_values[row["voted_up"].strip()] += 1

            # -------------------------------------------------------
            # Numeric validation
            # -------------------------------------------------------

            try:
                appid_value = int(appid)

                if appid_value <= 0:
                    invalid_appid += 1

            except ValueError:
                invalid_appid += 1

            try:
                steamid_value = int(steamid)

                if steamid_value <= 0:
                    invalid_steamid += 1

            except ValueError:
                invalid_steamid += 1

            # -------------------------------------------------------
            # Playtime
            # -------------------------------------------------------

            try:
                playtime = int(row["playtime_forever"])

                if min_playtime is None or playtime < min_playtime:
                    min_playtime = playtime

                if max_playtime is None or playtime > max_playtime:
                    max_playtime = playtime

            except ValueError:
                pass

            # -------------------------------------------------------
            # Weighted vote score
            # -------------------------------------------------------

            try:
                score = float(row["weighted_vote_score"])

                if min_weighted_score is None or score < min_weighted_score:
                    min_weighted_score = score

                if max_weighted_score is None or score > max_weighted_score:
                    max_weighted_score = score

            except ValueError:
                pass

            # -------------------------------------------------------
            # Review length
            # -------------------------------------------------------

            if review:
                length = len(review)

                review_length_total += length

                if review_length_min is None or length < review_length_min:
                    review_length_min = length

                if review_length_max is None or length > review_length_max:
                    review_length_max = length

            # -------------------------------------------------------
            # Duplicate check
            #
            # We use the combination of steamid + appid + review
            # rather than storing the entire 15M rows.
            # -------------------------------------------------------

            duplicate_key = (
                steamid,
                appid,
                review
            )

            if duplicate_key in duplicate_check:
                duplicate_count += 1
            else:
                duplicate_check.add(duplicate_key)

        print(f"Records processed: {file_records:,}")


average_review_length = (
    review_length_total / total_records
    if total_records
    else 0
)


print("\n" + "=" * 80)
print("REVIEWS PROFILING SUMMARY")
print("=" * 80)

print(f"Total records: {total_records:,}")

print("\nMissing values:")
print(f"  steamid: {missing_steamid:,}")
print(f"  appid: {missing_appid:,}")
print(f"  review: {missing_review:,}")

print("\nvoted_up values:")
for value, count in voted_up_values.items():
    print(f"  {value!r}: {count:,}")

print("\nInvalid numeric identifiers:")
print(f"  Invalid AppID: {invalid_appid:,}")
print(f"  Invalid SteamID: {invalid_steamid:,}")

print("\nPlaytime:")
print(f"  Minimum: {min_playtime}")
print(f"  Maximum: {max_playtime}")

print("\nWeighted vote score:")
print(f"  Minimum: {min_weighted_score}")
print(f"  Maximum: {max_weighted_score}")

print("\nReview text length:")
print(f"  Minimum: {review_length_min}")
print(f"  Maximum: {review_length_max}")
print(f"  Average: {average_review_length:.2f}")

print("\nDuplicate review records:")
print(f"  {duplicate_count:,}")

print("\n" + "=" * 80)
print("Profiling complete.")
print("=" * 80)