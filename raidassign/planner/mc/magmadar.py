import discord
from raidassign.planner.assign_tasks import assign_tasks
from raidassign.planner.party import Party, PlayerClass
from raidassign.planner.planner import BasePlanner


class Magmadar(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        embed = discord.Embed(
            title="Magmadar",
            color=0xff0000
        )
        embed.set_image(url="attachment://mc-magmadar.png")

        hunter_tasks, _ = assign_tasks(party.get_class(class_names=[PlayerClass.HUNTER]),
                                       ["Tranq1", "Tranq2"],
                                       invert_result=True)
        formatted_tranq = "; ".join([f"{task}={', '.join(hunters)}" for task, hunters in hunter_tasks.items()])

        embed.add_field(name="Tanking + Tranq",
                        value=f"/rw Tanking boss - Cronos; {formatted_tranq}")
        embed.add_field(name="All",
                        value="/rw Stay spread, max distance, tremor totems or stay away from fire")
        await interaction.followup.send(
            embed=embed,
            file=discord.File("images/mc/magmadar.png", filename="mc-magmadar.png")
        )
