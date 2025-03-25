from enum import StrEnum
from typing import Callable


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


class PlayerSpec(StrEnum):
    BALANCE = "Balance"
    RESTORATION = "Restoration"
    FERAL = "Feral"
    ENHANCEMENT = "Enhancement"
    ELEMENTAL = "Elemental"

    HOLY = "Holy"
    DISCIPLINE = "Discipline"
    SHADOW = "Shadow"

    PROTECTION = "Protection"
    FURY = "Fury"
    ARMS = "Arms"


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
                 spec: str,
                 role: PlayerClass | None,
                 group: int | None):
        self.name: str = name
        self.discord_user_id: int = discord_user_id
        self.class_name: str = class_name
        self.spec: str = spec
        self.role: str = role
        self.group: int | None = group


class Party:
    def __init__(self, members: list[PartyMember]):
        self.members: list[PartyMember] = members

    def get_decursers(self, favour: str) -> list[str]:
        """
        Returns a list of players who can remove curses (druid and mage in classic).
        Parameters:
            favour can be "dps", "healer", or "any"
        """
        filter_fn: Callable[[PartyMember], bool]
        if favour == "dps":
            # Favours mages and balance druids
            filter_fn = lambda member: member.class_name == PlayerClass.MAGE or member.spec == PlayerSpec.BALANCE
        elif favour == "healer":
            # Favours healing druids only
            filter_fn = lambda member: member.class_name == PlayerClass.DRUID and member.spec == PlayerSpec.RESTORATION
        else:
            # Takes any of the above
            filter_fn = lambda member: member.class_name == PlayerClass.MAGE or member.class_name == PlayerClass.DRUID

        return [member.name for member in self.members if filter_fn(member)]

    def get_dispelers(self, favour: str) -> list[str]:
        """
        Returns a list of players who can dispel magic (priest only for classic Horde).
        Parameters:
            favour can be "dps", "healer", or "any"
        """
        filter_fn: Callable[[PartyMember], bool]
        if favour == "dps":
            # Favours only shadow priests
            filter_fn = lambda member: member.class_name == PlayerClass.PRIEST and member.spec == PlayerSpec.SHADOW
        elif favour == "healer":
            # Favours only holy and discipline priests
            filter_fn = lambda member: member.class_name == PlayerClass.PRIEST and member.spec in [
                PlayerSpec.HOLY, PlayerSpec.DISCIPLINE]
        else:
            # Takes any of the above
            filter_fn = lambda member: member.class_name == PlayerClass.PRIEST

        return [member.name for member in self.members if filter_fn(member)]

    def get_class(self, class_names: list[PlayerClass]) -> list[str]:
        """
        Returns a list of players who can use a specific class.
        """
        return [member.name for member in self.members if member.class_name in class_names]

    def get_role(self, role_names: list[PlayerClass]) -> list[str]:
        """
        Returns a list of players who can use a specific role.
        """
        return [member.name for member in self.members if member.role in role_names]

    def get_spec(self, spec_names: list[PlayerSpec]) -> list[str]:
        """
        Returns a list of players who can use a specific spec.
        """
        return [member.name for member in self.members if member.spec in spec_names]
