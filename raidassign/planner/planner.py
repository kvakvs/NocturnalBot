from typing import List
import discord

from raidassign.planner.party import Party, PartyMember, get_role
from raidassign.raidhelperbot.raid_event import RaidEvent
from raidassign.raidhelperbot.raid_plan import RaidPlan


class BasePlanner:
    """Abstract base class for all planners."""

    async def run(self, interaction: discord.Interaction, party: Party):
        await interaction.followup.send("This default planner implementation does nothing.", ephemeral=True)


def get_planners_for(raid: str) -> List[BasePlanner]:
    if raid == "mc":
        from raidassign.planner.mc_planner import McPlanner
        return [
            McPlanner.AllBosses(),
            McPlanner.Lucifron(), McPlanner.Magmadar(), McPlanner.Gehennas(), McPlanner.Garr(),
            McPlanner.Geddon(), McPlanner.Shazzrah(), McPlanner.SulfuronHarbinger(),
            McPlanner.Majordomo(), McPlanner.Ragnaros()
        ]
    # elif raid == "bwl":
    #     return BwlPlanner()
    # elif raid == "aq40":
    #     return Aq40Planner()
    # elif raid == "naxx":
    #     return NaxxPlanner()
    else:
        raise ValueError(f"No planner found for raid: {raid}")


def extract_party(raid_event: RaidEvent, raid_plan: RaidPlan | None) -> Party:
    if raid_plan is not None:
        return Party(
            [PartyMember(name=drop.name, discord_user_id=drop.user_id, class_name=drop.class_name, role=get_role(drop.class_name), group=drop.party_id)
             for drop in raid_plan.raid_drops])
    else:
        return Party(
            [PartyMember(member.name, member.discord_user_id, member.class_name, member.role, None)
             for member in raid_event.members])


async def run_planner(raid: str, interaction: discord.Interaction, raid_event: RaidEvent, raid_plan: RaidPlan | None):
    planners = get_planners_for(raid)
    party = extract_party(raid_event, raid_plan)
    for planner in planners:
        await planner.run(interaction, party)
