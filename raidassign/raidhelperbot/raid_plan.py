from typing import Dict, Any, List

from raidassign.planner.party import PlayerClass


class RaidDrop:
    """
    This is a single player assignment in the raid plan.

    partyId: int
    slotId: int
    class: string
    spec: string
    name: string
    color: string - "#RRGGBB" hex color
    userid: int - Discord user id
    isConfirmed: boolean - set to true if json string equals "confirmed"
    """

    def __init__(self, json_data: Dict[str, Any]) -> None:
        self.party_id: int = int(json_data.get('partyId'))
        self.slot_id: int = int(json_data.get('slotId'))
        self.class_name: PlayerClass = PlayerClass(json_data.get('class'))
        self.spec: str = json_data.get('spec')
        self.name: str = json_data.get('name')
        self.color: str = json_data.get('color')
        self.user_id: int = int(json_data.get('userid'))
        self.is_confirmed: bool = json_data.get('isConfirmed') == "confirmed"

    def __str__(self) -> str:
        return (f"RaidDrop(party={self.party_id}, slot={self.slot_id}, "
                f"class={self.class_name}, spec={self.spec}, "
                f"name={self.name}, color={self.color}, "
                f"user_id={self.user_id}, confirmed={self.is_confirmed})")


class RaidPlan:
    """
    This is the raid plan, as created by the Raid Composition tool (https://raid-helper.dev/raidplan),
    and contains the raid plan for the event.

    raidDrop: array of RaidDrop - The player group position and class for the event.
    """

    def __init__(self, json_data: Dict[str, Any]) -> None:
        self.raid_drops: List[RaidDrop] = [
            RaidDrop(drop_data)
            for drop_data in json_data.get('raidDrop', [])
        ]

    def __str__(self) -> str:
        drops_str = "\n".join(f"  {drop}" for drop in self.raid_drops)
        return f"RaidPlan(\n{drops_str}\n)"
