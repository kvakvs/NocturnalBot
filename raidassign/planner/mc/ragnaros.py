import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


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
            file=discord.File("images/mc/ragnaros.png", filename="mc-ragnaros.png")
        )
