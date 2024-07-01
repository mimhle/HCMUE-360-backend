from flask import Flask
import os

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return str(os.environ.get("DB_HOST", "") != "")


if __name__ == "__main__":
    app.run()
