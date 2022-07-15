import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

from helperInfo import pack_info, parse_team_info
from helperRanking import calculate_ranking
from helperResult import pack_result, parse_match_result


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = '62e8f6980b724f83f2bb4a'
CORS(app)


@app.route('/add/teamInfo', methods=['POST'])
def add_team_info():
    """    Parse team info and add it into the database    """
    conn = get_db_connection()

    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify('Input is empty'), 400

    parsed_input = parse_team_info(user_input)
    if isinstance(parsed_input, str):
        return jsonify(parsed_input), 400

    for row in parsed_input:
        # Check for format, if error, request user to update again
        # Do you know what you are doing?
        # If users know what they are doing, there should not be a single mistake
        if len(row[1]) != 5 or row[1][2] != '/':
            conn.close()
            return jsonify('Registration date for team: ' + row[0]
                           + ' (' + row[1] + ') is not of the format DD/MM'), 400

        # Check if valid date
        if not row[1][0:2].isdigit() or not 0 < int(row[1][0:2]) < 32:
            conn.close()
            return jsonify('Registration date for team: ' + row[0]
                           + ' (' + row[1] + ') is not a valid date'), 400

        # Check if valid month
        if not row[1][3:].isdigit() or not 0 < int(row[1][3:]) < 13:
            conn.close()
            return jsonify('Registration month for team: ' + row[0]
                           + ' (' + row[1] + ') is not a valid month'), 400

        try:
            conn.execute(
                'INSERT INTO teamInfo (teamName, registrationDate, groupNumber) VALUES(?, ?, ?)',
                (row[0], row[1], row[2]))
        except:
            conn.close()
            return jsonify('Entry already existed in database: ', row), 400

    conn.commit()
    conn.close()
    return jsonify(parsed_input), 200


@ app.route('/add/matchResult', methods=['POST'])
def add_team_score():
    """    Parse team score and add it into database    """
    conn = get_db_connection()

    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify('Input is empty'), 400

    parsed_input = parse_match_result(user_input)
    if isinstance(parsed_input, str):
        return jsonify(parsed_input), 400

    for row in parsed_input:
        # Check if score is a number
        if int(row[1]) < 0:
            conn.close()
            return jsonify('Team: ' + row[0] + ' score is not a number: ' + row[1]), 400

        if int(row[3]) < 0:
            conn.close()
            return jsonify('Team: ' + row[2] + ' score is not a number: ' + row[3]), 400

        try:
            conn.execute(
                'INSERT INTO matchResult (teamA, scoreA, teamB, scoreB) VALUES(?, ?, ?, ?)',
                (row[0], row[1], row[2], row[3]))
        except:
            conn.close()
            return jsonify('Entry already existed in database: ', row), 400

    conn.commit()
    conn.close()
    return jsonify(parsed_input), 200


@app.route('/get/teamInfo')
def get_team_info():
    """    Get team info, short form as info    """
    conn = get_db_connection()
    db_info = conn.execute(
        'SELECT teamName, registrationDate, groupNumber FROM teamInfo').fetchall()
    conn.close()

    team_info_arr = pack_info(db_info)

    return jsonify(team_info_arr), 200


@app.route('/get/matchResult')
def get_match_result():
    """    Get match result    """
    conn = get_db_connection()
    db_result = conn.execute(
        'SELECT teamA, scoreA, teamB, scoreB FROM matchResult').fetchall()
    conn.close()

    match_result_arr = pack_result(db_result)

    return jsonify(match_result_arr), 200


@app.route('/delete/all')
def drop_table():
    """    Delete rows from both table    """
    conn = get_db_connection()
    temp = conn.execute('DELETE FROM teamInfo')
    conn.execute('DELETE FROM matchResult')
    conn.commit()
    conn.close()

    return jsonify("Delete all"), 200


@app.route('/get/ranking')
def get_ranking():
    """    Generate ranking    """

    conn = get_db_connection()
    db_team_info = conn.execute(
        'SELECT teamName, registrationDate, groupNumber FROM teamInfo').fetchall()
    db_result = conn.execute(
        'SELECT teamA, scoreA, teamB, scoreB FROM matchResult').fetchall()
    conn.close()

    if len(db_team_info) <= 0 or len(db_result) <= 0:
        return jsonify("Team info and match result cannot be empty"), 400

    ranking_result = calculate_ranking(db_team_info, db_result)

    return jsonify(ranking_result), 200
