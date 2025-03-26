import discord
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner


class SulfuronHarbinger(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        formatted_kickers = party.get_interrupts_formatted([RAID_MARK[8], RAID_MARK[7], RAID_MARK[6], RAID_MARK[5]])
        embed = discord.Embed(
            title="Sulfuron Harbinger",
            color=0xff0000
        )
        embed.set_image(url="attachment://mc-sulfuron-harbinger.png")
        embed.add_field(name="Interrupts", value=f"/rw Interrupts: {formatted_kickers}")
        await interaction.followup.send(
            embed=embed,
            file=discord.File("images/mc/sulfuron-harbinger.png", filename="mc-sulfuron-harbinger.png")
        )
