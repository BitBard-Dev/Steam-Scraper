import json
from src.steam_api.steamspy import fetch_steamspy

INPUT = "data/processed/steam_games_languages.json"
OUTPUT = "data/processed/steam_games_with_tags.json"

if __name__ == "__main__":
    with open(INPUT, "r", encoding="utf-8") as f:
        games = json.load(f)

    for g in games:
        spy = fetch_steamspy(g["steam_appid"])
        if spy:
            g.update(spy)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)

    print("SteamSpy data added.")