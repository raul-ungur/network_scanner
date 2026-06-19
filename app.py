from flask import Flask, jsonify, render_template
import sqlite3
from scanner import scan_network
from database import init_database


app = Flask(__name__)

@app.route("/api/scan", methods=["POST"])
def scan():

    scan_network()

    return jsonify({
        "success": True,
        "message": "Scan completed"
    })


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/devices")
def devices():

    conn = sqlite3.connect("network.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT ip, mac, vendor
    FROM devices
    """)

    dati = cursor.fetchall()

    conn.close()

    return jsonify(dati)

if __name__ == "__main__":

    init_database()

    app.run(debug=True)