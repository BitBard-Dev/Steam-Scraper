import time, requests
from config.constants import STEAMSPY_URL
from config.settings import STEAMSPY_DELAY

STEAMSPY_KEYS = ["positive","negative","owners","ccu","tags"]

def fetch_steamspy(appid):
    r = requests.get(STEAMSPY_URL.format(appid))
    if r.status_code == 200:
        data = r.json()
        return {k: data.get(k) for k in STEAMSPY_KEYS} | {"steam_appid": appid}
    time.sleep(STEAMSPY_DELAY)
    return None