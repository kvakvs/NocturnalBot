import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


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
            file=discord.File("images/mc/shazzrah.png", filename="mc-shazzrah.png")
        )
