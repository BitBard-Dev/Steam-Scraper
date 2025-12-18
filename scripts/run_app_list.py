from src.steam_api.app_list import fetch_valid_apps

API_KEY = "STEAMKEY"
OUTPUT_CSV = "data/raw/steam_valid_apps.csv"

if __name__ == "__main__":
    count = fetch_valid_apps(API_KEY, OUTPUT_CSV)
    print(f"Saved {count} valid Steam apps.")