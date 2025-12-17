# db/mongo_handler.py

from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION

def get_mongo_collection():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    return db[MONGODB_COLLECTION]

def delete_duplicates():
    coll = get_mongo_collection()
    pipeline = [
        {"$group": {"_id": "$steam_appid", "count": {"$sum": 1}, "ids": {"$push": "$_id"}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    for doc in coll.aggregate(pipeline):
        dup_ids = doc["ids"][1:]  # keep 1
        coll.delete_many({"_id": {"$in": dup_ids}})
