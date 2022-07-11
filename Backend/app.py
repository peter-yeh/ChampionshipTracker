import sqlite3
from hashids import Hashids
from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = '62e8f6980b724f83f2bb4a'
CORS(app)

hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


@app.route('/add/teamInfo', methods = ['POST'])
def add_url():
    conn = get_db_connection()
    input = request.json.get('input')
    output = {}

    if not input:
        return jsonify('Input is empty'), 400
        
    # temp = conn.execute('INSERT INTO (teamInfo) VALUES (?)',
    #                         (url,))

    conn.commit()
    conn.close()

    return jsonify('testing'), 200

@app.route('/add/matchResult', methods = ['POST'])
def add_url():
    return jsonify('Not implemented'), 200





def parse_team_info(input):
    split_by_next_line = input.splitlines()
    # firstTeam 17/05 2
    # secondTeam 07/02 2
    # thirdTeam 24/04 1
    # fourthTeam 24/01 1P
    team_info_arr = []

    for team_info in split_by_next_line:
        split_by_space = team_info.split()
        # Skip lines if line contains more than 3 param
        if len(team_info) != 3:
            continue
        team_info_arr.append(split_by_space)
    
    return team_info_arr

        



