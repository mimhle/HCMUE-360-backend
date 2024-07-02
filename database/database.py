import pymongo
import os

DB_URL = os.environ.get("MONGO_PRIVATE_URL", "")
DB_DB = os.environ.get("MONGO_DB", "")
# DB_COLLECTION = os.environ.get("MONGO_COLLECTION", "")


def get_scene(id_: int) -> dict:
    with pymongo.MongoClient(DB_URL) as client:
        collection = client[DB_DB]["scenes"]
        return collection.find_one({"id": id_})
