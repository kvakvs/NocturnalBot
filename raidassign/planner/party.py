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


class PlayerSpec(StrEnum):
    BALANCE = "Balance"
    RESTORATION = "Restoration"
    HOLY = "Holy"
    DISCIPLINE = "Discipline"
    SHADOW = "Shadow"


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

    def get_decursers(self, favour: str) -> list[PartyMember]:
        """
        Returns a list of players who can remove curses (druid and mage in classic).
        Parameters:
            favour can be "dps", "healer", or "any"
        """
        if favour == "dps":
            # Favours mages and balance druids
            def filter_fn(member): return member.class_name == PlayerClass.MAGE or member.spec == PlayerSpec.BALANCE
        elif favour == "healer":
            # Favours healing druids only
            def filter_fn(member): return member.class_name == PlayerClass.DRUID and member.spec == PlayerSpec.RESTORATION
        else:
            # Takes any of the above
            def filter_fn(member): return member.class_name == PlayerClass.MAGE or member.class_name == PlayerClass.DRUID

        return [member.name for member in self.members if filter_fn(member)]

    def get_dispelers(self, favour: str) -> list[PartyMember]:
        """
        Returns a list of players who can dispel magic (priest only for classic Horde).
        Parameters:
            favour can be "dps", "healer", or "any"
        """
        if favour == "dps":
            # Favours only shadow priests
            def filter_fn(member): return member.class_name == PlayerClass.PRIEST and member.spec == PlayerSpec.SHADOW
        elif favour == "healer":
            # Favours only holy and discipline priests
            def filter_fn(member): return member.class_name == PlayerClass.PRIEST and member.spec in [
                PlayerSpec.HOLY, PlayerSpec.DISCIPLINE]
        else:
            # Takes any of the above
            def filter_fn(member): return member.class_name == PlayerClass.PRIEST

        return [member.name for member in self.members if filter_fn(member)]

    def get_class(self, class_names: list[PlayerClass]) -> list[PartyMember]:
        """
        Returns a list of players who can use a specific class.
        """
        return [member.name for member in self.members if member.class_name in class_names]
