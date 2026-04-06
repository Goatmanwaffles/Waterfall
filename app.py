from flask import Flask
import config

app = Flask(__name__)

db = config.dbserver

@app.route("/")
def hello_world():
#    cursor = db.cursor
    return "<h1>Waterfall</h1>"

if __name__ == '__main__':
    app.run(host="localhost", port=4500)
