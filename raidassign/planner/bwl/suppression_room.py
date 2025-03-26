import random
import discord
from raidassign.planner.party import Party, PlayerClass
from raidassign.planner.planner import BasePlanner


class SuppressionRoom(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        embed = discord.Embed(
            title="Suppression Room",
            color=0x800000,
            description="A very welcome place with clouds of ~~death~~ joy and traps of ~~death~~ fun!"
        )
        rogues = party.get_class([PlayerClass.ROGUE])
        random.shuffle(rogues)
        if len(rogues) > 3:
            rogues = rogues[:3]
        formatted_rogues = ", ".join([r for r in rogues])
        embed.add_field(name="Rogues", value=f"/rw Rogues having fun in the Suppression Room: {formatted_rogues}")
        await interaction.followup.send(embed=embed)
