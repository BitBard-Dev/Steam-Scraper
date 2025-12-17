# utils/data_cleaning.py

import pandas as pd
import json
from config import CSV_VALID_APPS, CSV_UNIQUE_APPS

def remove_duplicates():
    """Removes duplicate App IDs from CSV."""
    df = pd.read_csv(CSV_VALID_APPS)
    df_unique = df.drop_duplicates(subset=["appid"])
    df_unique.to_csv(CSV_UNIQUE_APPS, index=False)

def filter_json_keys(input_file, output_file, keep_keys):
    """Keeps only specified keys in each JSON object."""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    cleaned = [{k: v for k, v in game.items() if k in keep_keys} for game in data]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4)
