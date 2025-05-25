import logging

from typing import List, Tuple
from discord import Client, Status, Member, Guild


class BotMonitor:
    def __init__(self, client: Client, bot_ids: List[int]) -> None:
        self.client = client

        self.bot_ids = bot_ids

        self.last_status: dict[int, Status] = {}

        self.alerted_bots: set[int] = set()


    async def check_bots(self) -> List[Tuple[str, int, str]]:
        await self.client.wait_until_ready()

        guilds: List[Guild] = self.client.guilds

        offline: List[Tuple[str, int, str]] = []

        for bot_id in self.bot_ids:
            member: Member | None = self._find_member_in_guilds(bot_id, guilds)

            if member:
                current_status = member.status

                self._log_status_change(member.name, bot_id, current_status)

                self.last_status[bot_id] = current_status

                if current_status != Status.online:
                    if bot_id not in self.alerted_bots:
                        offline.append((member.name, bot_id, str(current_status)))

                        self.alerted_bots.add(bot_id)
                else:
                    self.alerted_bots.discard(bot_id)

            else:
                if bot_id not in self.alerted_bots:
                    offline.append((f"ID {bot_id}", bot_id, "not in guild"))

                    self.alerted_bots.add(bot_id)

                self.last_status[bot_id] = Status.offline

        return offline


    def _find_member_in_guilds(self, bot_id: int, guilds: List[Guild]) -> Member | None:
        for guild in guilds:
            member = guild.get_member(bot_id)

            if member:
                return member

        return None


    def _log_status_change(self, name: str, bot_id: int, new_status: Status) -> None:
        prev = self.last_status.get(bot_id)

        if prev != new_status:
            logging.info(f"{name} ({bot_id}) status changed: {prev} -> {new_status}")
