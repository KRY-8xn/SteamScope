# SteamScope – Data Cleaning & Transformation Plan

## 1. Pipeline

Raw Excel/CSV
→ Raw/staging representation
→ Profile and validate
→ Clean/transform with Python + Pandas
→ Export normalized intermediate files
→ Load into MySQL

The original source files should remain unchanged.

## 2. Games cleaning rules

1. Preserve `AppID` as the source game identifier and verify uniqueness.
2. Trim whitespace from text fields.
3. Normalize missing markers such as empty strings, `NaN`, and placeholder values to NULL where appropriate.
4. Parse `Release date` into a consistent DATE representation; invalid dates go to a validation report.
5. Validate numeric fields such as price, CCU, age, recommendations, and playtime.
6. Investigate suspicious column mappings before accepting values. Do not repair by simply shifting every column globally.
7. Parse multi-valued developers, publishers, genres, tags, categories, and languages into individual values.
8. Deduplicate reference values case-insensitively where appropriate while preserving a canonical display form.
9. Convert Windows/Mac/Linux availability into platform relationships only after verifying the source column semantics.
10. Split screenshot and movie URL collections into separate rows.
11. Exclude the empty `Achievements` source field from achievement loading unless a separate public achievement source is obtained.
12. Keep a rejected/uncertain-record report for fields that cannot be reliably interpreted.
13. Validate URLs and emails before loading, but do not silently discard values merely because they are unusual.
14. Do not invent missing developer, publisher, review, or achievement data.

## 3. Reviews cleaning rules

1. Preserve the original `steamid` as an external/public identifier.
2. Verify `appid` values against the cleaned GAME AppID set before creating REVIEW foreign-key rows.
3. Convert Unix timestamps to DATETIME.
4. Preserve review text as text; do not split it.
5. Validate boolean `voted_up`.
6. Validate non-negative vote counts and playtime values.
7. Check duplicate reviews using available source identifiers/field combinations.
8. Keep the original review dataset unchanged and produce a cleaned derivative.
9. Do not interpret the public reviewer identifier as proof of private Steam account access.

## 4. Normalization mapping

| Raw concept | Normalized target |
|---|---|
| Game record | GAME |
| Developer list | DEVELOPER + GAME_DEVELOPER |
| Publisher list | PUBLISHER + GAME_PUBLISHER |
| Genre list | GENRE + GAME_GENRE |
| Tag list | TAG + GAME_TAG |
| Category list | CATEGORY + GAME_CATEGORY |
| Platform flags | PLATFORM + GAME_PLATFORM |
| Supported/audio languages | LANGUAGE + GAME_LANGUAGE |
| Screenshot list | GAME_SCREENSHOT |
| Movie list | GAME_MOVIE |
| Public review records | REVIEW |
| SteamScope users | USER |
| Simulated ownership | LIBRARY |
| Simulated wishlist | WISHLIST |
| Simulated purchases | PURCHASE |
| Simulated/approved achievement records | ACHIEVEMENT + USER_ACHIEVEMENT |
| Simulated activity | USER_ACTIVITY |

## 5. Validation gates before MySQL

The data is not ready for final import until:

- GAME AppID uniqueness is confirmed.
- GAME field alignment is understood.
- Review AppIDs have adequate coverage in the cleaned GAME dataset.
- Multi-valued fields can be parsed reliably.
- Platform fields are verified.
- Timestamp conversion is verified.
- Duplicate rules are established.
- Missing-value rules are documented.
- Public-source data and simulated data are clearly separated.

## 6. Recommended data folders

Use:

```text
data/
├── raw/
├── cleaned/
└── validation/
```

`raw/` contains original source files and should not be edited.

`cleaned/` contains transformed files intended for database loading.

`validation/` contains profiling reports, rejected/uncertain records, and data-quality summaries.
