import json
from src.processing.language_processing import clean_languages

INPUT = "data/processed/steam_games_cleaned.json"
OUTPUT = "data/processed/steam_games_languages.json"

if __name__ == "__main__":
    with open(INPUT, "r", encoding="utf-8") as f:
        games = json.load(f)

    for g in games:
        if "supported_languages" in g:
            g["supported_languages"] = clean_languages(g["supported_languages"])

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)

    print("Languages normalized.")