import random
import discord
from raidassign.planner.party import Party, PlayerClass
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Firemaw(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw a plan for the Firemaw fight.
        """
        plan = PlanPainter("images/bwl/room-firemaw.png")
        maintank_rel_xy = (0.8, 0.1)

        # Draw the affected area from boss center to all edges of the doorway and safe spots
        boss_rel_xy = (0.65, 0.37)
        # Red AoE area going left
        plan.draw_polygon(
            [boss_rel_xy, (0.33, 0.0), (0.0, 0.0), (0.0, 0.85)],
            color=(128, 0, 0, 64),
            outline=(255, 0, 0, 255),
            width=3)
        # Red AoE area going right
        plan.draw_polygon(
            [boss_rel_xy, (1.0, boss_rel_xy[1]), (1.0, 1.0), (0.47, 1.0)],
            color=(128, 0, 0, 64),
            outline=(255, 0, 0, 255),
            width=3)
        # Green Maintank Healing Accessibility Zone
        plan.draw_polygon(
            [maintank_rel_xy, (0.0, 0.38), (0.0, 1.0), (0.04, 1.0)],
            color=(0, 128, 0, 64),
            outline=(0, 255, 0, 255),
            width=2)

        # Tanks
        plan.add_icon("images/shield.png",
                      maintank_rel_xy, 48,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)
        plan.add_icon("images/shield.png",
                      (0.45, 0.12), 48,
                      text="Offtanks",
                      background_color=PlanPainter.COLOR_PLAYER)

        # Boss (black dragon)
        plan.add_icon("images/black-dragon.png",
                      boss_rel_xy, 200,
                      text="Firemaw",
                      background_color=PlanPainter.COLOR_RAGE)
        # plan.add_circle((0.65, 0.25), 256, (255, 128, 0, 255), "Blast Wave 20 yd", width=2)

        plan.add_icon("images/nurse.png",
                      (0.2, 0.75), 64,
                      text="MT Heal Safe Zone",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/orc.png",
                      (0.53, 0.75), 64,
                      text="Melee Safe Zone",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/bow-and-arrow.png",
                      (0.4, 0.75), 64,
                      text="Ranged Safe Zone",
                      background_color=PlanPainter.COLOR_PLAYER)

        text_embed = discord.Embed(
            title="Firemaw",
            color=0x800000,
            description="A bit finicky fight with a lot of moving parts and fire AoE damage." +
            "Use Onyxia Scale Cloak if the dragon will ever look at you."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Flame Buffet :fire:, Shadow Flame :fire:, Wing Buffet")
        text_embed.add_field(
            name="Tanks", value="Position dragon in the doorway, your back to the gate." +
            "You can increase safe zone for MT healers by moving yourself a little closer to the doorway.")
        text_embed.add_field(
            name="Offtanks", value="Wing Buffet is a threat dump, taunt before Wing Buffet, " +
            "if resisted, use another ability or second tank will taunt.")
        text_embed.add_field(
            name="Melee", value="Use the other side of the doorway to recover. There will be a healer with you.")
        text_embed.add_field(
            name="Hunters", value="Manage your pet, use 'stay' mode in safe spot and let it reset stacks with you.")
        text_embed.add_field(
            name="Tank Healers",
            value="Find a position where you see the main tank but not see the central point of the dragon, " +
            "you will not gain any stacks of Flame Buffet.")
        text_embed.set_image(url="attachment://firemaw.png")

        plan_embed = discord.Embed(
            title="Plan: Firemaw",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://firemaw-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-firemaw.png", filename="firemaw.png"),
                   discord.File(plan.output(".png"), filename="firemaw-plan.png")]
        )
