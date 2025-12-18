from src.persistence.sqlite_loader import build_all_tables

DB_PATH = "data/processed/steam_analysis.sqlite"

if __name__ == "__main__":
    build_all_tables(DB_PATH)
    print("SQLite build complete.")