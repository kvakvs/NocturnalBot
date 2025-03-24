class PlayerRole:
    """
    name<string> - The name of this role.
    limit<string> - The maximum allowed sign-ups for this role.
    emoteId<string> - The emote id of this role.
    """

    def __init__(self, json_data: dict):
        """
        Initialize a PlayerRole from a JSON object.

        Args:
            json_data (dict): A dictionary containing the player role data
        """
        self.name = json_data.get('name')
        self.limit = json_data.get('limit')
        self.emote_id = json_data.get('emoteId')

    def __str__(self) -> str:
        """
        Returns a string representation of the PlayerRole with all its fields.

        Returns:
            str: A formatted string showing all fields of the PlayerRole
        """
        output = []
        output.append(f"PlayerRole: {self.name}")
        output.append("-" * 30)
        output.append(f"  Limit: {self.limit}")
        output.append(f"  Emote ID: {self.emote_id}")
        return "\n".join(output)
