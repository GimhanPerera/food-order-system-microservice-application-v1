import time
import psycopg2
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# DB CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database="fooddb",
        user="fooduser",
        password="foodpass"
    )

# -----------------------------
# WAIT FOR DB TO BE READY
# -----------------------------
while True:
    try:
        conn = get_db_connection()
        conn.close()
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(3)

# -----------------------------
# ORDERS ENDPOINT
# -----------------------------
@app.route("/orders")
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
        print("ERROR:", e)
        return {"error": "Database unavailable"}, 503

# -----------------------------
# COMPLETE ORDER
# -----------------------------
@app.route("/order/<int:oid>/complete", methods=["POST"])
def complete(oid):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE orders SET status='COMPLETED' WHERE id=%s",
            (oid,)
        )
        conn.commit()

        cur.close()
        conn.close()

        # Notify notification service
        try:
            requests.post(
                "http://notification:5000/notify",
                json={"message": f"Order {oid} completed (mock email)"},
                timeout=3
            )
        except requests.exceptions.RequestException as e:
            print("Notification error:", e)

        return {"status": "completed"}

    except Exception as e:
        print("ERROR:", e)
        return {"error": "Failed to complete order"}, 500

# -----------------------------
# NOTIFICATIONS ENDPOINT
# -----------------------------
@app.route("/notifications")
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
                "created_at": r[2].isoformat() if r[2] else None
            }
            for r in rows
        ])

    except Exception as e:
        print("ERROR:", e)
        return {"error": "Database unavailable"}, 503

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
[root@docker-test-vm initial-code]#
[root@docker-test-vm initial-code]# cat custmer-backend/app.py
cat: custmer-backend/app.py: No such file or directory
[root@docker-test-vm initial-code]# cat customer-backend/app.py
import time
import psycopg2
import os
from flask import Flask, request, jsonify
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

@app.route("/customer-api/foods")
def foods():
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM foods WHERE available=true")
    return jsonify(cur.fetchall())

@app.route("/customer-api/order", methods=["POST"])
def order():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (food_id, quantity, status) VALUES (%s,%s,'PENDING')",
        (data["food_id"], data["quantity"])
    )
    conn.commit()
    return {"message": "Order placed"}

@app.route("/customer-api/health")
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
