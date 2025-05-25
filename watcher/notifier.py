import logging

from discord import User, Client
from typing import List, Tuple


class Notifier:
    def __init__(self, client: Client, owner_id: int) -> None:
        self.client = client

        self.owner_id = owner_id
    

    async def send_alert(self, offline_bots: List[Tuple[str, int, str]]) -> None:
        try:
            user: User = await self.client.fetch_user(self.owner_id)

            msg: str = "**Alert**: Some bots are unreachable or offline:\n" + \
                       "\n".join(f"- {name} ({bot_id}): {status}" for name, bot_id, status in offline_bots)
            
            await user.send(msg)
        except Exception as e:
            logging.error(f"Failed to send alert DM: {e}")