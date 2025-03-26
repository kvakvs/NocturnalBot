from typing import Any, Dict, List, Tuple


def invert_dict(assigns: Dict[Any, List[Any]]) -> Dict[Any, List[Any]]:
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


def assign_tasks(players: list[str], tasks: list[str], one_per_player: bool = False, invert_result: bool = False) -> Tuple[Dict[str, List[str]], List[str]]:
    """
    Assigns N tasks to M players. The result would look like:
        G1 G2= player1; G3 G4= player2; ...
    """

    assigns = {}
    players_adjusted = players.copy()
    tasks_adjusted = tasks.copy()
    available_players = True
    available_tasks = True
    extra_players = []  # in one_per_player mode these are extra players not getting a task (FFA basically)

    while available_players or available_tasks:
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
            if not one_per_player:
                assigns[task].append(pick_player)
            else:
                extra_players.append(pick_player)

    if invert_result:
        return invert_dict(assigns), extra_players

    return assigns, extra_players
