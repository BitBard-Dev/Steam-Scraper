from src.validation.completeness_checks import find_missing

VALID = "data/raw/steam_valid_apps.csv"
PROCESSED = "data/interim/processed_apps.csv"
OUTPUT = "data/interim/missing_apps.csv"

if __name__ == "__main__":
    missing = find_missing(VALID, PROCESSED, OUTPUT)
    print(f"Missing apps: {missing}")