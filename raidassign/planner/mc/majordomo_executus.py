import discord
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.mc.planner_mc import PlannerMC
from raidassign.planner.party import Party, PlayerClass
from raidassign.planner.planner import BasePlanner


class MajordomoExecutus(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        formatted_sheepers = party.assign_to_class_formatted(
            class_names=[PlayerClass.MAGE],
            targets=[RAID_MARK[4], RAID_MARK[3], RAID_MARK[2], RAID_MARK[1]])
        formatted_kiters = party.assign_to_class_formatted(
            class_names=[PlayerClass.HUNTER],
            targets=[RAID_MARK[8], RAID_MARK[7]],
            one_per_player=True)

        all_conf = PlannerMC.get_config("all_bosses")
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
            file=discord.File("images/mc/majordomo-executus.png", filename="mc-majordomo-executus.png")
        )
