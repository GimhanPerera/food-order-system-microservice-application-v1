import psycopg2
import os
from flask import Flask, request, jsonify

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
# GET AVAILABLE FOODS
# -------------------------
@app.route("/customer-api/foods")
def foods():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, name, price FROM foods WHERE available=true"
        )
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify(rows)

    except Exception:
        return {"error": "Database unavailable"}, 503

# -------------------------
# PLACE ORDER
# -------------------------
@app.route("/customer-api/order", methods=["POST"])
def order():
    data = request.json

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO orders (food_id, quantity, status) VALUES (%s, %s, 'PENDING')",
            (data["food_id"], data["quantity"])
        )

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Order placed"}

    except Exception:
        return {"error": "Database unavailable"}, 503

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/customer-api/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

