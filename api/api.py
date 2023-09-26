import sqlite3  
import flask  
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tischreservierung</h1>"

@app.route('/available_seats', methods=['GET'])
def check_available_seats():
    conn = sqlite3.connect('../database/tables.db')
    c = conn.cursor()

    c.execute('''
        SELECT tische.tischnummer, anzahlPlaetze - IFNULL(sum(case when storniert = "False" then 1 else 0 end), 0) as freiePlaetze
        FROM tische
        LEFT JOIN reservierungen
        ON tische.tischnummer = reservierungen.tischnummer
        GROUP BY tische.tischnummer
        HAVING freiePlaetze > 0

    ''')
    result = c.fetchall()

    conn.close()

    return jsonify(result)

app.run()