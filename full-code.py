import requests
import pandas as pd

# Steam API URL (Replace 'STEAMKEY' with API key)
# https://steamcommunity.com/dev/apikey to request API key
STEAMKEY = ""
APP_LIST_URL = (f"https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key={STEAMKEY}&format=json")

# CSV file to store valid app IDs
CSV_FILE = "steam_valid_apps.csv"

def fetch_and_save_valid_apps():
    """Fetches all Steam apps and saves only those with valid names to CSV."""
    try:
        response = requests.get(APP_LIST_URL)
        response.raise_for_status()
        data = response.json()

        apps = data.get("applist", {}).get("apps", [])
        # for loop only pulls data if "name" != None
        valid_apps = [{"appid": app["appid"], "name": app["name"]} for app in apps if app.get("name")]

        df = pd.DataFrame(valid_apps)
        df.to_csv(CSV_FILE, index= False)

        print(f"Saved {len(df)} valid apps to {CSV_FILE}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching app list: {e}")

# Run step 1
fetch_and_save_valid_apps()


