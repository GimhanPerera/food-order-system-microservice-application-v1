import time
import psycopg2
import os
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow all origins

while True:
    try:
        conn = psycopg2.connect(
            host=os.environ["DB_HOST"],
            database="fooddb",
            user="fooduser",
            password="foodpass"
        )
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(3)

@app.route("/notify", methods=["POST"])
def notify():
    msg = request.json["message"]
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notification_logs (message) VALUES (%s)",
        (msg,)
    )
    conn.commit()
    print("EMAIL LOG:", msg)
    return {"logged": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
