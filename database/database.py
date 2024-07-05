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
        result = [item for item in
                  collection.find({}, {"id": 1, "name": 1, "description": 1, "_id": 0}, sort=[("_id", 1)])]
        return result


def update_scene(id_: int, data: dict, *, db: dict | None = None) -> dict:
    if not db:
        raise ValueError("db must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["Scenes"]
        if data == {}:
            return json.loads(
                json.dumps(collection.find_one_and_delete({"id": id_}, {"_id": 0}), default=str))
        return json.loads(
            json.dumps(collection.find_one_and_replace({"id": id_}, data, {"_id": 0}, return_document=True),
                       default=str))


def add_scene(data: dict, *, db: dict | None = None) -> bool:
    if not db:
        raise ValueError("db must be provided")

    if "name" not in data:
        raise ValueError("name must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["Scenes"]

        last_id = collection.find_one(sort=[("id", -1)])["id"]
        data["id"] = last_id + 1

        return collection.insert_one(data) is not None
