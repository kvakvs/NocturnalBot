from enum import StrEnum
from typing import Callable

from raidassign.planner.assign_tasks import assign_tasks


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
    # --- Artifacts from the signup bot ---
    TENTATIVE = "Tentative"
    ABSENCE = "Absence"
    BENCH = "Bench"


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
        self.role: PlayerClass | None = role
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

        def filter_mages_and_balance(member):
            """Favours mages and balance druids"""
            return member.class_name == PlayerClass.MAGE or member.spec == PlayerSpec.BALANCE

        def filter_healing_druids(member):
            """Favours healing druids only"""
            return member.class_name == PlayerClass.DRUID and member.spec == PlayerSpec.RESTORATION

        def filter_any_decursers(member):
            """Takes any of the above"""
            return member.class_name == PlayerClass.MAGE or member.class_name == PlayerClass.DRUID

        filter_fn: Callable[[PartyMember], bool]
        if favour == "dps":
            filter_fn = filter_mages_and_balance
        elif favour == "healer":
            filter_fn = filter_healing_druids
        else:
            filter_fn = filter_any_decursers

        return [member.name for member in self.members if filter_fn(member)]

    def get_dispelers(self, favour: str) -> list[str]:
        """
        Returns a list of players who can dispel magic (priest only for classic Horde).
        Parameters:
            favour can be "dps", "healer", or "any"
        """
        def filter_only_shadow_priests(member):
            """Favours only shadow priests"""
            return member.class_name == PlayerClass.PRIEST and member.spec == PlayerSpec.SHADOW

        def filter_only_healing_priests(member):
            """Favours only holy and discipline priests"""
            return member.class_name == PlayerClass.PRIEST and member.spec in [
                PlayerSpec.HOLY, PlayerSpec.DISCIPLINE]

        def filter_any_priests(member):
            """Takes any of the above"""
            return member.class_name == PlayerClass.PRIEST

        filter_fn: Callable[[PartyMember], bool]

        if favour == "dps":
            filter_fn = filter_only_shadow_priests
        elif favour == "healer":
            filter_fn = filter_only_healing_priests
        else:
            filter_fn = filter_any_priests

        return [member.name for member in self.members if filter_fn(member)]

    def get_class(self, class_names: list[PlayerClass] | set[PlayerClass]) -> list[str]:
        """
        Returns a list of players who can use a specific class.
        """
        return [member.name for member in self.members if member.class_name in class_names]

    def get_role(self, role_names: list[PlayerClass] | set[PlayerClass]) -> list[str]:
        """
        Returns a list of players who can use a specific role.
        """
        return [member.name for member in self.members if member.role in role_names]

    def get_spec(self, spec_names: list[PlayerSpec] | set[PlayerClass]) -> list[str]:
        """
        Returns a list of players who can use a specific spec.
        """
        return [member.name for member in self.members if member.spec in spec_names]

    def get_raid_decursers_fav_dps_formatted(self) -> str:
        decursers, _ = assign_tasks(self.get_decursers(favour="dps"),
                                    [f"G{i}" for i in range(1, 8)],
                                    invert_result=True)

        return "; ".join([
            f"{group}={', '.join(players)}"
            for group, players in decursers.items()
        ])

    def get_raid_dispelers_formatted(self) -> str:
        dispelers, _ = assign_tasks(self.get_dispelers(favour="any"),
                                    [f"G{i}" for i in range(1, 8)],
                                    invert_result=True)
        return "; ".join([
            f"{group}={','.join(players)}"
            for group, players in dispelers.items()
        ])

    def assign_to_class_formatted(self, class_names: list[PlayerClass] | set[PlayerClass],
                                  targets: list[str],
                                  one_per_player: bool = False) -> str:
        players_of_class, _ = assign_tasks(self.get_class(class_names=class_names),
                                           targets,
                                           one_per_player=one_per_player)
        return "; ".join([
            f"{group}={','.join(players)}"
            for group, players in players_of_class.items()
        ])

    def get_tanks_except(self, exclude_tanks: list[PlayerClass] | set[PlayerClass]) -> list[str]:
        all_tanks = self.get_role(role_names=[PlayerClass.TANK])
        return [tank for tank in all_tanks if tank not in exclude_tanks]

    def assign_to_tanks_formatted(self, exclude_tanks: list[PlayerClass] | set[PlayerClass],
                                  targets: list[str],
                                  one_per_player: bool = False) -> str:
        """Select all tanks, exclude main tank (or any in 'exclude_tanks') and assign targets."""
        offtanks = self.get_tanks_except(exclude_tanks)
        players_of_role, _ = assign_tasks(offtanks,
                                          targets,
                                          one_per_player=one_per_player)
        return "; ".join([
            f"{group}={','.join(players)}"
            for group, players in players_of_role.items()
        ])

    def get_interrupts_formatted(self, targets: list[str],
                                 use_shamans: bool = False,
                                 use_mages: bool = False) -> str:
        """
        Assign rogues, warriors, mages and shamans to interrupt the targets.
        Shamans' earth shock has shorter spell lockout.
        """
        class_names = [PlayerClass.ROGUE, PlayerClass.WARRIOR]
        if use_shamans:
            class_names.append(PlayerClass.SHAMAN)
        if use_mages:
            class_names.append(PlayerClass.MAGE)
        kickers, _ = assign_tasks(
            players=self.get_class(class_names=class_names),
            tasks=targets,
            one_per_player=True
        )
        return "; ".join([
            f"{group}={','.join(players)}"
            for group, players in kickers.items()
        ])
