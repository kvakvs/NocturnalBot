class RaidhelperPlayerSpec:
    """
    name<string> - The name of this spec.
    emoteId<string> - The emote id of this spec.
    roleName<string> - The name of the role that this spec belongs to.
    roleEmoteId<string> - The emote id of the role that this spec belongs to.
    """

    def __init__(self, json_data: dict):
        """
        Initialize a PlayerSpec from a JSON object.

        Args:
            json_data (dict): A dictionary containing the player spec data
        """
        self.name = json_data.get('name')
        self.emote_id = json_data.get('emoteId')
        self.role_name = json_data.get('roleName')
        self.role_emote_id = json_data.get('roleEmoteId')

    def __str__(self) -> str:
        """
        Returns a string representation of the PlayerSpec with all its fields.

        Returns:
            str: A formatted string showing all fields of the PlayerSpec
        """
        output = []
        output.append(f"PlayerSpec: {self.name}")
        output.append("-" * 30)
        output.append(f"  Emote ID: {self.emote_id}")
        output.append(f"  Role: {self.role_name}")
        output.append(f"  Role Emote: {self.role_emote_id}")
        return "\n".join(output)


class RaidhelperPlayerClass:
    """
    name<string> - The name of this class.
    limit<string> - The maximum allowed sign-ups for this class.
    emoteId<string> - The emote id of this class.
    type<string> - The type (primary/default) of this class.
    specs array of PlayerSpec - The classes that are applied to this event.
    """

    def __init__(self, json_data: dict):
        """
        Initialize a PlayerClass from a JSON object.

        Args:
            json_data (dict): A dictionary containing the player class data
        """
        self.name = json_data.get('name')
        self.limit = json_data.get('limit')
        self.emote_id = json_data.get('emoteId')
        self.type = json_data.get('type')
        self.specs = [RaidhelperPlayerSpec(json_data=each_spec) for each_spec in json_data.get('specs', [])]

    def __str__(self) -> str:
        """
        Returns a string representation of the PlayerClass with all its fields.

        Returns:
            str: A formatted string showing all fields of the PlayerClass
        """
        output = []
        output.append(f"PlayerClass: {self.name}")
        output.append("-" * 30)
        output.append(f"  Limit: {self.limit}")
        output.append(f"  Type: {self.type}")
        output.append(f"  Emote ID: {self.emote_id}")
        if self.specs:
            output.append(f"  Specs: {', '.join(str(spec) for spec in self.specs)}")
        return "\n".join(output)
