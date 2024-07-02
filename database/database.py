import pymongo


def get_scene(id_: int, *, db: dict = None) -> dict:
    if not dict:
        raise ValueError("db must be provided")

    with pymongo.MongoClient(db["url"]) as client:
        collection = client[db["db"]]["scenes"]
        result = collection.find_one({"id": id_})
        print(result)
        return result
