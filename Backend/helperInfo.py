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
        # Skip lines if line does not contain 3 param
        if len(split_by_space) != 3:
            continue

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
