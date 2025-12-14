import requests
import pandas as pd

## Code Block 1: Query ISteam API to Determine Total Number of Valid Steam Apps

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

# Run code block 1
fetch_and_save_valid_apps()





## Code Block 2: Remove Duplicate Steam App IDs from the list of Valid Steam Apps

# File paths (enter file explorer path for INPUT_CSV and OUTPUT_CSV)
# If no manual changes (due to redo), then INPUT_CSV == CSV_FILE
INPUT_CSV = CSV_FILE
OUTPUT_CSV = "steam_valid_apps_unique.csv"

def remove_csv_duplicates(input_csv, output_csv):
    """Removes duplicate steam_appid entries from a CSV file."""
    try:
        #Load CSV file
        df = pd.read_csv(input_csv)
        #Drop duplicates based on steam_appid, keepint the first occurance
        df_unique = df.drop_duplicates(subset=["appid"], keep="first")
        # Save cleaned CSV file
        df_unique.to_csv(output_csv, index=False)
        print(f"Removed {(len(df))-(len(df_unique))} duplicates. Original count: {len(df)}, Unique count: {len(df_unique)}")
        print(f"Cleaned file saved as: {output_csv}")
    except FileNotFoundError:
        print("Error: CSF file not found")
    except Exception as e:
        print(f"Error: {e}")

# Run code block 2
remove_csv_duplicates(INPUT_CSV, OUTPUT_CSV)





## Code Block 3: Query Steam API to Pull All AppDetails for Each Steam Valid, Unique App ID
# API request rate-limited to ~500 requests/5 minutes due to no API key included in request when original project was run
## ???Improves: load "appid query results" into "log.csv". Load successful "appid query results" into "games_data.csv"

# import requests Duplicate from Code Block 1
# import pandas as pd Duplicate from Code Block 1
import json
import time
import os
import datetime

# Steam API URL
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails?appids={}"

# File paths
OUTPUT_CSV = "steam_valid_apps_unique.csv" # assumes code block 2 OUTPUT_CSV is in the same folder as the .ipynb
PROCESSED_CSV = "processed_apps.csv" # New CSV for successfully processed apps
OUTPUT_JSON = "steam_apps_grouped.json" # Output JSON for games only

# Steam API rate limits
BATCH_SIZE = 200 # Max requests per 5-minute interval (Steam API limit)
REQUEST_INTERVAL = 305 # 5:05 minute wait interval

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
} # spoofs as a regular user to reduce risk of temporary blacklist/rate limit from Steam

def fetch_app_details(app_id):
    """Fetch details for a single app with retry handling"""
    url = APP_DETAILS_URL.format(app_id)
    retries = 3

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS)

            if response.status_code == 429:
                print(f"429: Too many requests for {app_id}. Waiting 30 seconds...")
                time.sleep(30)
                continue

            if response.status_code != 200:
                print(f"Error {response.status_code} fetching {app_id}: {response.text}")
                return {"appid": app_id, "error": f"HTTP {response.status_code}"}
            
            data = response.json()

            if not data or str(app_id) not in data:
                print(f"Warning: No valid data received for {app_id}")
                return {"appid": app_id, "error": "No valid data"}
            
            # Extract only "data" part
            app_data = data[str(app_id)]
            if not app_data.get("success"):
                print(f"Invalid app ID: {app_id} (No success flag)")
                return {"appid": app_id, "error": "Invalid App ID"}
            
            # Extract actual game data
            game_info = app_data["data"]

            # Ensure it's a gamve before returning
            if game_info.get("type") == "game":
                return game_info
            else:
                print(f"Skipping non-game app: {app_id} (Type: {game_info.get('type')})") #Single quotes needed???
                return {"appid": app_id, "error": f"Not a game (Type: {game_info.get('type')})"} #Single quotes needede???
        
        except requests.RequestException as e:
            print(f"Network error while fetching {app_id}: {e}")
            return {"appid": app_id, "error": "Network error"}
        
    print(f"Repeated errors for {app_id}. Skiping.")
    return {"appid": app_id, "error": "Too many requests, skipped"}

def load_valid_apps():
    """Loads valid app IDs form CSV file"""
    df = pd.read_csv(CSV_FILE) # Cprrect CSV file call???
    return df["appid"].tolist()

