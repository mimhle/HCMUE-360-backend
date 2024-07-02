import json
import pymongo


def get_scene(id_: int, *, db: dict = None) -> dict:
    if not dict:
        raise ValueError("db must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["Scenes"]
        return json.loads(json.dumps(collection.find_one({"id": id_}, {"_id": 0}), default=str))


def get_scenes(*, db: dict | None = None) -> list[dict]:
    if not db:
        raise ValueError("db must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["Scenes"]
        result = [item for item in collection.find({}, {"id": 1, "name": 1, "_id": 0}, sort=[("_id", 1)])]
        return result


def update_scene(id_: int, data: dict, *, db: dict | None = None) -> dict:
    if not db:
        raise ValueError("db must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["Scenes"]
        return collection.find_one_and_replace({"id": id_}, data)
