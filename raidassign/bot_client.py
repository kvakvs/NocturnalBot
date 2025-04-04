from typing import Optional, Dict

import discord
from discord import app_commands
import toml


class NocDiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, conf: Dict):
        super().__init__(intents=intents, application_id=int(conf['application_id']))

        self.conf = conf
        # self.application_id = int(self.conf['application_id'])
        self.guild = discord.Object(id=int(self.conf['guild']))

        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=self.guild)
        await self.tree.sync(guild=self.guild)
