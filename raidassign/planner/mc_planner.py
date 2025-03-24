import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class McPlanner:
    class AllBosses(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Lucifron(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Magmadar(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Gehennas(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Garr(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Geddon(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Shazzrah(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class SulfuronHarbinger(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Majordomo(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass

    class Ragnaros(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            pass
