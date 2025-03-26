import discord
from raidassign.planner.mc.planner_mc import PlannerMC
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class AllBossesMC(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        all_conf = PlannerMC.get_config("all_bosses")
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
