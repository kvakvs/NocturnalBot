import discord
import toml
from raidassign.planner.assign_tasks import assign_tasks, invert_dict
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party, PlayerClass
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
            embed = discord.Embed(
                title="All Bosses",
                color=0x000000,
            )
            embed.add_field(name="Healing",
                            value=f"/rw Maintank healing: {', '.join(preferred_healers_maintank)}; "
                            f"offtank healing: {', '.join(preferred_healers_offtank)}")
            await interaction.followup.send(embed=embed)

    class Lucifron(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            decursers = invert_dict(assign_tasks(party.get_decursers(favour="dps"), [f"G{i}" for i in range(1, 8)]))
            formatted_decursers = "; ".join([f"{group}={', '.join(players)}" for group, players in decursers.items()])

            dispelers = invert_dict(assign_tasks(party.get_dispelers(favour="any"), [f"G{i}" for i in range(1, 8)]))
            formatted_dispelers = "; ".join([f"{group}={','.join(players)}" for group, players in dispelers.items()])

            embed = discord.Embed(
                title="Lucifron",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-lucifron.png")
            embed.add_field(name="Tanking",
                            value=f"/rw Boss: {maintank}; Add {RAID_MARK[8]}: {offtank1}; Add {RAID_MARK[7]}: {offtank2}")
            embed.add_field(name="All",
                            value="/rw All mages decurse; All priests dispel; Sheep Mind controls; use restorative Potion")
            embed.add_field(name="Decursing",
                            value=f"/rw Decursing (SELF FIRST): {formatted_decursers}")
            embed.add_field(name="Dispel Magic",
                            value=f"/rw Dispel Magic (SELF FIRST): {formatted_dispelers}")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-lucifron.png", filename="mc-lucifron.png")
            )

    class Magmadar(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            embed = discord.Embed(
                title="Magmadar",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-magmadar.png")

            hunter_tasks = invert_dict(assign_tasks(party.get_class(
                class_names=[PlayerClass.HUNTER]), ["Tranq1", "Tranq2"]))
            formatted_tranq = "; ".join([f"{task}={', '.join(hunters)}" for task, hunters in hunter_tasks.items()])

            embed.add_field(name="Tanking + Tranq",
                            value=f"/rw Tanking boss - Cronos; {formatted_tranq}")
            embed.add_field(name="All",
                            value="/rw Stay spread, max distance, tremor totems or stay away from fire")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-magmadar.png", filename="mc-magmadar.png")
            )

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
