import discord
import toml
from raidassign.planner.assign_tasks import assign_tasks, invert_dict
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


def get_3_tanks(tanks: list[str]) -> tuple[str, str, str]:
    """Extracts main tank and two offtanks from the list of tanks."""
    return tanks[0], tanks[1], tanks[2]


class McPlanner:
    @staticmethod
    def get_config(section: str) -> dict:
        config = toml.load("mc_planner.toml")
        return config[section]

    class AllBosses(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            preferred_healers_maintank = all_conf["preferred_healers_maintank"]
            preferred_healers_offtank = all_conf["preferred_healers_offtank"]
            await interaction.followup.send(
                f"**ALL BOSSES**\n"
                f"/rw Maintank healing: {', '.join(preferred_healers_maintank)}; "
                f"offtank healing: {', '.join(preferred_healers_offtank)}\n"
                "\n"
            )

    class Lucifron(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            decursers = invert_dict(assign_tasks(party.get_decursers(favour="dps"), [f"G{i}" for i in range(1, 8)]))
            formatted_decursers = "; ".join([f"{group}={', '.join(players)}" for group, players in decursers.items()])

            dispelers = invert_dict(assign_tasks(party.get_dispelers(favour="any"), [f"G{i}" for i in range(1, 8)]))
            formatted_dispelers = "; ".join([f"{group}={','.join(players)}" for group, players in dispelers.items()])
            await interaction.followup.send(
                f"**LUCIFRON**\n"
                f"/rw Boss: {maintank}; Add {RAID_MARK[8]}: {offtank1}; Add {RAID_MARK[7]}: {offtank2}\n"
                "/rw All mages decurse; All priests dispel; Sheep Mind controls; use restorative Potion\n"
                f"/rw Decursing (SELF FIRST): {formatted_decursers}\n"
                f"/rw Dispel Magic (SELF FIRST): {formatted_dispelers}\n"
                "\n"
            )

    class Magmadar(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Gehennas(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Garr(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Geddon(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Shazzrah(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class SulfuronHarbinger(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Majordomo(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Ragnaros(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass
