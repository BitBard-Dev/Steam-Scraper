from src.processing.chunking import split_json

INPUT = "data/processed/steam_games_with_tags.json"
OUTPUT_DIR = "data/processed/chunks"

if __name__ == "__main__":
    split_json(INPUT, OUTPUT_DIR)
    print("JSON chunking complete.")