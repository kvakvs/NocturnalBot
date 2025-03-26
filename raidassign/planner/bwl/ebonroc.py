
import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Ebonroc(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw a plan for the Ebonroc fight.
        """
        plan = PlanPainter("images/bwl/room-ebonroc-flamegor.png")

        # Boss (black dragon)
        plan.add_icon("images/black-dragon.png",
                      (0.6, 0.3), 128,
                      text="Ebonroc",
                      background_color=PlanPainter.COLOR_RAGE)

        # Tanks
        plan.add_icon("images/shield.png",
                      (0.65, 0.3), 48,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)
        plan.add_icon("images/shield.png",
                      (0.6, 0.2), 48,
                      text="Offtank",
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
            title="Ebonroc",
            color=0x800000,
            description="Very simple fight, the boss is tauntable. Use Onyxia Scale Cloak if the dragon will ever look at you."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Shadow of Ebonroc, Wing Buffet, Shadow Flame :skull:, Thrash (double attack)")
        text_embed.add_field(
            name="Tanks", value="Position dragon in the corner your back to the wall.")
        text_embed.add_field(
            name="Offtank", value="On Shadow of Ebonroc, taunt and keep it for 8 seconds.")
        text_embed.add_field(
            name="All DPS", value="Start DPS slow, to let the tanks build threat for Wing Buffet.")
        text_embed.set_image(url="attachment://ebonroc.png")

        plan_embed = discord.Embed(
            title="Plan: Ebonroc",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://ebonroc-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-ebonroc.png", filename="ebonroc.png"),
                   discord.File(plan.output(".png"), filename="ebonroc-plan.png")]
        )
