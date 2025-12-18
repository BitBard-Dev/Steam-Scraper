from src.persistence.mongo_loader import import_chunks

CHUNK_DIR = "data/processed/chunks"
DB_NAME = "steam_games"
COLLECTION = "games"

if __name__ == "__main__":
    import_chunks(CHUNK_DIR, DB_NAME, COLLECTION)