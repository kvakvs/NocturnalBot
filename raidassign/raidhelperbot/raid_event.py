from typing import List
from raidassign.raidhelperbot.advanced_settings import AdvancedSettings
from raidassign.raidhelperbot.player_class import PlayerClass
from raidassign.raidhelperbot.player_role import PlayerRole
from raidassign.raidhelperbot.signup import Signup


class RaidEvent:
    """
    This is Raid Helper's event, as created by the event admin, and contains all sign ups, even those
    who are not taken into the raid composition.

    id<string> - The message id of this event.
    serverId<string> - The server id of this event.
    leaderId<string> - The user id of this events leader.
    leaderName<string>- The name of events leader.
    channelId<string> - This events channel id.
    channelName<string> - This events channel name.
    channelType<string> - The type of this events channel.
    templateId<string> - The id of this events template.
    templateEmoteId<string> - The emote id of the emote used to represent the template of this event.
    title<string> - The event title.
    description<string> - The event description.
    startTime<number> - The unix timestamp of when this event will start.
    endTime<number> - The unix timestamp of when this event will end.
    closingTime<number> - The unix timestamp of when this event will close and deny further sign-ups.
    date<string> - The raw date string of when this event will start.
    time<string> - The raw time string of when this event will start.
    advancedSettings: AdvancedSettings - The advanced settings for this event.
    classes: array of PlayerClass - The classes that are applied to this event.
    roles: array of PlayerRole - The roles that are applied to this event.
    signUps: array of Signup - The current sign-ups on this event.
    lastUpdated<number> - The unix timestamp of when this event was updated last.
    softresId<string> - The softres id attached to this event.
    color<string> - The current embed color in RGB format.
    """

    def __init__(self, json_data: dict) -> None:
        """Initialize a RaidEvent from a JSON object."""
        # Basic event information
        self.id: str = json_data.get('id')
        self.server_id: str = json_data.get('serverId')
        self.leader_id: str = json_data.get('leaderId')
        self.leader_name: str = json_data.get('leaderName')
        self.channel_id: str = json_data.get('channelId')
        self.channel_name: str = json_data.get('channelName')
        self.channel_type: str = json_data.get('channelType')
        self.template_id: str = json_data.get('templateId')
        self.template_emote_id: str = json_data.get('templateEmoteId')
        self.title: str = json_data.get('title')
        self.description: str = json_data.get('description')

        # Timestamps and time-related fields
        self.start_time: int = int(json_data.get('startTime'))
        self.end_time: int = int(json_data.get('endTime'))
        self.closing_time: int = int(json_data.get('closingTime'))
        self.date: str = json_data.get('date')
        self.time: str = json_data.get('time')
        self.last_updated: int = int(json_data.get('lastUpdated'))

        # Complex objects and arrays
        self.advanced_settings: AdvancedSettings = AdvancedSettings(
            json_data.get('advancedSettings', {}))
        self.classes: List[PlayerClass] = [PlayerClass(json_data=each_class)
                                           for each_class in json_data.get('classes', [])]
        self.roles: List[PlayerRole] = [PlayerRole(json_data=each_role)
                                        for each_role in json_data.get('roles', [])]
        self.sign_ups: List[Signup] = [Signup(json_data=each_signup)
                                       for each_signup in json_data.get('signUps', [])]

        # Additional fields
        self.softres_id: str = json_data.get('softresId')
        self.color: str = json_data.get('color')

    def __str__(self) -> str:
        """Returns a string representation of the RaidEvent with all its fields."""
        output = []
        output.append(f"RaidEvent: {self.title}")
        output.append("=" * 50)

        # Basic event information
        output.append("\nBasic Information:")
        output.append(f"  ID: {self.id}")
        output.append(f"  Server ID: {self.server_id}")
        output.append(f"  Leader: {self.leader_name} (ID: {self.leader_id})")
        output.append(
            f"  Channel: {self.channel_name} (ID: {self.channel_id}, Type: {self.channel_type})")
        output.append(f"  Template ID: {self.template_id}")
        output.append(f"  Description: {self.description}")

        # Time information
        output.append("\nTime Information:")
        output.append(f"  Start: {self.date} {self.time}")
        output.append(f"  Start Time (Unix): {self.start_time}")
        output.append(f"  End Time (Unix): {self.end_time}")
        output.append(f"  Closing Time (Unix): {self.closing_time}")
        output.append(f"  Last Updated (Unix): {self.last_updated}")

        # Advanced Settings
        if False:
            output.append("\nAdvanced Settings:")
            for key, value in vars(self.advanced_settings).items():
                if value is not None:  # Only show non-None values
                    output.append(f"  {key}: {value}")

        # Classes
        if False:
            output.append("\nClasses:")
            for i, player_class in enumerate(self.classes, 1):
                output.append(f"  {i}. {player_class.name}")
                output.append(f"     Limit: {player_class.limit}")
                output.append(f"     Type: {player_class.type}")
                if player_class.specs:
                    output.append(
                        f"     Specs: {', '.join(str(spec) for spec in player_class.specs)}")

        # Roles
        if False:
            output.append("\nRoles:")
            for i, role in enumerate(self.roles, 1):
                output.append(f"  {i}. {role.name}")
                output.append(f"     Limit: {role.limit}")

        # Sign-ups
        output.append("\nSign-ups:")
        for i, signup in enumerate(self.sign_ups, 1):
            output.append(f"  {i}. {signup.name}")
            output.append(f"     Class: {signup.class_name}")
            output.append(f"     Spec: {signup.spec_name}")
            output.append(f"     Role: {signup.role_name}")
            output.append(f"     Status: {signup.status}")
            output.append(f"     Position: {signup.position}")

        # Additional fields
        output.append("\nAdditional Information:")
        output.append(f"  Softres ID: {self.softres_id}")
        output.append(f"  Color: {self.color}")

        return "\n".join(output)
