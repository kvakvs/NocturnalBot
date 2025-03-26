import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class BaronGeddon(BasePlanner):
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
            file=discord.File("images/mc/geddon.png", filename="mc-geddon.png")
        )
