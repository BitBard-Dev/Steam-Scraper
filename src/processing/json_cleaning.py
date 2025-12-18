import json

KEEP_KEYS = {
    "type","name","steam_appid","is_free","about_the_game",
    "supported_languages","developers","publishers",
    "price_overview","categories","genres","recommendations",
    "release_date","content_descriptors","ratings"
}

def prune_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = [{k:v for k,v in g.items() if k in KEEP_KEYS} for g in data]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
