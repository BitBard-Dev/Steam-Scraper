import time
import requests
from config.constants import HEADERS

def get_with_retries(url, retries=3, backoff=30):
    for _ in range(retries):
        r = requests.get(url, headers=HEADERS)
        if r.status_code == 200:
            return r
        if r.status_code == 429:
            time.sleep(backoff)
    return None