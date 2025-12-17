# api/steamspy_api.py

import requests
import time
from config import STEAMSPY_API_URL, STEAMSPY_REQUEST_INTERVAL

def fetch_steamspy_data(appid):
    """Fetch data for a Steam app from SteamSpy."""
    url = STEAMSPY_API_URL.format(appid)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching SteamSpy for {appid}: {e}")
    time.sleep(STEAMSPY_REQUEST_INTERVAL)
    return None
