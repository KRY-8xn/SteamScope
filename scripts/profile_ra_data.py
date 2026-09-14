from pathlib import Path
import pandas as pd


# ============================================================
# SteamScope - Raw Data Profiling
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

GAMES_FILE = RAW_DIR / "games.csv"

REVIEW_FILES = sorted(RAW_DIR.glob("reviews-*.csv"))


def profile_games():
    print("\n" + "=" * 80)
    print("GAMES DATASET")
    print("=" * 80)

    print(f"File: {GAMES_FILE}")

    df = pd.read_csv(
        GAMES_FILE,
        low_memory=False
    )

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- Column Names ---")
    for i, col in enumerate(df.columns, start=1):
        print(f"{i:>3}. {col}")

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- Missing Values ---")
    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(2)

    missing_report = pd.DataFrame({
        "missing_count": missing,
        "missing_percent": missing_pct
    })

    print(missing_report[missing_report["missing_count"] > 0])

    print("\n--- Duplicate Rows ---")
    print(f"Exact duplicate rows: {df.duplicated().sum():,}")

    print("\n--- First 5 Rows ---")
    print(df.head().to_string())

    print("\n--- Basic Statistics ---")
    print(df.describe(include="all").transpose().to_string())

    print("\n--- Unique Values ---")
    for col in df.columns:
        try:
            print(f"{col}: {df[col].nunique(dropna=True):,}")
        except Exception:
            print(f"{col}: unable to calculate")


def profile_reviews():
    print("\n" + "=" * 80)
    print("REVIEW DATASETS")
    print("=" * 80)

    if not REVIEW_FILES:
        print("No review CSV files found.")
        return

    total_rows = 0

    for file in REVIEW_FILES:
        print("\n" + "-" * 80)
        print(f"FILE: {file.name}")
        print("-" * 80)

        # Read only a small sample first.
        sample = pd.read_csv(
            file,
            nrows=1000,
            low_memory=False
        )

        print(f"Sample rows read: {len(sample):,}")
        print(f"Columns: {len(sample.columns)}")

        print("\nColumn Names:")
        for i, col in enumerate(sample.columns, start=1):
            print(f"{i:>3}. {col}")

        print("\nData Types:")
        print(sample.dtypes)

        print("\nMissing Values in Sample:")

        missing = sample.isna().sum()
        missing_pct = (missing / len(sample) * 100).round(2)

        missing_report = pd.DataFrame({
            "missing_count": missing,
            "missing_percent": missing_pct
        })

        print(
            missing_report[
                missing_report["missing_count"] > 0
            ]
        )

        print("\nExact Duplicate Rows in Sample:")
        print(sample.duplicated().sum())

        print("\nFirst 3 Rows:")
        print(sample.head(3).to_string())

        # Count rows without loading the complete file into memory.
        file_rows = 0

        with open(file, "rb") as f:
            for _ in f:
                file_rows += 1

        # Subtract header row.
        file_rows = max(file_rows - 1, 0)

        total_rows += file_rows

        print(f"\nEstimated/physical row count: {file_rows:,}")

    print("\n" + "=" * 80)
    print("REVIEW DATASET SUMMARY")
    print("=" * 80)

    print(f"Review files: {len(REVIEW_FILES)}")
    print(f"Total review rows across files: {total_rows:,}")


def main():
    print("=" * 80)
    print("STEAMSCOPE RAW DATA PROFILER")
    print("=" * 80)

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Raw data directory: {RAW_DIR}")

    if not GAMES_FILE.exists():
        print(f"\nERROR: Games file not found:")
        print(GAMES_FILE)
        return

    profile_games()
    profile_reviews()

    print("\n" + "=" * 80)
    print("PROFILING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()