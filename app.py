from database.database import get_scene
from flask import Flask
import os


app = Flask(__name__)


with app.app_context():
    DB = {
        "url": os.environ.get("MONGO_PRIVATE_URL"),
        "db": os.environ.get("MONGO_DB"),
    }


@app.route('/')
def hello_world():  # put application's code here
    return DB["db"]


@app.route("/scenes/<int:id_>", methods=["GET"])
def get_scene_(id_: int) -> dict:
    return get_scene(id_, db=DB)


if __name__ == "__main__":
    app.run()
