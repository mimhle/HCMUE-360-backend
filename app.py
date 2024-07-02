from database.database import get_scene
from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return str(os.environ.get("MONGO_PRIVATE_URL", "") != "")


@app.route("/scene/<int:id_>")
def get_scene_(id_: int) -> dict:
    return get_scene(id_)


if __name__ == "__main__":
    app.run()
