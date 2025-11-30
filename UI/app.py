ifrom flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "/data/database.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS values_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/add", methods=["POST"])
def add_value():
    content = request.json
    value = content.get("value")

    if not value:
        return jsonify({"error": "Missing value"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO values_table (value) VALUES (?)", (value,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Value inserted successfully"})

@app.route("/list", methods=["GET"])
def list_values():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, value FROM values_table")
    rows = cur.fetchall()
    conn.close()

    return jsonify([{"id": r[0], "value": r[1]} for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)

