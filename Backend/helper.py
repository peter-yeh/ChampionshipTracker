from typing import NamedTuple


class TeamInfo(NamedTuple):
    """Team info class"""
    name: str
    regDate: str
    groupNumber: int


class MatchResult(NamedTuple):
    """Match result class"""
    teamA: str
    scoreA: int
    teamB: str
    scoreB: int


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


def parse_match_result(user_input):
    """Parse input based on this format
    teamA teamB 0 1
    teamA teamC 1 3
    """
    split_by_next_line = user_input.splitlines()
    match_result_arr = []

    for line in split_by_next_line:
        split_by_space = line.split()
        # Skip lines if line does not contain 4 param
        if len(split_by_space) != 4:
            continue

        match_result = MatchResult(
            split_by_space[0], split_by_space[1], split_by_space[2], split_by_space[3])
        match_result_arr.append(match_result)

    return match_result_arr
