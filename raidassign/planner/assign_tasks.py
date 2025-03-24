from typing import Dict, List


def assign_tasks(players: list[str], tasks: list[str]) -> Dict[str, str]:
    """
    Assigns N tasks to M players. The result would look like:
        G1 G2= player1; G3 G4= player2; ...
    """
    assigns = {}
    queue = players.copy()

    for task in tasks:
        if len(queue) == 0:
            queue = players.copy()
        pick_player = queue.pop(0)
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
