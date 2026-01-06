import psycopg2
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "database": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD")
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# -------------------------
# GET ORDERS
# -------------------------
@app.route("/api/orders")
def orders():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM orders ORDER BY id")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(rows)

    except Exception as e:
        return {"error": "Database unavailable"}, 503

# -------------------------
# COMPLETE ORDER
# -------------------------
@app.route("/api/order/<int:oid>/complete", methods=["POST"])
def complete(oid):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE orders SET status='COMPLETED' WHERE id=%s",
            (oid,)
        )

        message = f"Order {oid} completed (mock email)"

        conn.commit()
        cur.close()
        conn.close()

        # Notify notification service (non-blocking style)
        try:
            requests.post(
                "http://notification:5000/notify",
                json={"message": message},
                timeout=2
            )
        except requests.RequestException:
            pass  # notification failure should not break admin backend

        return {"status": "completed"}

    except Exception:
        return {"error": "Database unavailable"}, 503

# -------------------------
# GET NOTIFICATIONS
# -------------------------
@app.route("/api/notifications")
def notifications():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, message, created_at FROM notification_logs ORDER BY created_at DESC"
        )
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify([
            {
                "id": r[0],
                "message": r[1],
                "created_at": r[2].isoformat()
            }
            for r in rows
        ])

    except Exception:
        return {"error": "Database unavailable"}, 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

