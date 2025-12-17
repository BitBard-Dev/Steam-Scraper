# api/steam_api.py

import requests
import pandas as pd
import time
import json
from config import APP_LIST_URL, APP_DETAILS_URL, HEADERS, CSV_VALID_APPS

def fetch_app_list():
    """Fetches Steam app list and saves valid app names to CSV."""
    response = requests.get(APP_LIST_URL)
    data = response.json()
    apps = data["applist"]["apps"]
    valid_apps = [{"appid": app["appid"], "name": app["name"]} for app in apps if app["name"]]
    pd.DataFrame(valid_apps).to_csv(CSV_VALID_APPS, index=False)

def fetch_app_details(app_id):
    """Fetch appdetails for a single app_id."""
    url = APP_DETAILS_URL.format(app_id)
    retries = 3

    for _ in range(retries):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            result = data.get(str(app_id), {})
            if result.get("success") and result.get("data", {}).get("type") == "game":
                return result["data"]
        elif response.status_code == 429:
            print("Rate limited. Waiting...")
            time.sleep(30)
        else:
            print(f"Error {response.status_code} for app_id {app_id}")
    return None
