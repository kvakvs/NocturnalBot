class Signup:
    """
    name<string> - The name of the user.
    id<number> - The id of this sign-up.
    userId<string> - The Discord id of the user.
    className<string> - The class name of the sign-up.
    classEmoteId<string> - The class emote id of the sign-up.
    specName<string> - the spec name of the sign-up.
    specEmoteId<string> - The spec emote id of the sign-up.
    roleName<string> - The role name of the sign-up.
    roleEmoteId<string> - The role emote id of the sign-up.
    status<string> - The status (primary/queued) of the sign-up.
    entryTime<number> - The unix timestamp of the registration time.
    position<number> - The order number of this sign-up.
    """

    def __init__(self, json_data: dict):
        """
        Initialize a Signup from a JSON object.

        Args:
            json_data (dict): A dictionary containing the signup data
        """
        # User information
        self.name = json_data.get('name')
        self.id = json_data.get('id')
        self.user_id = json_data.get('userId')

        # Class information
        self.class_name = json_data.get('className')
        self.class_emote_id = json_data.get('classEmoteId')

        # Spec information
        self.spec_name = json_data.get('specName')
        self.spec_emote_id = json_data.get('specEmoteId')

        # Role information
        self.role_name = json_data.get('roleName')
        self.role_emote_id = json_data.get('roleEmoteId')

        # Status and timing
        self.status = json_data.get('status')
        self.entry_time = json_data.get('entryTime')
        self.position = json_data.get('position')

    def __str__(self) -> str:
        """
        Returns a string representation of the Signup with all its fields.

        Returns:
            str: A formatted string showing all fields of the Signup
        """
        output = []
        output.append(f"Signup: {self.name}")
        output.append("-" * 30)

        # User information
        output.append("User Information:")
        output.append(f"  ID: {self.id}")
        output.append(f"  Discord ID: {self.user_id}")

        # Class and spec information
        output.append("\nClass Information:")
        output.append(f"  Class: {self.class_name}")
        output.append(f"  Class Emote: {self.class_emote_id}")
        output.append(f"  Spec: {self.spec_name}")
        output.append(f"  Spec Emote: {self.spec_emote_id}")

        # Role information
        output.append("\nRole Information:")
        output.append(f"  Role: {self.role_name}")
        output.append(f"  Role Emote: {self.role_emote_id}")

        # Status and timing
        output.append("\nStatus Information:")
        output.append(f"  Status: {self.status}")
        output.append(f"  Position: {self.position}")
        output.append(f"  Entry Time (Unix): {self.entry_time}")

        return "\n".join(output)
