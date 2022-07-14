import json
import sqlite3
from tokenize import group
from helper import MatchResult, TeamInfo, Ranking, parse_match_result, parse_team_info, team_won, team_lose, team_draw
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = '62e8f6980b724f83f2bb4a'
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=="__main__":
    app.run()

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
        if len(row[1]) != 5:
            return jsonify('Registration date for ', row[0], ' is wrong: ', row[1]), 400

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
    conn = get_db_connection()

    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify('Input is empty'), 400

    parsed_input = parse_match_result(user_input)
    if len(parsed_input) <= 0:
        return jsonify('No valid input exist'), 400

    for row in parsed_input:
        conn.execute(
            'INSERT INTO matchResult (teamA, scoreA, teamB, scoreB) VALUES(?, ?, ?, ?)',
            (row[0], row[1], row[2], row[3]))

    conn.commit()
    conn.close()
    return jsonify(parsed_input), 200


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


@app.route('/get/matchResult')
def get_match_result():
    """
    Get match result
    """
    conn = get_db_connection()
    db_result = conn.execute(
        'SELECT teamA, scoreA, teamB, scoreB FROM matchResult').fetchall()
    conn.close()

    match_result_arr = []
    for row in db_result:
        match_result = MatchResult(
            row[0], row[1], row[2], row[3])
        match_result_arr.append(match_result)

    return jsonify(match_result_arr), 200

@app.route('/delete/all')
def drop_table():
    """
    Delete rows from both table
    """
    conn = get_db_connection()
    temp = conn.execute('DELETE FROM teamInfo')
    conn.execute('DELETE FROM matchResult')
    print(temp)
    conn.commit()
    conn.close()

    return jsonify("Delete all"), 200


@app.route('/get/ranking')
def get_ranking():
    """Generate ranking based on
    1. Highest total match points
    """

# Pull data from db
    conn = get_db_connection()
    db_team_info = conn.execute(
        'SELECT teamName, registrationDate, groupNumber FROM teamInfo').fetchall()
    db_result = conn.execute(
        'SELECT teamA, scoreA, teamB, scoreB FROM matchResult').fetchall()
    conn.close()

    if len(db_team_info) <= 0 or len(db_result) <= 0:
        return jsonify("Team info and match result cannot be empty"), 400

    # Extract this function into another class
    # This function would be able to sort any number of groupings
    # If there is 3 groups, this can still handle

    team_ranking = {}

    # Populate the team_ranking first
    for team_info in db_team_info:
        temp = Ranking(0, 0, 0, team_info[1], team_info[2])
        team_ranking[team_info[0]] = temp

    # Populate the remaining attributes
    for result in db_result:
        teamA = result[0]
        teamB = result[2]

        if result[1] > result[3]:
            # Team A won
            team_ranking[teamA] = team_won(team_ranking[teamA], result[1])
            team_ranking[teamB] = team_lose(team_ranking[teamB], result[3])

        elif result[3] > result[1]:
            # Team B won
            team_ranking[teamA] = team_lose(team_ranking[teamA], result[1])
            team_ranking[teamB] = team_won(team_ranking[teamB], result[3])

        else:
            # Draw
            team_ranking[teamA] = team_draw(team_ranking[teamA], result[1])
            team_ranking[teamB] = team_draw(team_ranking[teamB], result[3])

    group_ranking = {}
    # Populate the ranking by group first
    for team_name, rank in team_ranking.items():
        if not rank.groupNumber in group_ranking:
            group_ranking[rank.groupNumber] = {}

        group_ranking[rank.groupNumber][team_name] = rank

    # Basic test case
    # rank1 = Ranking(2, 3, 4, '30/01', 1)
    # rank6 = Ranking(2, 3, 5, '28/01', 1)
    # rank2 = Ranking(2, 3, 5, '30/01', 1)
    # rank7 = Ranking(2, 3, 5, '28/02', 1)
    # rank3 = Ranking(2, 3, 5, '01/05', 1)
    # rank5 = Ranking(2, 3, 5, '28/06', 1)
    # rank4 = Ranking(2, 3, 5, '29/06', 1)
    # group_ranking = {}
    # group_ranking[1] = {'aa': rank1, 'bb': rank2, 'cc': rank3, 
    # 'dd': rank4, 'ee': rank5, 'ff': rank6, 'gg': rank7}

    result = {}
    for group_number, rank in group_ranking.items():
        # rank is a dictionary of the teams in this grouping
        # Sort each group by score, totalGoals, alternateMatchPoint, then reg date
        temp = sorted(rank.items(), key=lambda team: 
            (team[1].score, team[1].totalGoals, team[1].alternateMatchPoint, team[1].regDate[3:],
            team[1].regDate ))

        result[group_number] = temp

    return jsonify(result), 200
