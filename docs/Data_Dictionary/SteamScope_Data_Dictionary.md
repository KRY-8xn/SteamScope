# SteamScope – Data Dictionary

## Source files examined

| Source | Rows | Columns | Status |
|---|---:|---:|---|
| `games_dataset_first200.xlsx` | 199 | 39 | Requires substantial validation/cleaning |
| `games_reviews_first30.xlsx` | 37 | 13 | Structurally clean sample |

## A. Games dataset

### Fields proposed for the normalized GAME entity

| Source column | Proposed target | Decision | Notes |
|---|---|---|---|
| AppID | GAME.AppID | KEEP | 199/199 non-null and unique in sample |
| Name | GAME.Name | KEEP | 199/199 non-null and unique |
| Release date | GAME.ReleaseDate | TRANSFORM | Convert valid source dates to DATE; 189 unique values |
| Estimated owners | GAME.EstimatedOwners | KEEP/VALIDATE | Categorical range; 8 distinct values |
| Peak CCU | GAME.PeakCCU | KEEP | Numeric |
| Required age | GAME.RequiredAge | KEEP/VALIDATE | Numeric; inspect source semantics |
| Price | GAME.Price | KEEP/VALIDATE | Numeric price; validate currency/source meaning |
| DiscountDLC count | GAME.DiscountDLCCount | VALIDATE | Keep only after confirming source meaning |
| About the game | GAME.Description | INVESTIGATE | Sample profiling suggests this column is not consistently aligned with its apparent name |
| Website | GAME.Website | INVESTIGATE | Sample contains values that appear to be Steam header-image URLs |
| Support url | GAME.SupportURL | KEEP/VALIDATE | 81 non-null in sample |
| Support email | GAME.SupportEmail | KEEP/VALIDATE | 89 non-null; inspect for shifted values |
| Metacritic score | GAME.MetacriticScore | INVESTIGATE | Loaded as BOOLEAN in pandas, so source mapping is suspicious |
| User score | GAME.UserScore | TRANSFORM/VALIDATE | Only 10 non-null in sample |
| Positive | GAME.PositiveReviews | INVESTIGATE | All 199 values are 0 in sample |
| Negative | GAME.NegativeReviews | INVESTIGATE | Numeric but source alignment must be verified |
| Score rank | GAME.ScoreRank | INVESTIGATE | Numeric; validate meaning |
| Recommendations | GAME.Recommendations | KEEP/VALIDATE | Numeric |
| Average playtime forever | GAME.AveragePlaytimeForever | INVESTIGATE | Loaded as object with only 36 non-null; some values appear unrelated to playtime |
| Average playtime two weeks | GAME.AveragePlaytimeTwoWeeks | KEEP/VALIDATE | Numeric |
| Median playtime forever | GAME.MedianPlaytimeForever | KEEP/VALIDATE | Numeric but only 3 distinct values; validate |
| Median playtime two weeks | GAME.MedianPlaytimeTwoWeeks | KEEP/VALIDATE | Numeric |

### Source fields that should not be directly imported into GAME

| Source column | Action | Reason |
|---|---|---|
| Developers | SPLIT/NORMALIZE | Multi-valued relationship → DEVELOPER + GAME_DEVELOPER |
| Publishers | SPLIT/NORMALIZE | Multi-valued relationship → PUBLISHER + GAME_PUBLISHER |
| Genres | SPLIT/NORMALIZE | Multi-valued relationship → GENRE + GAME_GENRE |
| Tags | SPLIT/NORMALIZE | Multi-valued relationship → TAG + GAME_TAG |
| Categories | SPLIT/NORMALIZE | Multi-valued relationship → CATEGORY + GAME_CATEGORY |
| Windows/Mac/Linux | TRANSFORM | Map platform availability to PLATFORM + GAME_PLATFORM after validating source columns |
| Supported languages | SPLIT/NORMALIZE | → LANGUAGE + GAME_LANGUAGE |
| Full audio languages | SPLIT/NORMALIZE | → LANGUAGE + GAME_LANGUAGE with LanguageType=AUDIO |
| Screenshots | SPLIT/NORMALIZE | → GAME_SCREENSHOT |
| Movies | SPLIT/NORMALIZE | → GAME_MOVIE |
| Header image | INVESTIGATE | Appears inconsistent with apparent source schema |
| Reviews | DO NOT TREAT AS REVIEW RECORDS | This field is not the actual review dataset |
| Achievements | DO NOT LOAD FROM THIS FIELD | Sample is entirely empty |
| Notes | INVESTIGATE | Meaning and alignment require validation |

## B. Reviews dataset

| Source column | Target | Decision | Notes |
|---|---|---|---|
| steamid | USER.SteamID / source identifier | KEEP AS EXTERNAL ID | 64-bit-sized numeric identifier; do not use INT |
| appid | REVIEW.AppID | KEEP | Game FK after coverage validation |
| voted_up | REVIEW.VotedUp | KEEP | Boolean |
| votes_up | REVIEW.VotesUp | KEEP | Integer |
| votes_funny | REVIEW.VotesFunny | KEEP | Integer |
| weighted_vote_score | REVIEW.WeightedVoteScore | KEEP | Numeric |
| playtime_forever | REVIEW.PlaytimeForever | KEEP | Integer |
| playtime_at_review | REVIEW.PlaytimeAtReview | KEEP | Integer |
| num_games_owned | REVIEW.NumGamesOwned | KEEP | Integer |
| num_reviews | REVIEW.NumReviews | KEEP | Integer |
| review | REVIEW.ReviewText | KEEP | Text |
| unix_timestamp_created | REVIEW.CreatedAt | TRANSFORM | Convert Unix timestamp to DATETIME |
| unix_timestamp_updated | REVIEW.UpdatedAt | TRANSFORM | Convert Unix timestamp to DATETIME |

### Review sample validation results

- 37 rows
- 13 columns
- No missing values in the sample
- No duplicate complete rows
- 37 unique `steamid` values
- 1 distinct `appid` value (`10`)
- No duplicate `(steamid, appid)` pairs in the sample
- The sample's `appid=10` does not overlap with the 199-game sample's AppIDs, so the two samples cannot currently be joined by AppID. This is expected for small samples and must be rechecked against the larger source datasets before import.

## C. Important source-data warning

The games sample contains several type/cardinality patterns that conflict with the apparent column names, including:

- `About the game` loaded as integer
- `Metacritic score` loaded as boolean
- `Developers` loaded as integer with only 3 distinct values
- `Average playtime forever` loaded as object and sparsely populated
- `Positive` is all zero in the sample
- `Mac` is TRUE for every sampled row
- `Website` values appear to include Steam header-image URLs

Therefore, the project must use a **staging + validation + transformation** process rather than directly importing the spreadsheet into the normalized schema.
