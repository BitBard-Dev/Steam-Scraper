from src.steam_api.app_details import fetch_app_details
from src.persistence.csv_io import append_rows

# thin orchestration only

###??? incorporate???
import time
import pandas as pd

from src.steam_api.app_details import fetch_app_details
from src.persistence.csv_io import append_rows
from config.settings import BATCH_SIZE, REQUEST_INTERVAL

INPUT_CSV = "data/raw/steam_valid_apps.csv"
PROCESSED_CSV = "data/interim/processed_apps.csv"
OUTPUT_JSON = "data/raw/steam_games.json"

def main():
    df = pd.read_csv(INPUT_CSV)
    appids = df["appid"].tolist()

    processed = []
    games = []

    for appid in appids:
        data = fetch_app_details(appid)
        if data:
            games.append(data)
            processed.append((appid, data.get("name", ""), "Success"))
        else:
            processed.append((appid, "", "Skipped"))

        if len(processed) % BATCH_SIZE == 0:
            append_rows(PROCESSED_CSV, processed, ["appid", "name", "status"])
            processed.clear()
            time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    main()
