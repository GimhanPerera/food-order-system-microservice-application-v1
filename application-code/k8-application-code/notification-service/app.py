import psycopg2
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow all origins

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD")
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------
# NOTIFY (LOG EMAIL)
# -------------------------
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json

    if not data or "message" not in data:
        return {"error": "message required"}, 400

    msg = data["message"]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO notification_logs (message) VALUES (%s)",
            (msg,)
        )

        conn.commit()
        cur.close()
        conn.close()

        print("EMAIL LOG:", msg)
        return {"logged": True}

    except Exception:
        return {"error": "Database unavailable"}, 503

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

