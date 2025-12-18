import requests
import pandas as pd
from config.constants import APP_LIST_URL

def fetch_valid_apps(api_key: str, output_csv: str):
    url = f"{APP_LIST_URL}?key={api_key}&format=json"
    response = requests.get(url)
    response.raise_for_status()

    apps = response.json()["applist"]["apps"]
    valid = [{"appid": a["appid"], "name": a["name"]} for a in apps if a.get("name")]

    pd.DataFrame(valid).to_csv(output_csv, index=False)
    return len(valid)