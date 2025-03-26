
import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Flamegor(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw a plan for the Flamegor fight.
        """
        plan = PlanPainter("images/bwl/room-ebonroc-flamegor.png")

        # Boss (black dragon)
        plan.add_icon("images/black-dragon.png",
                      (0.6, 0.3), 128,
                      text="Flamegor",
                      background_color=PlanPainter.COLOR_RAGE)

        # Tanks
        plan.add_icon("images/shield.png",
                      (0.65, 0.3), 48,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/bow-and-arrow.png",
                      (0.47, 0.63), 64,
                      text="Ranged",
                      background_color=PlanPainter.COLOR_PLAYER)
        plan.add_icon("images/nurse.png",
                      (0.43, 0.58), 64,
                      text="Healers",
                      background_color=PlanPainter.COLOR_PLAYER)

        text_embed = discord.Embed(
            title="Flamegor",
            color=0x800000,
            description="Very simple fight, the boss is tauntable. Use Onyxia Scale Cloak if the dragon will ever look at you."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Frenzy (followed by Fire Nova if not cleared), Wing Buffet, Shadow Flame :skull:, Thrash (double attack)")
        text_embed.add_field(
            name="Tanks", value="Position dragon in the corner your back to the wall.")
        text_embed.add_field(
            name="Hunters", value="Tranquilize.")
        text_embed.add_field(
            name="All DPS", value="Start DPS slow, to let the tanks build threat for Wing Buffet.")
        text_embed.set_image(url="attachment://flamegor.png")

        plan_embed = discord.Embed(
            title="Plan: Flamegor",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://flamegor-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-flamegor.png", filename="flamegor.png"),
                   discord.File(plan.output("flamegor-plan.png"), filename="flamegor-plan.png")]
        )
