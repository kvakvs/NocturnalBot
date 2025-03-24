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
from raidassign.raidhelperbot.api import fetch_raid_data
from raidassign.raidhelperbot.raid_event import RaidEvent
from raidassign.cache import RaidCache

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

@bot.tree.command(name="nocraid", description="Fetch and display raid information")
@discord.app_commands.describe(raid_id="The ID of the raid to fetch")
async def command_raid(interaction: discord.Interaction, raid_id: str):
    """Command to fetch and display raid information."""
    await interaction.response.defer()  # Defer the response as this might take some time

    try:
        raid_data = fetch_raid_data(raid_id, cache)
        if raid_data:
            evt = RaidEvent(json_data=raid_data)
            # Create an embed for the raid information
            embed = discord.Embed(
                title=f"Raid Information: {evt.title}",
                description=f"Date: {evt.date}\nTime: {evt.time}",
                color=discord.Color.blue()
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Failed to fetch raid data")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

@bot.tree.command(name="nochelp", description="Show available commands")
async def command_help(interaction: discord.Interaction):
    """Display help information about available commands."""
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.green()
    )
    embed.add_field(name="/nocraid <raid_id>", value="Fetch and display raid information", inline=False)
    embed.add_field(name="/nochelp", value="Show this help message", inline=False)
    await interaction.response.send_message(embed=embed)

async def main():
    """Main function to run the bot."""
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
