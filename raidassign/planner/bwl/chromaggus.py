
import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Chromaggus(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw a plan for the Chromaggus fight.
        """

        plan = PlanPainter("images/bwl/room-chromaggus.png")

        # Draw Red Zone where the boss will be casting the breaths
        plan.draw_polygon(
            rel_points=[(0.0, 1.0), (0.0, 0.68), (0.33, 0.49), (0.37, 0.28), (0.46, 0.28), (0.47, 0.0),
                        (0.65, 0.0), (0.625, 0.105), (0.64, 0.275), (0.725, 0.275), (0.78, 0.49), (1.0, 1.0)],
            color=(255, 0, 0, 64),
            outline=(255, 0, 0, 255),
            width=3)

        # Boss (Cerberus icon)
        plan.add_icon("images/bwl/cerberus.png",
                      (0.55, 0.35), 160,
                      text="Chromaggus",
                      background_color=PlanPainter.COLOR_RAGE)

        # Tanks
        plan.add_icon("images/shield.png",
                      (0.55, 0.53), 64,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)

        for spot_rel in [(0.39, 0.25), (0.45, 0.175), (0.47, 0.05)]:
            plan.add_icon("images/orc.png",
                          spot_rel, 48,
                          text="Melee Safe Spot",
                          background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/bow-and-arrow.png",
                      (0.15, 0.5), 64,
                      text="Ranged",
                      background_color=PlanPainter.COLOR_PLAYER)
        plan.add_icon("images/nurse.png",
                      (0.22, 0.5), 64,
                      text="Healers",
                      background_color=PlanPainter.COLOR_PLAYER)

        text_embed = discord.Embed(
            title="Chromaggus",
            color=0x800000,
            description="Selects 2 random AoE attacks (breaths) from 5 choices every week, the choice is fixed for the full week." +
            "The choices:\n" +
            ":black_heart: Black (Ignite Flesh, 1 min of fire DoT)\n" +
            r":yellow_heart: Bronze (Time Lapse - 6 second stun and your existing threat is reduced to 50%)" + "\n" +
            ":blue_heart: Blue (Frost Burn, 15 seconds of slow attack speed and 1400 Frost damage)\n" +
            ":green_heart: Green (Corrosive Acid, 1000 Nature every 3 seconds for 15 seconds and reduced armor by 4500)\n" +
            ":heart: Red (Incinerate, 4000 Fire damage once).\n"
            + "\n" +
            "Also randomly debuffs players with 5 Brood Afflictions:\n" +
            ":black_large_square: Black (**curse**, increased fire damage taken)\n" +
            ":yellow_square: Bronze (periodic stuns, use Sand or ignore)\n" +
            ":blue_square: Blue (**magic**, mana burn 50 per second, slower cast and movement)\n" +
            ":green_square: Green (**poison**, 250 damage every 5 seconds, reduced healing taken)\n" +
            ":red_square: Red (**disease**, 50 damage every 3 seconds, reduced armor. Heals boss if player dies)."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Breath 1 (every 30 seconds after Breath 2), Breath 2 (every 30 seconds after Breath 1), " +
                             "random Brood Affliction on random players. When a player collects all 5 Brood Afflictions, " +
                             "they turn into a draconid.")

        formatted_dispelers = party.get_raid_dispelers_formatted()
        text_embed.add_field(name="Dispel Magic :blue_square:", value=f"/rw Dispel {formatted_dispelers}")

        formatted_disease_cleansers = party.get_raid_disease_cleansers_formatted(only_healers=True)
        text_embed.add_field(name="Cure Disease :red_square:", value=f"/rw Cure Disease {formatted_disease_cleansers}")

        formatted_poison_cleansers = party.get_raid_poison_cleansers_formatted(only_healers=True)
        text_embed.add_field(name="Remove Poison :green_square:",
                             value=f"/rw Remove Poison {formatted_poison_cleansers}")

        formatted_decursers = party.get_raid_decursers_formatted()
        text_embed.add_field(name="Decurse :black_large_square:", value=f"/rw Remove Curse {formatted_decursers}")

        text_embed.set_image(url="attachment://chromaggus.png")

        plan_embed = discord.Embed(
            title="Plan: Chromaggus",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://chromaggus-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-chromaggus.png", filename="chromaggus.png"),
                   discord.File(plan.output("chromaggus-plan.png"), filename="chromaggus-plan.png")]
        )
