# db/sqlite_handler.py

import sqlite3
from config import SQLITE_DB

def connect_sqlite():
    return sqlite3.connect(SQLITE_DB)

def create_overall_info_table(cursor):
    cursor.execute("DROP TABLE IF EXISTS overall_info")
    cursor.execute("""
    CREATE TABLE overall_info(
        steam_appid INTEGER PRIMARY KEY,
        type TEXT,
        name TEXT,
        release_date DATE,
        coming_soon BOOLEAN,
        about_the_game TEXT,
        developers TEXT,
        publishers TEXT
    )""")

def insert_overall_info(cursor, game):
    devs = ", ".join(game.get("developers", [])) if isinstance(game.get("developers"), list) else "N/A"
    pubs = ", ".join(game.get("publishers", [])) if isinstance(game.get("publishers"), list) else "N/A"
    cursor.execute("""
        INSERT INTO overall_info (
            steam_appid, type, name, release_date, coming_soon, about_the_game, developers, publishers
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            game.get("steam_appid"),
            game.get("type"),
            game.get("name"),
            game.get("release_date", {}).get("date", None),
            game.get("release_date", {}).get("coming_soon", False),
            game.get("about_the_game", "N/A"),
            devs,
            pubs
        )
    )
