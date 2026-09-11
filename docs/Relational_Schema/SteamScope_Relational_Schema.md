# SteamScope – Relational Schema

## 1. Purpose

This document defines the relational schema for SteamScope, a database-driven game library and Steam ecosystem analytics platform.

The schema is designed around:
- 3NF normalization
- Primary and foreign keys
- Many-to-many relationships resolved through junction tables
- Referential integrity
- SQL analytics over games, reviews, and simulated user-side activity

> **Data policy:** Publicly available game/catalog/review data is used as the source data. User libraries, wishlists, purchases, achievements, and activity may be simulated for the academic project. No private Steam purchase, revenue, or user data is assumed.

---

## 2. Core Entities

### USER
| Attribute | Key | Description |
|---|---|---|
| UserID | PK | Internal SteamScope user identifier |
| SteamID | UNIQUE | External/public Steam identifier where available |
| Username | | SteamScope username |
| Email | | User email |
| RegistrationDate | | Date the user registered |
| Country | | User country |

### GAME
| Attribute | Key | Description |
|---|---|---|
| AppID | PK | Steam application/game identifier |
| Name | | Game name |
| ReleaseDate | | Release date |
| EstimatedOwners | | Estimated ownership range from source |
| PeakCCU | | Peak concurrent users |
| RequiredAge | | Required age |
| Price | | Listed/current source price |
| DiscountDLCCount | | Source field retained after validation |
| Description | | Game description |
| Website | | Game website |
| SupportURL | | Support website |
| SupportEmail | | Support email |
| MetacriticScore | | Metacritic score |
| UserScore | | User score |
| PositiveReviews | | Positive review count |
| NegativeReviews | | Negative review count |
| ScoreRank | | Source score rank |
| Recommendations | | Recommendation count |
| AveragePlaytimeForever | | Average lifetime playtime |
| AveragePlaytimeTwoWeeks | | Average two-week playtime |
| MedianPlaytimeForever | | Median lifetime playtime |
| MedianPlaytimeTwoWeeks | | Median two-week playtime |

**Data-quality note:** The uploaded game sample showed evidence of malformed/misaligned source columns. Final mappings and retained attributes must therefore be validated during the data-cleaning stage before import.

### REVIEW
| Attribute | Key | Description |
|---|---|---|
| ReviewID | PK | Internal unique review identifier |
| UserID | FK → USER.UserID | Reviewer |
| AppID | FK → GAME.AppID | Reviewed game |
| VotedUp | | Recommendation flag |
| VotesUp | | Helpful/up votes |
| VotesFunny | | Funny votes |
| WeightedVoteScore | | Weighted review score |
| PlaytimeForever | | Total playtime |
| PlaytimeAtReview | | Playtime when review was written |
| NumGamesOwned | | Number of games owned by reviewer |
| NumReviews | | Number of reviews written |
| ReviewText | | Review text |
| CreatedAt | | Review creation timestamp |
| UpdatedAt | | Review update timestamp |

---

## 3. Game Reference Entities

### DEVELOPER
`DeveloperID (PK), DeveloperName (UNIQUE)`

### PUBLISHER
`PublisherID (PK), PublisherName (UNIQUE)`

### GENRE
`GenreID (PK), GenreName (UNIQUE)`

### TAG
`TagID (PK), TagName (UNIQUE)`

### CATEGORY
`CategoryID (PK), CategoryName (UNIQUE)`

### PLATFORM
`PlatformID (PK), PlatformName (UNIQUE)`

### LANGUAGE
`LanguageID (PK), LanguageName (UNIQUE)`

---

## 4. Many-to-Many Junction Tables

### GAME_DEVELOPER
- `AppID` — PK, FK → GAME.AppID
- `DeveloperID` — PK, FK → DEVELOPER.DeveloperID
- Composite PK: `(AppID, DeveloperID)`

### GAME_PUBLISHER
- `AppID` — PK, FK → GAME.AppID
- `PublisherID` — PK, FK → PUBLISHER.PublisherID
- Composite PK: `(AppID, PublisherID)`

### GAME_GENRE
- `AppID` — PK, FK → GAME.AppID
- `GenreID` — PK, FK → GENRE.GenreID
- Composite PK: `(AppID, GenreID)`

### GAME_TAG
- `AppID` — PK, FK → GAME.AppID
- `TagID` — PK, FK → TAG.TagID
- Composite PK: `(AppID, TagID)`

### GAME_CATEGORY
- `AppID` — PK, FK → GAME.AppID
- `CategoryID` — PK, FK → CATEGORY.CategoryID
- Composite PK: `(AppID, CategoryID)`

