import discord
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.mc.planner_mc import PlannerMC
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class Lucifron(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        all_conf = PlannerMC.get_config("all_bosses")
        maintank, offtank1, offtank2 = PlannerMC.get_3_tanks(all_conf["tanks"])

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
            file=discord.File("images/mc/lucifron.png", filename="mc-lucifron.png")
        )
