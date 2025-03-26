from typing import List, Set
import discord

from raidassign.planner.party import Party, PartyMember, get_role
from raidassign.raidhelperbot.raid_event import RaidEvent
from raidassign.raidhelperbot.raid_plan import RaidPlan


class BasePlanner:
    """Abstract base class for all planners."""

    async def run(self, interaction: discord.Interaction, party: Party):
        await interaction.followup.send("This default planner implementation does nothing.", ephemeral=True)


def get_planners_for(raid: str, only_bosses: Set[str] | None) -> List[BasePlanner]:
    if raid == "mc":
        from raidassign.planner.mc_planner import McPlanner
        return [p
                for name, p in McPlanner.get_all().items()
                if not only_bosses or name in only_bosses]
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
            [PartyMember(name=drop.name, discord_user_id=drop.user_id, class_name=drop.class_name, role=get_role(drop.class_name),
                         spec=drop.spec, group=drop.party_id)
             for drop in raid_plan.raid_drops])
    else:
        return Party(
            [PartyMember(name=member.name, discord_user_id=int(member.user_id), class_name=member.class_name, role=None,
                         spec=member.spec_name, group=None)
             for member in raid_event.sign_ups])


async def run_planner(raid: str,
                      interaction: discord.Interaction,
                      raid_event: RaidEvent,
                      raid_plan: RaidPlan | None,
                      only_bosses: Set[str] | None):
    planners = get_planners_for(raid, only_bosses)
    party = extract_party(raid_event, raid_plan)
    for planner in planners:
        await planner.run(interaction, party)
