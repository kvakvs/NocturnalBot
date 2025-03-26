import discord
import toml
from raidassign.planner.assign_tasks import assign_tasks, invert_dict
from raidassign.planner.discord_const import RAID_MARK
from raidassign.planner.party import Party, PlayerClass, PlayerSpec
from raidassign.planner.planner import BasePlanner
from raidassign.planpics.plan_painter import PlanPainter


def get_3_tanks(tanks: list[str]) -> tuple[str, str, str]:
    """Extracts main tank and two offtanks from the list of tanks."""
    return tanks[0], tanks[1], tanks[2]


class PlannerBWL:
    @staticmethod
    def get_config(section: str) -> dict:
        # config = toml.load("mc_planner.toml")
        # return config[section]
        return {}

    class Razorgore(BasePlanner):
        async def run(self, interaction: discord.Interaction, party: Party):
            """
            Draw Razorgore room, spawns in all 4 corners, Groups 1-4 in all 4 corners, ranged in the middle,
            and controller at the orb.
            """
            plan = PlanPainter("images/bwl/room-razorgore.png")

            def spawns(x: float, y: float, plan: PlanPainter):
                plan.add_icon("images/bwl/death-talon-dragonspawn.png",
                              (x, y), 64,
                              text="Dragonspawn", background_color=PlanPainter.COLOR_RAGE)
                plan.add_icon("images/bwl/blackwing-mage.png",
                              (x+0.1, y), 64,
                              text="Mage", background_color=PlanPainter.COLOR_MANA)
                plan.add_icon("images/bwl/blackwing-legionnaire.png",
                              (x+0.2, y), 64,
                              text="Legionnaire", background_color=PlanPainter.COLOR_RAGE)

            spawns(0.10, 0.10, plan)
            spawns(0.10, 0.90, plan)
            spawns(0.70, 0.10, plan)
            spawns(0.70, 0.90, plan)

            plan.add_icon("images/bow-and-arrow.png",
                          (0.5, 0.4), 96,
                          text="Ranged And Healers",
                          background_color=PlanPainter.COLOR_PLAYER)

            plan.add_icon("images/shield.png",
                          (0.15, 0.4), 48,
                          text="Controller",
                          background_color=PlanPainter.COLOR_PLAYER)

            def players(x: float, y: float, group: str, plan: PlanPainter):
                plan.add_icon("images/orc.png",
                              (x, y), 64,
                              text=group,
                              background_color=PlanPainter.COLOR_PLAYER)

            players(0.25, 0.25, "G1", plan)
            players(0.1, 0.75, "G2", plan)
            players(0.75, 0.25, "G3", plan)
            players(0.9, 0.75, "G4", plan)

            text_embed = discord.Embed(
                title="Razorgore",
                color=0x800000,
                description="Phase 1: Ranged stand in the middle, groups 1-4 spread into every corner. " +
                "An egg can be broken every 10 seconds (3 sec cast, 7 sec cd), the ability is 4th on the pet bar. " +
                "Protect the controller from damage, otherwise a backup controller must step in for a minute!\n" +
                "\n" +
                "Phase 2: Main tank breaks the last egg and takes the boss with very large aggro lead, the " +
                "fight continues like UBRS Drakkisath on steroids: Current tank gets conflagged and the " +
                "offtank should be the 2nd on threat because Razorgore is **IMMUNE** to taunt."
            )
            text_embed.add_field(name="Healers", value="Save mana, downrank heals")
            text_embed.add_field(name="Hunters and Warlocks",
                                 value="Do not use expensive DoT spells on targets that die quickly")
            text_embed.add_field(name="Druids", value="Sleep dragonspawns, even if they are under DPS.")
            text_embed.set_image(url="attachment://razorgore.png")

            plan_embed = discord.Embed(
                title="Nice Picture",
                color=0x800000,
            )
            plan_embed.set_image(url="attachment://razorgore-plan.png")

            await interaction.followup.send(
                embeds=[text_embed, plan_embed],
                files=[discord.File("images/bwl/boss-razorgore-the-untamed.png", filename="razorgore.png"),
                       discord.File(plan.output(".png"), filename="razorgore-plan.png")]
            )

    @staticmethod
    def get_all() -> dict[str, BasePlanner]:
        return {
            "razorgore": PlannerBWL.Razorgore()
        }
