# main.py

from api.steam_api import fetch_app_list
from utils.data_cleaning import remove_duplicates
from db.mongo_handler import delete_duplicates
from db.sqlite_handler import connect_sqlite, create_overall_info_table, insert_overall_info
from config import JSON_CLEANED

import json

def run_all():
    print("📥 Step 1: Fetch app list from Steam...")
    fetch_app_list()

    print("🧹 Step 2: Remove duplicate appids...")
    remove_duplicates()

    print("🧼 Step 3: Clean up MongoDB duplicates (if any)...")
    delete_duplicates()

    print("📦 Step 4: Import JSON to SQLite...")
    with open(JSON_CLEANED, "r", encoding="utf-8") as f:
        games = json.load(f)

    conn = connect_sqlite()
    cur = conn.cursor()
    create_overall_info_table(cur)

    for game in games:
        insert_overall_info(cur, game)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ All steps completed.")

if __name__ == "__main__":
    run_all()
