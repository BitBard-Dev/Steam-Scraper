from config.constants import APP_DETAILS_URL
from src.utils.http import get_with_retries

def fetch_app_details(appid: int):
    r = get_with_retries(APP_DETAILS_URL.format(appid))
    if not r:
        return None

    payload = r.json().get(str(appid), {})
    if payload.get("success"):
        data = payload["data"]
        if data.get("type") == "game":
            return data
    return None