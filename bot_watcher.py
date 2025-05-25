import asyncio
import yaml
import logging
import discord

from datetime import datetime
from typing import List, Tuple, Dict, Any
from discord import Client
from os.path import expanduser

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

WATCHER_TOKEN: str = config["watcher_token"]

OWNER_ID: int = int(config["owner_id"])

INTERVAL: int = config["interval"]

BOT_IDS: list[int] = [int(b) for b in config["bots"]]

LOG_PATH: str = expanduser(config["log_path"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

intents: discord.Intents = discord.Intents.none()

intents.presences = True
intents.guilds = True
intents.members = True

client: Client = discord.Client(intents=intents)

async def check_bots() -> None:
    await client.wait_until_ready()

    guilds: List[Guild] = client.guilds

    owner: User = await client.fetch_user(OWNER_ID)

    unreachable: List[Tuple[str, int, str]] = []

    logging.info("\n\nCHECKING STATUS:")

    for bot_id in BOT_IDS:
        found: bool = False

        for guild in guilds:
            member: Member | None = guild.get_member(bot_id)

            if member:
                found = True

                status: Status = member.status

                logging.info(f"{member.name} ({bot_id}) is {status}")

                if status != discord.Status.online:
                    unreachable.append((member.name, bot_id, str(status)))
                break

        if not found:
            logging.warning(f"Bot ID {bot_id} not found in any guilds.")

            unreachable.append((f"ID {bot_id}", bot_id, "not in guild"))
        
    if unreachable:
        msg: str = "**Alert**: Some bots are unreachable or offline:\n" + \
                   "\n".join(f"- {name} ({bot_id}): {status}" for name, bot_id, status in unreachable)
        
        try:
            await owner.send(msg)
        except Exception as e:
            logging.error(f"Failed to DM owner: {e}")
    

    await asyncio.sleep(INTERVAL)

    await check_bots()


@client.event
async def on_ready() -> None:
    logging.info(f"Watcher bot logged in as {client.user}")

    asyncio.create_task(check_bots())


if __name__ == "__main__":
    client.run(WATCHER_TOKEN)