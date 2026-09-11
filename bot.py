import discord
from discord.ext import commands, tasks
import os
import itertools
import logging
from pathlib import Path

# ================= CONFIG =================
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "1454248846208139324"))
LINKS_FILE = os.getenv("LINKS_FILE", "links.txt")
POST_INTERVAL_MINUTES = int(os.getenv("POST_INTERVAL_MINUTES", "1"))
STATUS_INTERVAL_MINUTES = int(os.getenv("STATUS_INTERVAL_MINUTES", "2"))
GUILD_ID = int(os.getenv("GUILD_ID", "1313110086910218331"))
AUTO_ROLE_ID = int(os.getenv("AUTO_ROLE_ID", "1427593128264601682"))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID") or CHANNEL_ID)
# =========================================

# -------- LOGGING SETUP --------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s: %(message)s",
)
logger = logging.getLogger("bot")

# -------- INTENTS --------
intents = discord.Intents.default()

# Members intent is privileged — must be enabled in the Discord Developer Portal
# (Bot → Privileged Gateway Intents → Server Members Intent) AND ENABLE_MEMBERS_INTENT=true
if os.getenv("ENABLE_MEMBERS_INTENT", "false").lower() == "true":
    intents.members = True  # REQUIRED for on_member_join

# Message content intent is privileged — needed for command processing
# Enable in the Developer Portal AND set ENABLE_MESSAGE_CONTENT_INTENT=true
if os.getenv("ENABLE_MESSAGE_CONTENT_INTENT", "false").lower() == "true":
    intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------- LINK MANAGEMENT --------
link_index = 0


def load_links() -> list[str]:
    """Load links from the links file."""
    path = Path(LINKS_FILE)
    if not path.exists():
        logger.warning(f"{LINKS_FILE} not found. Creating empty file.")
        path.touch()
        return []

    try:
        links = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        logger.info(f"Loaded {len(links)} links from {LINKS_FILE}")
        return links
    except Exception as e:
        logger.error(f"Error loading links: {e}", exc_info=True)
        return []


# -------- ACTIVITY ROTATION --------
activities = itertools.cycle([
    discord.Streaming(
        name="Arpa Roy Onlyfans Collections",
        url="https://twitch.tv/arparoy"
    ),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Arpa Roy Screaming"
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="Arpa Roy Pussy"
    ),
    discord.Activity(
        type=discord.ActivityType.playing,
        name="Arpa Roy Boobs"
    ),
    discord.Activity(
        type=discord.ActivityType.competing,
        name="Arpa Roy Moaning"
    ),
    discord.Game(name="Discord Bot Simulator"),
    discord.Activity(
        type=discord.ActivityType.listening,
        name="Arpa Roy Ass Fucking"
    ),
    discord.Activity(
        type=discord.ActivityType.watching,
        name="Arpa Roy Fucking Pussy"
    ),
    discord.Activity(
        type=discord.ActivityType.playing,
        name="Arpa Roy Pussy & Boobs"
    ),
    discord.Streaming(
        name="Arpa Roy Nudes",
        url="https://arparoy-website.vercel.app"
    )
])


# -------- SETUP HOOK --------
@bot.event
async def setup_hook() -> None:
    """Called once on startup before the bot connects to the gateway."""
    post_links.start()
    rotate_status.start()
    logger.info("Started background tasks: link posting, status rotation")


# -------- EVENTS --------
@bot.event
async def on_ready() -> None:
    logger.info(f"Bot online: {bot.user} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} server(s)")


@bot.event
async def on_error(event: str, *args, **kwargs) -> None:
    logger.error(f"Error in event '{event}'", exc_info=True)


@bot.event
async def on_member_join(member: discord.Member) -> None:
    if member.guild.id != GUILD_ID:
        return

    logger.info(f"New member joined: {member} (ID: {member.id})")

    # --- Auto-role assignment ---
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role, reason="Auto role on join")
            logger.info(f"Gave role '{role.name}' to {member}")
        except discord.Forbidden:
            logger.error("Missing permissions to assign roles")
        except Exception as e:
            logger.error(f"Error assigning role: {e}", exc_info=True)
    else:
        logger.error("Auto role not found")

    # --- Announce the new member ---
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        logger.warning(f"Welcome channel {WELCOME_CHANNEL_ID} not found; skipping announcement")
        return

    try:
        await channel.send(f"👋 Welcome {member.mention} to the server!")
        logger.info(f"Announced new member {member} in channel {channel}")
    except discord.Forbidden:
        logger.error("Missing permissions to send messages in the welcome channel")
    except Exception as e:
        logger.error(f"Error announcing new member: {e}", exc_info=True)


# -------- LINK POSTER --------
@tasks.loop(minutes=POST_INTERVAL_MINUTES)
async def post_links() -> None:
    """Post links from the file to the specified channel."""
    global link_index

    links = load_links()
    if not links:
        logger.warning("No links to post")
        return

    if link_index >= len(links):
        link_index = 0
        logger.info("Restarting link rotation")

    if not bot.guilds:
        logger.warning("Bot is not connected to any servers; skipping link post")
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        logger.warning(f"Channel {CHANNEL_ID} is unavailable; skipping link post")
        return

    try:
        await channel.send(links[link_index])
        logger.info(f"Posted link {link_index + 1}/{len(links)}: {links[link_index][:50]}...")
        link_index += 1
    except discord.Forbidden:
        logger.error("Missing permissions to send messages in the channel")
    except Exception as e:
        logger.error(f"Error posting link: {e}", exc_info=True)


@post_links.before_loop
async def before_post_links() -> None:
    await bot.wait_until_ready()


@post_links.error
async def post_links_error(error: Exception) -> None:
    logger.error(f"Error in post_links task: {error}", exc_info=True)


# -------- STATUS ROTATION --------
@tasks.loop(minutes=STATUS_INTERVAL_MINUTES)
async def rotate_status() -> None:
    """Rotate bot's activity status."""
    try:
        activity = next(activities)
        await bot.change_presence(activity=activity)
        logger.info(f"Changed status to: {activity.name}")
    except Exception as e:
        logger.error(f"Error rotating status: {e}", exc_info=True)


@rotate_status.before_loop
async def before_rotate_status() -> None:
    await bot.wait_until_ready()


@rotate_status.error
async def rotate_status_error(error: Exception) -> None:
    logger.error(f"Error in rotate_status task: {error}", exc_info=True)


# -------- RUN BOT --------
if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise RuntimeError("DISCORD_TOKEN environment variable is not set")

    logger.info("Starting bot...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
