from typing import Dict, List


def assign_tasks(players: list[str], tasks: list[str]) -> Dict[str, str]:
    """
    Assigns N tasks to M players. The result would look like:
        G1 G2= player1; G3 G4= player2; ...
    """

    assigns = {}
    players_adjusted = players.copy()
    tasks_adjusted = tasks.copy()
    available_players = True
    available_tasks = True

    while available_players and available_tasks:
        # Round-robin the same players if more tasks are available
        if len(players_adjusted) == 0:
            players_adjusted = players.copy()
            available_players = False  # Ran out of players
        pick_player = players_adjusted.pop(0)

        # Round-robin the same tasks if more players are available
        if len(tasks_adjusted) == 0:
            tasks_adjusted = tasks.copy()
            available_tasks = False  # Ran out of tasks
        task = tasks_adjusted.pop(0)

        if task not in assigns:
            assigns[task] = [pick_player]
        else:
            assigns[task].append(pick_player)

    return assigns


def invert_dict(assigns: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Given a dict of {key: [value1, value2, ...]}, return a dict of {value: [key1, key2, ...]}
    """
    inverted = {}
    for k, values in assigns.items():
        for value in values:
            if value not in inverted:
                inverted[value] = [k]
            else:
                inverted[value].append(k)
    return inverted
