from src.processing.json_cleaning import prune_json

INPUT = "data/raw/steam_games.json"
OUTPUT = "data/processed/steam_games_cleaned.json"

if __name__ == "__main__":
    prune_json(INPUT, OUTPUT)
    print("JSON cleaned.")