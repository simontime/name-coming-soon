import bot_token, discord, flash_api, os, report, server_registry
from discord.ext import tasks

# Name of directory where data is stored
DATA_DIRECTORY_NAME = "data"

# How often the FlashStation API is checked (in seconds)
CHECK_FREQUENCY = 60 * 10

# Product ID of the Pixel 7 Pro
PRODUCT_PIXEL_7_PRO = "cheetah"

# Create data directory if non-existent
if not os.path.isdir(DATA_DIRECTORY_NAME):
    os.mkdir(DATA_DIRECTORY_NAME)

# Load server registry if existent
if server_registry.file_exists():
    server_registry.load_registry_from_file()

# Load last report if existent
if report.file_exists():
    report.load_last_report_from_file()

# Create a client
client = discord.Client(intents=discord.Intents.all())

# Create command tree
cmd = discord.app_commands.CommandTree(client)

@cmd.command(name="slap", description="Slaps another member around a bit with a large trout.")
async def slap(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"***{interaction.user.name}*** *slaps* ***{member.name}*** *around a bit with a large trout*")

@cmd.command(name="register", description="Registers a channel in this server to receive update reports.")
async def register(interaction: discord.Interaction, channel: discord.TextChannel):
    # Adds/changes guild and channel in registry and saves to file
    server_registry.add_to_registry(interaction.guild.id, channel.id)
    server_registry.save_registry_to_file()

    await interaction.response.send_message(f"{channel.mention} is now registered to recieve update reports.")

@cmd.command(name="deregister", description="De-registers this server from receiving update reports.")
async def deregister(interaction: discord.Interaction):
    # Attempt to remove guild from registry
    success = server_registry.remove_from_registry(interaction.guild.id)

    # Error if not registered
    if not success:
        await interaction.response.send_message(f"Unable to de-register - this server is not currently registered.")
        return

    # Save registry to file
    server_registry.save_registry_to_file()

    await interaction.response.send_message(f"This server has been de-registered from receiving update reports.")

# Executed when bot ready
@client.event
async def on_ready():
    # Start checks task
    perform_checks.start()
    
    # Sync slash commands
    await cmd.sync()

# Generates a message summarising the changes between the reports
def generate_report_message(added, removed):
    # Create embed
    embed = discord.Embed(
        title=f"Builds for '{PRODUCT_PIXEL_7_PRO}' have been updated",
        colour=discord.Colour.green()
    )

    # Add added and removed builds to embed
    for field in [added, removed]:
        text = ""

        for build in field:
            # Extract fields
            name     = build["releaseCandidateName"]
            version  = "Release" if "releaseBuildMetadata" in build else "Preview"
            build_id = build["buildId"]
            url      = build["factoryImageDownloadUrl"]

            # Add build to list
            text += f"• {name} ({version}) (build ID {build_id}) • [Download]({url})\n"

        # Add field to embed
        field_name = "Added" if field is added else "Removed"
        embed.add_field(name=field_name, value=text, inline=False)

    return embed

# Checks for changes between current and last build report
@tasks.loop(seconds=CHECK_FREQUENCY)
async def perform_checks():
    await client.wait_until_ready()

    # Get list of available builds for the Pixel 7 Pro
    builds = flash_api.retrieve_builds_for_product(PRODUCT_PIXEL_7_PRO)

    # Process report
    processed = report.process(builds)

    # If there are changes
    if processed is not None:
        # Generate embed
        added, removed = processed
        embed = generate_report_message(added, removed)

        # Send message to every channel in registry
        for guild, channel in server_registry.registry.items():
            await client.get_channel(channel).send(embed=embed)

# Start bot
client.run(bot_token.DISCORD_BOT_TOKEN)
