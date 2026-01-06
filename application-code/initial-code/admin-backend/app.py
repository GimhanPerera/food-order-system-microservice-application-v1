import time
import psycopg2
import os
import requests
from flask import Flask, jsonify, request
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

@app.route("/orders")
def orders():
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders ORDER BY id")
    return jsonify(cur.fetchall())

@app.route("/order/<int:oid>/complete", methods=["POST"])
def complete(oid):
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status='COMPLETED' WHERE id=%s", (oid,))
    conn.commit()

    requests.post(
        "http://notification:5000/notify",
        json={"message": f"Order {oid} completed (mock email)"}
    )

    return {"status": "completed"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
