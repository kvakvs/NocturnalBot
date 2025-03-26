import discord
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.mc.planner_mc import PlannerMC
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class Gehennas(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        all_conf = PlannerMC.get_config("all_bosses")
        maintank, offtank1, offtank2 = PlannerMC.get_3_tanks(all_conf["tanks"])
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
            file=discord.File("images/mc/gehennas.png", filename="mc-gehennas.png")
        )