### GAME_PLATFORM
- `AppID` — PK, FK → GAME.AppID
- `PlatformID` — PK, FK → PLATFORM.PlatformID
- Composite PK: `(AppID, PlatformID)`

### GAME_LANGUAGE
- `AppID` — PK, FK → GAME.AppID
- `LanguageID` — PK, FK → LANGUAGE.LanguageID
- `LanguageType` — identifies SUPPORTED or AUDIO
- Composite PK: `(AppID, LanguageID, LanguageType)`

---

## 5. Game Media

### GAME_SCREENSHOT
- `ScreenshotID` — PK
- `AppID` — FK → GAME.AppID
- `ImageURL`

### GAME_MOVIE
- `MovieID` — PK
- `AppID` — FK → GAME.AppID
- `VideoURL`

---

## 6. User Ecosystem

### LIBRARY
- `UserID` — PK, FK → USER.UserID
- `AppID` — PK, FK → GAME.AppID
- `AddedAt`
- `LastPlayedAt`
- `PlaytimeMinutes`
- Composite PK: `(UserID, AppID)`

### WISHLIST
- `UserID` — PK, FK → USER.UserID
- `AppID` — PK, FK → GAME.AppID
- `AddedAt`
- Composite PK: `(UserID, AppID)`

### PURCHASE
- `PurchaseID` — PK
- `UserID` — FK → USER.UserID
- `AppID` — FK → GAME.AppID
- `PurchaseDate`
- `PricePaid`

> Purchases are simulated academic data, not private Steam sales data.

### ACHIEVEMENT
- `AchievementID` — PK
- `AppID` — FK → GAME.AppID
- `AchievementName`
- `Description`

### USER_ACHIEVEMENT
- `UserID` — PK, FK → USER.UserID
- `AchievementID` — PK, FK → ACHIEVEMENT.AchievementID
- `UnlockedAt`
- Composite PK: `(UserID, AchievementID)`

### USER_ACTIVITY
- `ActivityID` — PK
- `UserID` — FK → USER.UserID
- `AppID` — FK → GAME.AppID
- `ActivityType`
- `ActivityTimestamp`
- `DurationMinutes`

---

## 7. Relationship Summary

| Relationship | Cardinality | Implemented By |
|---|---|---|
| USER → REVIEW | 1:N | REVIEW.UserID |
| GAME → REVIEW | 1:N | REVIEW.AppID |
| USER ↔ GAME | M:N | LIBRARY |
| USER ↔ GAME | M:N | WISHLIST |
| USER ↔ GAME | M:N | PURCHASE |
| GAME → ACHIEVEMENT | 1:N | ACHIEVEMENT.AppID |
| USER ↔ ACHIEVEMENT | M:N | USER_ACHIEVEMENT |
| USER → USER_ACTIVITY | 1:N | USER_ACTIVITY.UserID |
| GAME → USER_ACTIVITY | 1:N | USER_ACTIVITY.AppID |
| GAME ↔ DEVELOPER | M:N | GAME_DEVELOPER |
| GAME ↔ PUBLISHER | M:N | GAME_PUBLISHER |
| GAME ↔ GENRE | M:N | GAME_GENRE |
| GAME ↔ TAG | M:N | GAME_TAG |
| GAME ↔ CATEGORY | M:N | GAME_CATEGORY |
| GAME ↔ PLATFORM | M:N | GAME_PLATFORM |
| GAME ↔ LANGUAGE | M:N | GAME_LANGUAGE |
| GAME → GAME_SCREENSHOT | 1:N | GAME_SCREENSHOT.AppID |
| GAME → GAME_MOVIE | 1:N | GAME_MOVIE.AppID |

---

## 8. Normalization Summary

### First Normal Form (1NF)
Multi-valued attributes such as developers, publishers, genres, tags, categories, platforms, languages, screenshots, and movies are separated into atomic relational structures.

### Second Normal Form (2NF)
Junction tables with composite keys contain only attributes dependent on the complete composite key. Descriptive game, user, developer, genre, and other entity attributes are kept in their respective entities.

### Third Normal Form (3NF)
Transitive dependencies are removed. For example, developer names are stored in DEVELOPER rather than in GAME_DEVELOPER or GAME, and genre names are stored in GENRE rather than in GAME_GENRE or GAME.

---

## 9. Current Design Scope

The current conceptual design contains **25 tables**.

The schema will be validated against the cleaned datasets before SQL implementation. In particular:
1. GAME source-column mappings must be validated.
2. REVIEW-to-GAME AppID coverage must be checked.
3. Achievement source availability must be established before loading achievement records.
4. User-side records that are not publicly sourced will be explicitly identified as simulated data.
