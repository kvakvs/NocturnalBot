import discord
from raidassign.planner.assign_tasks import assign_tasks
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party, PlayerClass, PlayerSpec
from raidassign.planner.planner import BasePlanner


class Garr(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        # all_conf = McPlanner.get_config("all_bosses")
        # maintank, offtank1, offtank2 = get_3_tanks(all_conf["tanks"])

        # For adds tanking we want warlocks to take as many adds as there are warlocks, but only one per warlock
        warlocks = party.get_class(class_names=[PlayerClass.WARLOCK])
        raid_marks = list(RAID_MARK.values())

        if len(warlocks) > 0:
            warlock_targets = raid_marks[:len(warlocks)]
            banishes, _ = assign_tasks(warlocks, warlock_targets, one_per_player=True)
            formatted_banishes = "; ".join([
                f"{task}={next(iter(assign))}"
                for task, assign in banishes.items()
            ])
        else:
            formatted_banishes = "No warlocks :rip:"

        # Remaining targets are split for all who can tank. One per tank.
        offtanks = list(set(
            party.get_role(role_names=[PlayerClass.TANK]) +
            party.get_class(class_names=[PlayerClass.WARRIOR]) +
            party.get_spec(spec_names=[PlayerSpec.FERAL])
        ))
        offtank_targets = raid_marks[len(warlocks):]
        offtank_tasks, _ = assign_tasks(offtanks, offtank_targets, one_per_player=True)
        formatted_offtanks = "; ".join([
            f"{task}={", ".join(offtanks)}" for task,
            offtanks in offtank_tasks.items()
        ])

        embed = discord.Embed(
            title="Garr",
            color=0xff0000,
            description="Adds explode on death; Keep Garr 45 yd from adds"
        )
        embed.set_image(url="attachment://mc-garr.png")
        embed.add_field(name="Banish", value=f"/rw Banish: {formatted_banishes}")
        embed.add_field(name="Offtank", value=f"/rw Offtank: {formatted_offtanks}")
        embed.add_field(name="Pull", value="/rw Main tank pull with shield wall, warlocks banish")
        await interaction.followup.send(
            embed=embed,
            file=discord.File("images/mc/garr.png", filename="mc-garr.png")
        )