def load_existing_json(): # ???Improve: create LIST from valid apps, then remove processed apps. Reduces r/w of JSON file. would need error handling to maintain list integrity
    """Loads existing JSON data and extracts already processed app IDs"""
    processed_app_ids = set()

    # Check processed CSV to ensure no duplicates occur
    if os.path.exists(PROCESSED_CSV):
        try:
            df = pd.read_csv(PROCESSED_CSV, dtype={"appid": str})
            processed_app_ids.update(df["appid"].astype(int).tolist())
        except Exception as e:
            print(f"Error reading processed)apps.csv: {e}")
    
    try:
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list):
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    return existing_data, processed_app_ids

def save_data_to_json(new_data, filename):
    """Safely appends new game data to JSON filw without duplicates"""
    try:
        # Load existing JSON file
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            if not isinstance(existing_data, list): # Ensure it's a list, not a dict
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []  # Start fresh if file doesn't exist

    # Extract existing app IDs to avoid duplicates
    existing_app_ids = {app["steam_appid"] for app in existing_data if isinstance(app, dict)}

    # Append only new unique games
    new_entries = [app for app in new_data if app.get("steam_appid") not in existing_app_ids]
    existing_data.extend(new_entries)

    # Save updated JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(new_data)} new games added to {filename}")

def save_processed_apps_to_csv(processed_apps):
    """Logs ALL processed apps, including non-games and errors, to avoid re-querying"""
    df = pd.DataFrame(processed_apps, columns=["appid", "name", "status"])
    
    if not os.path.exists(PROCESSED_CSV):
        df.to_csv(PROCESSED_CSV, index=False)  # Create new file
    else:
        df.to_csv(PROCESSED_CSV, mode="a", index=False, header=False)  # Append without headers

    print(f"✅ Processed {len(processed_apps)} apps. Logged to {PROCESSED_CSV}")

def count_processed_apps():
    """Counts total processed apps from processed_apps.csf"""
    if os.path.exists(PROCESSED_CSV):
        df = pd.read_csv(PROCESSED_CSV)
        return len(df) # Count total rows in processed_apps.csv
    return 0 # Returns 0 if file doesn't exist or no apps processed yet

