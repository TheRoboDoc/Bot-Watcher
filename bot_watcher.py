import asyncio
import logging

from discord import Client, Intents

from watcher.config import Config
from watcher.logger import setup_logger
from watcher.monitor import BotMonitor
from watcher.notifier import Notifier


async def main_loop(client: Client, monitor: BotMonitor, notifier: Notifier, interval: int) -> None:
    while True:
        try:
            offline_bots = await monitor.check_bots()

            if offline_bots:
                await notifier.send_alert(offline_bots)
        except Exception as e:
            logging.exception(f"Error in monitoring loop: {e}")
        
        await asyncio.sleep(interval)


def main() -> None:
    config = Config()

    WATCHER_TOKEN: str = config.get("watcher_token")

    OWNER_ID: int = int(config.get("owner_id"))

    INTERVAL: int = config.get("interval")

    BOT_IDS: list[int] = [int(b) for b in config.get("bots")]

    LOG_PATH: str = config.get("log_path")

    setup_logger(LOG_PATH)

    intents = Intents.none()

    intents.presences = True
    intents.guilds = True
    intents.members = True

    client = Client(intents=intents)

    monitor = BotMonitor(client, BOT_IDS)

    notifier = Notifier(client, OWNER_ID)

    @client.event
    async def on_ready() -> None:
        logging.info(f"Watcher bot logged in as {client.user}")

        asyncio.create_task(main_loop(client, monitor, notifier, INTERVAL))
    

    client.run(WATCHER_TOKEN)


if __name__ == "__main__":
    main()