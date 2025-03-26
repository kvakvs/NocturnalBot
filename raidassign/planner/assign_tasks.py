from typing import Any


def invert_dict(assigns: dict[Any, set[Any]]) -> dict[Any, set[Any]]:
    """
    Given a dict of {key: [value1, value2, ...]}, return a dict of {value: [key1, key2, ...]}
    """
    inverted = {}
    for k, values in assigns.items():
        for value in values:
            if value not in inverted:
                inverted[value] = set([k])
            else:
                inverted[value].add(k)
    return inverted


def assign_tasks(players: list[str],
                 tasks: list[str],
                 one_per_player: bool = False,
                 invert_result: bool = False) -> tuple[dict[str, set[str]], set[str]]:
    """
    Assigns N tasks to M players. The result would look like:
        G1 G2= player1; G3 G4= player2; ...
    """

    assigns = {}
    # assigned_players = set() # remember that someone already got a task
    players_adjusted = players.copy()
    tasks_adjusted = tasks.copy()
    available_players = True
    available_tasks = True
    extra_players = set()  # in one_per_player mode these are extra players not getting a task (FFA basically)

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
            assigns[task] = set([pick_player])
        else:
            if not one_per_player:
                assigns[task].add(pick_player)
            else:
                extra_players.add(pick_player)

    if invert_result:
        return invert_dict(assigns), extra_players

    return assigns, extra_players
