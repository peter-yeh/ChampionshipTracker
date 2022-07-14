from typing import NamedTuple


class Ranking(NamedTuple):
    """Ranking type, for easier access instead of using arbitrary index"""
    score: int
    totalGoals: int
    alternateMatchPoint: int
    regDate: str
    groupNumber: int


def team_won(rank, goals):
    return Ranking(rank.score + 3, rank.totalGoals + goals,
                   rank.alternateMatchPoint + 5, rank.regDate, rank.groupNumber)


def team_lose(rank, goals):
    return Ranking(rank.score, rank.totalGoals + goals,
                   rank.alternateMatchPoint + 1, rank.regDate, rank.groupNumber)


def team_draw(rank, goals):
    return Ranking(rank.score + 1, rank.totalGoals + goals,
                   rank.alternateMatchPoint + 3, rank.regDate, rank.groupNumber)


def calculate_ranking(db_info, db_result):
    """This function would be able to sort any number of groupings"""

    # The results of all the team in a dictionary 
    team_result = {}

    # Split the teams into their groupings
    # Key: group name
    # Value: array of teams
    groups = {}

    # This is same as groups
    # The values (array of teams) is sorted by score 
    sorted_groups = {}

    # Populate the team_result using team info
    for team_info in db_info:
        temp = Ranking(0, 0, 0, team_info[1], team_info[2])
        team_result[team_info[0]] = temp

    # Populate the team_result using result
    for result in db_result:
        teamA = result[0]
        teamB = result[2]

        if result[1] > result[3]:
            # Team A won
            team_result[teamA] = team_won(team_result[teamA], result[1])
            team_result[teamB] = team_lose(team_result[teamB], result[3])

        elif result[3] > result[1]:
            # Team B won
            team_result[teamA] = team_lose(team_result[teamA], result[1])
            team_result[teamB] = team_won(team_result[teamB], result[3])

        else:
            # Draw
            team_result[teamA] = team_draw(team_result[teamA], result[1])
            team_result[teamB] = team_draw(team_result[teamB], result[3])

    # Split the team_result by grouping
    for team_name, rank in team_result.items():
        if not rank.groupNumber in groups:
            groups[rank.groupNumber] = {}

        groups[rank.groupNumber][team_name] = rank

    # For all the groups, rank the results
    for group_number, rank in groups.items():
        # Sort each group by score, totalGoals, alternateMatchPoint, then reg date
        temp = sorted(rank.items(), key=lambda team:
                      (team[1].score, team[1].totalGoals, team[1].alternateMatchPoint,
                      team[1].regDate[3:], team[1].regDate))

        sorted_groups[group_number] = temp
    
    return sorted_groups
    