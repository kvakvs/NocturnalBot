import random
import discord
from raidassign.planner.party import Party
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


class Nefarian(BasePlanner):
    async def run(self, interaction: discord.Interaction, party: Party):
        """
        Draw Nefarian room, tanking position, mage call position.
        """

        plan = PlanPainter("images/bwl/room-nefarian.png")

        plan.add_icon("images/black-dragon.png",
                      (0.45, 0.32), 200,
                      text="Nefarian",
                      background_color=PlanPainter.COLOR_RAGE)

        plan.add_icon("images/bow-and-arrow.png",
                      (0.9, 0.4), 96,
                      text="Ranged And Healers",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/orc.png",
                      (0.55, 0.3), 64,
                      text="Melee",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/shield.png",
                      (0.45, 0.1), 32,
                      text="Main Tank",
                      background_color=PlanPainter.COLOR_PLAYER)

        plan.add_icon("images/sheep.png",
                      (0.7, 0.9), 80,
                      text="Mage Call Safe Spot",
                      background_color=PlanPainter.COLOR_PLAYER_ORANGE)
        plan.draw_arrow((0.75, 0.87), 50, 270, color=(255, 255, 0, 255), width=3)

        decursers = party.get_decursers(favour="any")
        random.shuffle(decursers)
        mt_decursers = ", ".join(decursers[:3])

        text_embed = discord.Embed(
            title="Nefarian",
            color=0x800000,
            description="A big black dragon, with breath, fear and tail sweep. 2-phase fight with a special event.\n" +
            "Class calls:\n" +
            "Druids: Forced cat form. Adjust the decursers accordingly.\n" +
            "Priests: Direct heals damage the target. No direct healing, only shield and renew.\n" +
            "Mages: Randomly use Polymorph. Run to the sheep safe spot.\n" +
            "Warlocks: Create infernals, kill infernals.\n" +
            "Warriors: Forced into berserker stance. Extra MT healing required and use tank and healer cooldowns.\n" +
            "Rogues: Teleported to dragon face and rooted. Turn the dragon.\n" +
            "Hunters: Ranged weapon breaks. Remove ranged weapon before this.\n" +
            "Shamans: Create corrupted totems. Kill totems."
        )
        text_embed.add_field(name="Boss Abilities",
                             value="Shadow Flame :fire:, Tail Sweep, Cleave, Fear, Veil of Shadow (curse), Class Calls")
        text_embed.add_field(
            name="Phase 1", value="Kill dragons pouring out of 2 doors. After this entire room becomes engulfed in Shadow Flame (cloak required).")
        text_embed.add_field(
            name="Phase 2", value="Regular black dragon tank & spank, breaking fear and reacting to class calls.")
        text_embed.add_field(
            name="Phase 3 (Special Event)", value="All dragons killed in phase 1 resurrect as skeletons. Kill them using AoE, explosives and holy water.")
        text_embed.add_field(
            name="Decurse Main Tank", value=f"/rw Decurse Veil of Shadow from the MT: {mt_decursers}")

        text_embed.set_image(url="attachment://nefarian.png")

        plan_embed = discord.Embed(
            title="Plan: Nefarian",
            color=0x800000,
        )
        plan_embed.set_image(url="attachment://nefarian-plan.png")

        await interaction.followup.send(
            embeds=[text_embed, plan_embed],
            files=[discord.File("images/bwl/boss-nefarian.png", filename="nefarian.png"),
                   discord.File(plan.output(".png"), filename="nefarian-plan.png")]
        )
