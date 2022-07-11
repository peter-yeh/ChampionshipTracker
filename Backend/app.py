import sqlite3
from typing import NamedTuple
from flask import Flask, request, jsonify
from flask_cors import CORS


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = '62e8f6980b724f83f2bb4a'
CORS(app)


class TeamInfo(NamedTuple):
    """Team info class"""
    name: str
    regDate: str
    groupNumber: int


@app.route('/add/teamInfo', methods=['POST'])
def add_team_info():
    """
    Parse team info and add it into the database
    """
    conn = get_db_connection()

    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify('Input is empty'), 400

    parsed_input = parse_team_info(user_input)
    if len(parsed_input) <= 0:
        return jsonify('No valid input exist'), 400

    for row in parsed_input:
        conn.execute(
            'INSERT INTO teamInfo (teamName, registrationDate, groupNumber) VALUES(?, ?, ?)',
            (row[0], row[1], row[2]))

    conn.commit()
    conn.close()
    return jsonify(parsed_input), 200


@ app.route('/add/matchResult', methods=['POST'])
def add_team_score():
    """
    Parse team score and add it into database
    """
    return jsonify('Not implemented'), 200


@app.route('/get/teamInfo')
def get_team_info():
    """
    Get team info
    """
    conn = get_db_connection()
    db_team_info = conn.execute(
        'SELECT teamName, registrationDate, groupNumber FROM teamInfo').fetchall()
    conn.close()

    team_info_arr = []
    for row in db_team_info:
        team_info = TeamInfo(
            row[0], row[1], row[2])
        team_info_arr.append(team_info)

    return jsonify(team_info_arr), 200


def parse_team_info(user_input):
    """Parse input based on this format
    firstTeam 17/05 2
    secondTeam 07/02 2
    thirdTeam 24/04 1
    fourthTeam 24/01 1
    """
    split_by_next_line = user_input.splitlines()
    team_info_arr = []

    for line in split_by_next_line:
        split_by_space = line.split()
        # Skip lines if line contains more than 3 param
        if len(split_by_space) != 3:
            continue

        team_info = TeamInfo(
            split_by_space[0], split_by_space[1], split_by_space[2])
        team_info_arr.append(team_info)

    return team_info_arr
