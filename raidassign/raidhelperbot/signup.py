from raidassign.planner.party import PlayerClass
from raidassign.utils import safe_cast


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
    name: str
    id: int
    user_id: str
    class_name: PlayerClass
    class_emote_id: str
    spec_name: str
    spec_emote_id: str
    role_name: str
    role_emote_id: str
    status: str
    entry_time: int
    position: int

    def __init__(self, json_data: dict[str, str | int | None]) -> None:
        """
        Initialize a Signup from a JSON object.

        Args:
            json_data (dict[str, str | int | None]): A dictionary containing the signup data
        """
        # User information
        self.name = safe_cast(json_data.get('name'), str)
        self.id = safe_cast(json_data.get('id'), int)
        self.user_id = safe_cast(json_data.get('userId'), str)

        # Class information
        self.class_name = PlayerClass(json_data.get('className'))
        self.class_emote_id = safe_cast(json_data.get('classEmoteId'), str)

        # Spec information
        self.spec_name = safe_cast(json_data.get('specName'), str)
        self.spec_emote_id = safe_cast(json_data.get('specEmoteId'), str)

        # Role information
        self.role_name = safe_cast(json_data.get('roleName'), str)
        self.role_emote_id = safe_cast(json_data.get('roleEmoteId'), str)

        # Status and timing
        self.status = safe_cast(json_data.get('status'), str)
        self.entry_time = safe_cast(json_data.get('entryTime'), int)
        self.position = safe_cast(json_data.get('position'), int)

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
