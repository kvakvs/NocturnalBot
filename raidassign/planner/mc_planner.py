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

    class Lucifron(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

            formatted_decursers = party.get_raid_decursers_fav_dps_formatted()
            formatted_dispelers = party.get_raid_dispelers_formatted()

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
        async def run(self, interaction: discord.Interaction, party: Party):
            all_conf = McPlanner.get_config("all_bosses")
            maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])
            formatted_decursers = party.get_raid_decursers_fav_dps_formatted()

            embed = discord.Embed(
                title="Gehennas",
                color=0xff0000,
                description="DECURSE only tanks (or if the person is at risk). Ranged are usually safe. Stay out of rain of fire"
            )
            embed.set_image(url="attachment://mc-gehennas.png")
            embed.add_field(name="Tanking",
                            value=f"/rw Boss: {maintank}; Add {RAID_MARK[8]}: {offtank1}; Add {RAID_MARK[7]}: {offtank2}")
            embed.add_field(name="Offtanks",
                            value="/rw Pull adds away from boss, face away. FAP for tanks.")
            embed.add_field(name="Decursing",
                            value=f"/rw Decurses {formatted_decursers}")
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
                formatted_banishes = "; ".join([
                    f"{task}={next(iter(assign))}"
                    for task, assign in banishes.items()
                ])
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
            formatted_offtanks = "; ".join([
                f"{task}={", ".join(offtanks)}" for task,
                offtanks in offtank_tasks.items()
            ])

            embed = discord.Embed(
                title="Garr",
                color=0xff0000,
                description="Adds explode on death; Keep Garr 45 yd from adds"
            )
            embed.set_image(url="attachment://mc-garr.png")
            embed.add_field(name="Banish", value=f"/rw Banish: {formatted_banishes}")
            embed.add_field(name="Offtank", value=f"/rw Offtank: {formatted_offtanks}")
            embed.add_field(name="Pull", value="/rw Main tank pull with shield wall, warlocks banish")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-garr.png", filename="mc-garr.png")
            )

    class Geddon(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            formatted_dispelers = party.get_raid_dispelers_formatted()
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
            formatted_decursers = party.get_raid_decursers_fav_dps_formatted()
            embed = discord.Embed(
                title="Shazzrah",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-shazzrah.png")
            embed.add_field(name="Decursing",
                            value=f"/rw Decursing (SELF FIRST): {formatted_decursers}")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-shazzrah.png", filename="mc-shazzrah.png")
            )

    class SulfuronHarbinger(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            formatted_kickers = party.get_interrupts_formatted([RAID_MARK[8], RAID_MARK[7], RAID_MARK[6], RAID_MARK[5]])
            embed = discord.Embed(
                title="Sulfuron Harbinger",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-sulfuron-harbinger.png")
            embed.add_field(name="Interrupts", value=f"/rw Interrupts: {formatted_kickers}")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-sulfuron-harbinger.png", filename="mc-sulfuron-harbinger.png")
            )

    class Majordomo(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            formatted_sheepers = party.assign_to_class_formatted(
                class_names=[PlayerClass.MAGE],
                targets=[RAID_MARK[4], RAID_MARK[3], RAID_MARK[2], RAID_MARK[1]])
            formatted_kiters = party.assign_to_class_formatted(
                class_names=[PlayerClass.HUNTER],
                targets=[RAID_MARK[8], RAID_MARK[7]],
                one_per_player=True)

            all_conf = McPlanner.get_config("all_bosses")
            main_tank = all_conf["tanks"][0]
            formatted_tanks = party.assign_to_tanks_formatted(
                exclude_tanks=[main_tank],  # main tank does not tank the marked targets, boss only
                targets=[RAID_MARK[6], RAID_MARK[5]],
                one_per_player=True)
            embed = discord.Embed(
                title="Majordomo",
                color=0xff0000
            )
            embed.set_image(url="attachment://mc-majordomo-executus.png")
            embed.add_field(name="Sheep", value=f"/rw Sheep: {formatted_sheepers}")
            embed.add_field(name="Kite", value=f"/rw Kite: {formatted_kiters}")
            embed.add_field(name="Tanks", value=f"/rw Boss: {main_tank}, offtanks: {formatted_tanks}")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-majordomo-executus.png", filename="mc-majordomo-executus.png")
            )

    class Ragnaros(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            embed = discord.Embed(
                title="Ragnaros",
                color=0xff0000,
                description="Wrath of Ragnaros - knockback and threat reset, melee walk out on Wrath. There is no ranged threat, all ranged go bananas!"
            )
            embed.set_image(url="attachment://mc-ragnaros.png")
            await interaction.followup.send(
                embed=embed,
                file=discord.File("images/mc-ragnaros.png", filename="mc-ragnaros.png")
            )

    @staticmethod
    def get_all() -> dict[str, BasePlanner]:
        return {
            "all": McPlanner.AllBosses(),
            "lucifron": McPlanner.Lucifron(),
            "magmadar": McPlanner.Magmadar(),
            "gehennas": McPlanner.Gehennas(),
            "garr": McPlanner.Garr(),
            "geddon": McPlanner.Geddon(),
            "shazzrah": McPlanner.Shazzrah(),
            "sulfuron": McPlanner.SulfuronHarbinger(),
            "majordomo": McPlanner.Majordomo(),
            "ragnaros": McPlanner.Ragnaros()
        }
