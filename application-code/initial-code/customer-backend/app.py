import time
import psycopg2
import os
from flask import Flask, request, jsonify
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)  # allow all origins

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
