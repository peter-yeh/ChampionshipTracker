from typing import NamedTuple


class TeamInfo(NamedTuple):
    """Team info class"""
    name: str
    regDate: str
    groupNumber: int


def parse_team_info(user_input):
    """Parse input based on this format
    firstTeam 17/05 2
    secondTeam 07/02 2
    """
    split_by_next_line = user_input.splitlines()
    team_info_arr = []

    for line in split_by_next_line:
        split_by_space = line.split()
        # Fail this input block on error show the error line
        if len(split_by_space) != 3:
            if len(team_info_arr) > 0:
                return 'Format error after ' + team_info_arr[-1][0]
            else:
                return 'Format error in first line'

        team_info = TeamInfo(
            split_by_space[0], split_by_space[1], split_by_space[2])
        team_info_arr.append(team_info)

    return team_info_arr


def pack_info(db_info):
    """Pack the db info into TeamInfo typed array"""
    team_info_arr = []
    for row in db_info:
        team_info = TeamInfo(row[0], row[1], row[2])
        team_info_arr.append(team_info)

    return team_info_arr