def main():
    """Fetches Steam app details sequentially, logging processed app IDs and names."""
    all_valid_app_ids = load_valid_apps()
    existing_data, processed_app_ids = load_existing_json()
    unprocessed_app_ids = [appid for appid in all_valid_app_ids if appid not in processed_app_ids]

    if not unprocessed_app_ids:
        print("✅ All app IDs have been processed. Exiting loop.")
        return

    while unprocessed_app_ids:
        batch = unprocessed_app_ids[:BATCH_SIZE]  # Get up to 200 IDs
        unprocessed_app_ids = unprocessed_app_ids[BATCH_SIZE:]  # Remove processed batch

        print(f"\n⏳ Processing {len(batch)} new app IDs...")

        new_games = []  # Store only game-type entries
        processed_entries = [] #Store successfully procesed appids & names

        for app_id in batch:
            result = fetch_app_detail(app_id)

            # Log all apps, including non-games and errors
            if "error" not in result and result.get("type") == "game":
                new_games.append(result)
                processed_entries.append((app_id, result["name"], "Success")) # Save game info
            else:
                processed_entries.append((app_id, "", result.get("error", "Unknown Error"))) # Log non-games & errors

        save_processed_apps_to_csv(processed_entries) # Save all processed apps (games & non-games)

        print(f"✅ Finished fetching {len(batch)} apps.")

        # Save only games to JSON
        if new_games:
            save_data_to_json(new_games, OUTPUT_JSON) 

        # Get running total of processed apps
        total_processed_apps = count_processed_apps()

        # Calculate percentage completion
        percentage_complete = (total_processed_apps *100) / 172803 # 172803 is manual count of from steam_valid_apps.csv. Automate???

        # Print summary
        print(f"\n📊 Total games in JSON file: {len(load_existing_json()[0])}")
        print(f"Total apps processed: {total_processed_apps}")
        print(f"Percentage complete: {percentage_complete:.2f}%")
        
        # Wait before next batch
        print("\n⏳ Waiting 5 minutes before the next batch...")
        time.sleep(REQUEST_INTERVAL)

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(f"🚀 Script started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    main()  # Run sequentially

    end_time = datetime.datetime.now()
    print(f"✅ Script finished at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    duration = end_time - start_time
    print(f"⏳ Total execution time: {str(duration)}")





## Code Block 4: Verify All Valid Steam Apps were Processed (compares steam_valid_apps.csv to processed_apps.csv

# File paths
VALID_APPS_CSV = "steam_valid_apps_unique.csv"
PROCESSED_APPS_CSV = "processed_apps.csv"
MISSING_APPS_CSV = "missing_apps.csv"

def find_missing_apps():
    """Compares two CSV files and finds unprocessed app IDs."""
    # Load both CSVs
    valid_apps = pd.read_csv(VALID_APPS_CSV, usecols=["appid"])
    processed_apps = pd.read_csv(PROCESSED_APPS_CSV, usecols=["appid"])

    # Convert to sets for fast comparison
    valid_app_ids = set(valid_apps["appid"])
    processed_app_ids = set(processed_apps["appid"])

    # Find missing app IDs
    missing_app_ids = valid_app_ids - processed_app_ids

    if missing_app_ids:
        print(f"⚠️ {len(missing_app_ids)} apps were not processed!")
        
        # Create a DataFrame for missing apps
        missing_apps_df = valid_apps[valid_apps["appid"].isin(missing_app_ids)]
        
        # Save to CSV (Optional: Reprocess missing apps later)
        missing_apps_df.to_csv(MISSING_APPS_CSV, index=False)
        print(f"✅ Missing apps saved to {MISSING_APPS_CSV} for reprocessing.")
    else:
        print("✅ All apps have been successfully processed.")

# Run the comparison
find_missing_apps()





## Code Block 5: Clean steam_games_filtered.json Data to Remove Unnecessary Key-Value Pairs
#??? Improve: alter Code Block 4 to automatically filter unnecessary K-V pairs???

# File paths
INPUT_JSON = "steam_games_filtered.json"  # Your original JSON file
OUTPUT_JSON = "steam_games_cleaned.json"  # Cleaned JSON file

# ✅ Attributes to KEEP
keep_keys = {
    "type", "name", "steam_appid", "is_free", "about_the_game", "supported_languages",
    "developers", "publishers", "price_overview", "categories", "genres", "recommendations",
    "release_date", "content_descriptors", "ratings"
}

def clean_steam_json(input_file, output_file):
    """Loads, filters, and saves the cleaned JSON data."""
    try:
        # Load existing JSON
        with open(input_file, "r", encoding="utf-8") as f:
            games_data = json.load(f)
        
        # ✅ Keep only relevant attributes
        cleaned_data = [{k: v for k, v in game.items() if k in keep_keys} for game in games_data]

        # Save cleaned JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Successfully cleaned {len(cleaned_data)} game records. Saved to {output_file}")

    except Exception as e:
        print(f"⚠️ Error processing JSON: {e}")

# Run the cleaning function
clean_steam_json(INPUT_JSON, OUTPUT_JSON)





## Code Block 6: Clean the supported_languages Values for Follow-On Analyisis

import re

# File paths
INPUT_JSON = "steam_games_cleaned.json"  # Your cleaned JSON
OUTPUT_JSON = "steam_games_cleaned_languages.json"  # JSON file with cleaned languages

def clean_languages(lang_string):
    """Cleans the supported_languages string and categorizes full audio vs. interface/subtitles."""
    if not lang_string:
        return {"full_audio_languages": [], "interface_languages": []}

    # ✅ Extract full audio languages (inside <strong> tags)
    full_audio_matches = re.findall(r"<strong>(.*?)</strong>", lang_string)

    # ✅ Remove HTML tags & split by commas
    lang_string = re.sub(r"<.*?>", "", lang_string)  # Remove <strong>, <br>, etc.
    languages = [lang.strip() for lang in lang_string.split(",")]

    # ✅ Separate full audio and interface languages
    full_audio_languages = set(full_audio_matches)  # Convert to set to avoid duplicates
    interface_languages = [lang for lang in languages if lang not in full_audio_languages]

    return {
        "full_audio_languages": sorted(list(full_audio_languages)),  # Sort for consistency
        "interface_languages": sorted(interface_languages)  # Sort for consistency
    }

def clean_json_languages(input_file, output_file):
    """Processes JSON and cleans 'supported_languages'."""
    try:
        # Load existing JSON
        with open(input_file, "r", encoding="utf-8") as f:
            games_data = json.load(f)

        # ✅ Process each game's supported_languages
        for game in games_data:
            if "supported_languages" in game:
                game["supported_languages"] = clean_languages(game["supported_languages"])

        # Save updated JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(games_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Successfully cleaned and categorized languages for {len(games_data)} games.")
        print(f"✅ Cleaned data saved to {output_file}")

    except Exception as e:
        print(f"⚠️ Error processing JSON: {e}")

# Run the cleaning function
clean_json_languages(INPUT_JSON, OUTPUT_JSON)





## Code Block 7: Query SteamSpy to Retrieve Tags Data & Add It to steam_games_cleaned_languages.json

# File paths
INPUT_JSON = "steam_games_cleaned_languages.json"  # Source JSON
OUTPUT_CSV = "steamspy_games.csv"  # List of games to query

def extract_games_for_steamspy_csv():
    """Extracts steam_appid and name from JSON and saves to CSV."""
    try:
        # Load JSON data
        with open(INPUT_JSON, "r", encoding="utf-8") as f:
            games_data = json.load(f)

        # Convert to DataFrame
        df = pd.DataFrame(games_data, columns=["steam_appid", "name"])

        # Save to CSV
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Extracted {len(df)} games. Saved to {OUTPUT_CSV}")

    except Exception as e:
        print(f"⚠️ Error processing JSON: {e}")

# Run function
extract_games_for_steamspy_csv()





## Code Block 8: Query SteamSpy API, Save Data, and Ensure All Games Were Queried
#??? Improve: Is this step necessary? We just queried SteamSpy in the previous code block. Consolidate 7 & 8???

# API URL
STEAMSPY_API_URL = "https://steamspy.com/api.php?request=appdetails&appid={}"

# File paths
INPUT_CSV = "steamspy_games.csv"  # List of games to query
PROCESSED_CSV = "steamspy_processed_games.csv"  # Track completed queries
OUTPUT_JSON = "steam_games_allclean_tags.json"  # Save cleaned API responses

# SteamSpy Rate Limits
REQUEST_INTERVAL = 1  # 1 request per second

# Keys to extract from API response
STEAMSPY_KEYS = ["positive", "negative", "owners", "median_forever", "median_2weeks", "ccu", "tags"]

def load_processed_games():
    """Loads processed game appids from CSV to avoid duplicate queries."""
    if os.path.exists(PROCESSED_CSV):
        try:
            df = pd.read_csv(PROCESSED_CSV)
            return set(df["steam_appid"])
        except Exception as e:
            print(f"⚠️ Error reading processed games CSV: {e}")
    return set()

def save_processed_game(appid, name):
    """Logs processed games to CSV."""
    df = pd.DataFrame([[appid, name]], columns=["steam_appid", "name"])
    if not os.path.exists(PROCESSED_CSV):
        df.to_csv(PROCESSED_CSV, index=False)
    else:
        df.to_csv(PROCESSED_CSV, mode="a", index=False, header=False)

def fetch_steamspy_data(appid):
    """Fetches SteamSpy data for a given appid."""
    url = STEAMSPY_API_URL.format(appid)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Error {response.status_code} for appid {appid}")
    except requests.RequestException as e:
        print(f"⚠️ Network error fetching {appid}: {e}")
    return None

def save_to_json(data, filename):
    """Appends new SteamSpy data to JSON file."""
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_appids = {entry["steam_appid"] for entry in existing_data}
        new_entries = [entry for entry in data if entry["steam_appid"] not in existing_appids]

        existing_data.extend(new_entries)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        print(f"✅ {len(new_entries)} new games added to {filename}")

    except Exception as e:
        print(f"⚠️ Error saving JSON: {e}")

def query_steamspy():
    """Queries SteamSpy API for all games listed in steamspy_games.csv."""
    games_df = pd.read_csv(INPUT_CSV)
    processed_games = load_processed_games()

    new_data = []
    for index, row in games_df.iterrows():
        appid, name = row["steam_appid"], row["name"]

        if appid in processed_games:
            print(f"⏭️ Skipping already processed appid: {appid}")
            continue

        print(f"🔍 Fetching data for {appid} - {name}")
        game_data = fetch_steamspy_data(appid)

        if game_data:
            filtered_data = {key: game_data.get(key, None) for key in STEAMSPY_KEYS}
            filtered_data["steam_appid"] = appid  # Ensure appid is included
            new_data.append(filtered_data)

            # Log processed game
            save_processed_game(appid, name)

        # Respect API rate limit
        time.sleep(REQUEST_INTERVAL)

    # Save all new data
    if new_data:
        save_to_json(new_data, OUTPUT_JSON)
    print("✅ SteamSpy data collection complete.")

# Run the function
query_steamspy()

# Ensure All Steam Apps Were Processed by Comparing steamspy_games.csv and steamspy_processed_games.csv
# File paths
VALID_APPS_CSV = "steamspy_games.csv"  # Apps that should have been processed
PROCESSED_APPS_CSV = "steamspy_processed_games.csv"  # Apps that were actually processed
MISSING_APPS_CSV = "steamspy_missing_apps.csv"  # (Optional) Output file for missing apps

# Run the comparison
find_missing_apps()