from enum import StrEnum


class PlayerClass(StrEnum):
    TANK = "Tank"
    SHAMAN = "Shaman"
    MAGE = "Mage"
    HUNTER = "Hunter"
    PRIEST = "Priest"
    DRUID = "Druid"
    WARRIOR = "Warrior"
    WARLOCK = "Warlock"
    ROGUE = "Rogue"
    # PALADIN = "Paladin"
    # DEATH_KNIGHT = "Death Knight"


def get_role(class_name: PlayerClass) -> PlayerClass | None:
    """
    From PlayerClass return either a role, or None if the value is not a role.
    PlayerClass enum contains both class names and roles.
    """
    return PlayerClass.TANK if class_name == PlayerClass.TANK else None


class PartyMember:
    """
    A generalized party member mimicking a raid plan member, but in case of a missing raid plan,
    the party number might also be missing.
    """

    def __init__(self, name: str,
                 discord_user_id: int,
                 class_name: PlayerClass,
                 role: PlayerClass | None,
                 group: int | None):
        self.name: str = name
        self.discord_user_id: int = discord_user_id
        self.class_name: str = class_name
        self.role: str = role
        self.group: int | None = group


class Party:
    def __init__(self, members: list[PartyMember]):
        self.members: list[PartyMember] = members
