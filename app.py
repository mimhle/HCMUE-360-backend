from database.database import get_scene as get_scene_, get_scenes as get_scenes_, update_scene as update_scene_, add_scene as add_scene_
from flask import Flask, request, Response
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


with app.app_context():
    DB = {
        "url": os.environ.get("MONGO_PRIVATE_URL"),
        "db": os.environ.get("MONGO_DB"),
    }


@app.route('/')
def hello_world():
    return DB["db"]


# placeholder for authentication
@app.route("/auth", methods=["POST"])
def auth() -> Response:
    data = request.get_json()
    if not data:
        return Response(status=400)
    if data["password"] == os.environ.get("PASSWORD"):
        return Response(status=200)
    return Response(status=401)


@app.before_request
def check_token():
    if (request.path == "/auth") or (request.method in ["OPTIONS", "GET"]):
        return
    token = request.headers.get("Authorization")
    if not token or token != os.environ.get("PASSWORD"):
        return Response(status=401)


@app.route("/scenes", methods=["GET"])
def get_scenes() -> list[dict]:
    return get_scenes_(db=DB)


@app.route("/scenes/<int:id_>", methods=["GET"])
def get_scene(id_: int) -> dict:
    return get_scene_(int(id_), db=DB)


@app.route("/scenes/<int:id_>", methods=["PUT"])
def update_scene(id_: int) -> dict | Response:
    data = request.get_json()
    if not data:
        return Response(status=400)
    return update_scene_(id_, data, db=DB)


@app.route("/scenes/<int:id_>", methods=["DELETE"])
def delete_scene(id_: int) -> dict:
    return update_scene_(id_, {}, db=DB)


@app.route("/scenes", methods=["POST"])
def add_scene() -> Response:
    data = request.get_json()
    if not data:
        return Response(status=400)
    try:
        result = add_scene_(data, db=DB)
        if result:
            return Response(status=201, response=result)
        else:
            return Response(status=500)
    except ValueError as e:
        return Response(status=400, response=str(e))


if __name__ == "__main__":
    app.run()
