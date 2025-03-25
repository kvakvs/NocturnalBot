import discord
import toml
from raidassign.planner.assign_tasks import assign_tasks, invert_dict
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party, PlayerClass, PlayerSpec
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

    @staticmethod
    def raid_decursers_str(party: Party) -> str:
        decursers, _ = assign_tasks(party.get_decursers(favour="dps"),
                                    [f"G{i}" for i in range(1, 8)],
                                    invert_result=True)

        return "; ".join([
            f"{group}={', '.join(players)}"
            for group, players in decursers.items()
        ])

    @staticmethod
    def raid_dispelers_str(party: Party) -> str:
        dispelers, _ = assign_tasks(party.get_dispelers(favour="any"),
                                    [f"G{i}" for i in range(1, 8)],
                                    invert_result=True)
        return "; ".join([
            f"{group}={','.join(players)}"
            for group, players in dispelers.items()
        ])

    class Lucifron(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            formatted_decursers = McPlanner.raid_decursers_str(party)
            formatted_dispelers = McPlanner.raid_dispelers_str(party)

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

            hunter_tasks, _ = assign_tasks(party.get_class(class_names=[PlayerClass.HUNTER]),
                                           ["Tranq1", "Tranq2"],
                                           invert_result=True)
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
        async def run(self, interaction: discord.Interaction, _party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            embed = discord.Embed(
                title="Gehennas",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-gehennas.png")
            embed.add_field(name="Tanking",
                            value=f"/rw Boss: {maintank}; Add {RAID_MARK[8]}: {offtank1}; Add {RAID_MARK[7]}: {offtank2}")
            embed.add_field(name="Offtanks",
                            value="/rw Pull adds away from boss, face away. FAP for tanks.")
            embed.add_field(name="Decursing",
                            value=f"/rw DECURSE only tanks (or if the person is at risk). Ranged are usually safe. Stay out of rain of fire")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-gehennas.png", filename="mc-gehennas.png")
            )

    class Garr(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            # all_conf = McPlanner.get_config("all_bosses")
            # maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            # For adds tanking we want warlocks to take as many adds as there are warlocks, but only one per warlock
            warlocks = party.get_class(class_names=[PlayerClass.WARLOCK])
            raid_marks = list(RAID_MARK.values())

            if len(warlocks) > 0:
                warlock_targets = raid_marks[:len(warlocks)]
                banishes, _ = assign_tasks(warlocks, warlock_targets, one_per_player=True)
                formatted_banishes = "; ".join([f"{task}={warlock[0]}" for task, warlock in banishes.items()])
            else:
                formatted_banishes = "No warlocks :rip:"

            # Remaining targets are split for all who can tank. One per tank.
            offtanks = list(set(
                party.get_role(role_names=[PlayerClass.TANK]) +
                party.get_class(class_names=[PlayerClass.WARRIOR]) +
                party.get_spec(spec_names=[PlayerSpec.FERAL])
            ))
            offtank_targets = raid_marks[len(warlocks):]
            offtank_tasks, _ = assign_tasks(offtanks, offtank_targets, one_per_player=True)
            formatted_offtanks = "; ".join([f"{task}={", ".join(offtanks)}" for task,
                                           offtanks in offtank_tasks.items()])

            embed = discord.Embed(
                title="Garr",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-garr.png")
            embed.add_field(name="Banish", value=f"/rw Banish: {formatted_banishes}")
            embed.add_field(name="Offtank", value=f"/rw Offtank: {formatted_offtanks}")
            embed.add_field(name="Pull", value="/rw Main tank pull with shield wall, warlocks banish")
            embed.add_field(name="Safety", value="/rw Adds explode on death; Keep Garr 45 yd from adds")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-garr.png", filename="mc-garr.png")
            )

    class Geddon(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            formatted_dispelers = McPlanner.raid_dispelers_str(party)
            embed = discord.Embed(
                title="Geddon",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-geddon.png")
            embed.add_field(
                name="All", value="/rw Person with living bomb run to safe spot. Melee out on inferno. Priests no heal, DISPEL (skip warriors, rogues, ferals)")
            embed.add_field(
                name="Dispel", value=f"/rw Dispel magic: {formatted_dispelers}")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-geddon.png", filename="mc-geddon.png")
            )

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
