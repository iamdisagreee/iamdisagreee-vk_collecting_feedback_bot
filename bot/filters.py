from datetime import time, datetime
from zoneinfo import ZoneInfo
from vkbottle.bot import Message
from vkbottle import ABCRule


class TimeFilter(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        return time(hour=20, minute=30) <= datetime.now(ZoneInfo('Europe/Moscow')).time() or \
            datetime.now(ZoneInfo('Europe/Moscow')).time() < time(hour=7, minute=0)

class NoState(ABCRule[Message]):
    async def check(self, event: Message):
        return event.state_peer is None
