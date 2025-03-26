import random
import discord
from raidassign.planner.party import Party, PlayerClass
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class BroodlordLashlayer(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw Broodlord Lashlayer room, ranged on the left, melee on the right, tanks at the wall
        Boss is in the corner on the right.
        """
        plan = PlanPainter("images/bwl/room-broodlord-lashlayer.png")

        plan.add_icon("images/bow-and-arrow.png",
                      (0.15, 0.25), 96,
                      text="Ranged And Healers",
                      background_color=PlanPainter.COLOR_PLAYER)

        # A rogue guarding the traps
        plan.add_icon("images/thief.png",
                      (0.2, 0.5), 64,
                      text="Rogue in Stealth",
                      background_color=PlanPainter.COLOR_ENERGY)

        # Tanks
        plan.add_icon("images/shield.png",
                      (0.65, 0.1), 32,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)
        plan.add_icon("images/shield.png",
                      (0.73, 0.15), 32,
                      text="Offtank",
                      background_color=PlanPainter.COLOR_PLAYER)

        # Arrow from boss center for melee knockback direction
        plan.draw_arrow((0.65, 0.25), length=250, angle_deg=180, color=(255, 128, 0, 255), width=3)
        plan.draw_text((0.35, 0.25), "Safe Knockback Direction", color=(255, 128, 0, 255))
        # Boss (strong)
        plan.add_icon("images/bwl/icon-broodlord-strongman.png",
                      (0.65, 0.25), 128,
                      text="Broodlord Lashlayer",
                      background_color=PlanPainter.COLOR_RAGE)
        plan.add_circle((0.65, 0.25), 256, (255, 128, 0, 255), "Blast Wave 20 yd", width=2)

        plan.add_icon("images/orc.png",
                      (0.55, 0.25), 64,
                      text="Melee",
                      background_color=PlanPainter.COLOR_PLAYER)

        rogues = party.get_class([PlayerClass.ROGUE])
        if len(rogues) == 0:
            random_rogue = "No rogues, RIP"
        else:
            random_rogue = random.choice(rogues)

        text_embed = discord.Embed(
            title="Broodlord Lashlayer",
            color=0x800000,
            description="The boss is **IMMUNE** to taunt. The boss is very strong hitting and has " +
            "Mortal Strike which will leave main tank very low on health."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Mortal Strike :skull:, Knock Away (tanks), Blast Wave (all melee)")
        text_embed.add_field(
            name="Healers", value="Shield on Mortal Strike and extra heals. Tank swap on Knock Away.")
        text_embed.add_field(
            name="Melee", value="Expect Blast Wave knockback, position yourself in the " +
            "safe knockback direction. Must always be below second tank threat.")
        text_embed.add_field(
            name="Last Rogue", value=f"`/rw {random_rogue}: Stay in stealth. Watch the traps during the boss fight.`")
        text_embed.set_image(url="attachment://broodlord-lashlayer.png")

        plan_embed = discord.Embed(
            title="Plan: Broodlord Lashlayer",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://broodlord-lashlayer-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-broodlord-lashlayer.png", filename="broodlord-lashlayer.png"),
                   discord.File(plan.output(".png"), filename="broodlord-lashlayer-plan.png")]
        )
