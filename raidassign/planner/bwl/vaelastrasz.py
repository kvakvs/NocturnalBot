import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Vaelastrasz(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw Vaelastrasz room, ranged on the right, melee on the left, boss (middle) and the bomb spot.
        """
        plan = PlanPainter("images/bwl/room-vaelastrasz.png")

        plan.add_icon("images/bow-and-arrow.png",
                      (0.8, 0.4), 96,
                      text="Ranged And Healers",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/orc.png",
                      (0.4, 0.4), 64,
                      text="Melee",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/shield.png",
                      (0.5, 0.2), 32,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/red-dragon.png",
                      (0.5, 0.4), 128,
                      text="Vaelastrasz",
                      background_color=PlanPainter.COLOR_RAGE)

        plan.add_icon("images/bomb.png",
                      (0.8, 0.9), 128,
                      text="Bomb",
                      background_color=PlanPainter.COLOR_PLAYER_ORANGE)

        text_embed = discord.Embed(
            title="Vaelastrasz",
            color=0x800000,
            description="Chain Cleave! Main tank becomes the bomb in 1 minute. " +
            "Infinite mana, rage and energy. Feral druids shred, rogues stab. " +
            "Warriors **DO NOT** heroic strike! Bomb person gets 100%% crit (watch threat!)."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Chain Cleave :skull:, Flame Breath :fire:, Tail Sweep, Burning Adrenaline :bomb:")
        text_embed.add_field(
            name="Healers", value="Use fast heals: Flash Heal, Lesser HW/Chain Heal, Regrowth! Max rank heals!")
        text_embed.set_image(url="attachment://vaelastrasz.png")

        plan_embed = discord.Embed(
            title="Nice Picture",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://vaelastrasz-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-vaelastrasz.png", filename="vaelastrasz.png"),
                   discord.File(plan.output(".png"), filename="vaelastrasz-plan.png")]
        )
