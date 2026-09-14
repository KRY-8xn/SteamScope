import csv
import glob
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

REVIEW_FILES = sorted(
    glob.glob("data/raw/reviews-*.csv")
)

total = 0

invalid_steamid = 0
invalid_appid = 0
invalid_voted_up = 0

invalid_votes_up = 0
invalid_votes_funny = 0
invalid_weighted_score = 0
invalid_playtime_forever = 0
invalid_playtime_at_review = 0
invalid_num_games_owned = 0
invalid_num_reviews = 0

invalid_created_timestamp = 0
invalid_updated_timestamp = 0

negative_values = Counter()


def is_integer(value):
    try:
        int(value)
        return True
    except (ValueError, TypeError):
        return False


def is_float(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


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

            # SteamID
            steamid = row["steamid"]

            if not steamid or not is_integer(steamid):
                invalid_steamid += 1

            # AppID
            appid = row["appid"]

            if not appid or not is_integer(appid):
                invalid_appid += 1

            # voted_up
            voted_up = row["voted_up"].strip().lower()

            if voted_up not in {"true", "false"}:
                invalid_voted_up += 1

            # Integer fields
            integer_fields = {
                "votes_up": "votes_up",
                "votes_funny": "votes_funny",
                "playtime_forever": "playtime_forever",
                "playtime_at_review": "playtime_at_review",
                "num_games_owned": "num_games_owned",
                "num_reviews": "num_reviews",
                "unix_timestamp_created": "unix_timestamp_created",
                "unix_timestamp_updated": "unix_timestamp_updated",
            }

            for field, label in integer_fields.items():
                value = row[field]

                if not value or not is_integer(value):
                    if field == "votes_up":
                        invalid_votes_up += 1
                    elif field == "votes_funny":
                        invalid_votes_funny += 1
                    elif field == "playtime_forever":
                        invalid_playtime_forever += 1
                    elif field == "playtime_at_review":
                        invalid_playtime_at_review += 1
                    elif field == "num_games_owned":
                        invalid_num_games_owned += 1
                    elif field == "num_reviews":
                        invalid_num_reviews += 1
                    elif field == "unix_timestamp_created":
                        invalid_created_timestamp += 1
                    elif field == "unix_timestamp_updated":
                        invalid_updated_timestamp += 1
                else:
                    number = int(value)

                    if number < 0:
                        negative_values[field] += 1

            # Weighted vote score
            score = row["weighted_vote_score"]

            if not score or not is_float(score):
                invalid_weighted_score += 1
            else:
                score_value = float(score)

                if score_value < 0 or score_value > 1:
                    invalid_weighted_score += 1


print("\n" + "=" * 80)
print("REVIEW VALUE VALIDATION")
print("=" * 80)

print(f"Total review records: {total:,}")

print("\nInvalid values:")
print(f"  SteamID:                 {invalid_steamid:,}")
print(f"  AppID:                   {invalid_appid:,}")
print(f"  voted_up:                {invalid_voted_up:,}")
print(f"  votes_up:                {invalid_votes_up:,}")
print(f"  votes_funny:              {invalid_votes_funny:,}")
print(f"  weighted_vote_score:      {invalid_weighted_score:,}")
print(f"  playtime_forever:         {invalid_playtime_forever:,}")
print(f"  playtime_at_review:       {invalid_playtime_at_review:,}")
print(f"  num_games_owned:          {invalid_num_games_owned:,}")
print(f"  num_reviews:              {invalid_num_reviews:,}")
print(f"  created timestamp:        {invalid_created_timestamp:,}")
print(f"  updated timestamp:        {invalid_updated_timestamp:,}")

print("\nNegative values:")
if negative_values:
    for field, count in negative_values.items():
        print(f"  {field}: {count:,}")
else:
    print("  None")

print("\nValidation complete.")