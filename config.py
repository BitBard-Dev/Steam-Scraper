# config.py

# Steam API base URLs
APP_LIST_URL = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/?format=json"
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={}"
STEAMSPY_API_URL = "https://steamspy.com/api.php?request=appdetails&appid={}"

# Headers for Steam API requests
# Is this portion necessary? Needs extra testing??? Affects steam_api.py as well.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# File paths
CSV_VALID_APPS = "data/raw/steam_valid_apps.csv"
CSV_UNIQUE_APPS = "data/raw/steam_valid_apps_unique.csv"
CSV_PROCESSED_APPS = "data/raw/processed_apps.csv"
CSV_STEAMSPY = "data/raw/steamspy_games.csv"
JSON_RAW_GAME_DATA = "data/raw/steam_games_filtered.json"
JSON_CLEANED = "data/cleaned/steam_games_cleaned.json"
JSON_LANGUAGES = "data/cleaned/steam_games_cleaned_languages.json"
JSON_WITH_TAGS = "data/cleaned/steam_games_allclean_tags.json"

MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DB = "PROJECT_PHASE_2"
MONGODB_COLLECTION = "STEAM_GAMES_NOSTEAMSPY"

SQLITE_DB = "data/sqlite/steam_analysis.sqlite"

# API rate limits
STEAM_API_BATCH_SIZE = 200
STEAM_API_REQUEST_INTERVAL = 305
STEAMSPY_REQUEST_INTERVAL = 1
