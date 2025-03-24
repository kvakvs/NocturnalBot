#!/usr/bin/env python3

import os
import asyncio
from typing import Dict, Optional
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands
import toml

from raidassign.bot_client import NocDiscordClient
from raidassign.planner.planner import run_planner
from raidassign.raidhelperbot.api import fetch_raid_plan, fetch_signup_data
from raidassign.raidhelperbot.raid_event import RaidEvent
from raidassign.cache import RaidCache
from raidassign.raidhelperbot.raid_plan import RaidPlan

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set!")

# Initialize bot with command prefix '!'
intents = discord.Intents.default()
intents.message_content = True
bot = NocDiscordClient(intents=intents, conf=toml.load("config.toml"))

# Initialize cache
cache = RaidCache()


def get_invite_url():
    """Generate the proper invite URL for the bot with required permissions."""
    permissions = discord.Permissions(
        send_messages=True,
        embed_links=True,
        read_message_history=True,
        view_channel=True,
        add_reactions=True,
        use_external_emojis=True,
        attach_files=True
    )
    return discord.utils.oauth_url(
        bot.user.id if bot.user else None,
        permissions=permissions,
        scopes=['bot', 'applications.commands']
    )


async def sync_commands():
    # Clear existing commands
    bot.tree.clear_commands(guild=None)

    # Sync slash commands with Discord
    try:
        print("Syncing commands...")

        # Sync globally
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) globally")

        # Print command details
        for command in synced:
            print(f"Command: {command.name} - {command.description}")

        # Verify commands are registered
        commands = await bot.tree.fetch_commands()
        print(f"Registered commands: {[cmd.name for cmd in commands]}")

    except Exception as e:
        print(f"Failed to sync commands: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()


@bot.event
async def on_ready():
    """Called when the bot is ready and connected to Discord."""
    print(f'Bot is ready! Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'Invite URL: {get_invite_url()}')

    await sync_commands()


# async def clear_channel(channel: discord.TextChannel):
#     """Clear the channel of all messages."""
#     message_ids = []  # Empty list to put all the messages in the log
#     async for x in bot.logs_from(channel, limit=100):
#         message_ids.append(x)
#     await bot.delete_messages(message_ids)


@bot.tree.command(name="nocraid", description="Fetch and display raid information")
@discord.app_commands.describe(signup_id="The ID of the signup event to fetch",
                               raid="Abbreviation of the raid to invoke the planning logic. Example: mc, bwl, aq40, naxx")
async def command_raid(interaction: discord.Interaction, signup_id: str, raid: str):
    """Command to fetch and display raid information."""
    # await clear_channel(interaction.channel)
    await interaction.response.defer()  # Defer the response as this might take some time

    try:
        raid_plan_json = fetch_raid_plan(signup_id, cache)
        raid_plan: RaidPlan | None = None
        if raid_plan_json:
            raid_plan = RaidPlan(json_data=raid_plan_json)
        # else:
        #   await interaction.followup.send("Failed to fetch raid plan", ephemeral=True)

        # Always load signup data
        signup_data = fetch_signup_data(signup_id, cache)
        if signup_data:
            raid_event = RaidEvent(json_data=signup_data)
        else:
            await interaction.followup.send("Failed to fetch event signup data. Event must exist and be public.", ephemeral=True)
            return

        # On success the planner will begin updating the channel. On failure it throws.
        await run_planner(raid, interaction, raid_event, raid_plan)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)
        import traceback
        traceback.print_exc()


@bot.tree.command(name="nochelp", description="Show available commands")
async def command_help(interaction: discord.Interaction):
    """Display help information about available commands."""
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.green()
    )
    embed.add_field(name="/nocraid <raid_id>",
                    value="Fetch and display raid information", inline=False)
    embed.add_field(name="/nochelp",
                    value="Show this help message", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


async def main():
    """Main function to run the bot."""
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
