
import discord

from raidassign.planner.party import Party


class BasePlanner:
    """Abstract base class for all planners."""

    async def run(self, interaction: discord.Interaction, party: Party):
        await interaction.followup.send("This default planner implementation does nothing.", ephemeral=True)
