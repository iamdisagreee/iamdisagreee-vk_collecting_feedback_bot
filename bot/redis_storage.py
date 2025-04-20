from typing import Optional
import json
import redis.asyncio as redis  # Используем асинхронный Redis
from vkbottle import ABCStateDispenser, BaseStateGroup
from vkbottle.dispatch import StatePeer

from .fsm import FeedbackState


class RedisStateDispenser(ABCStateDispenser):

    def __init__(
            self,
            redis_client: redis.Redis,
            prefix: str = "vkbottle:state:",
    ):
        self.redis = redis_client
        self.prefix = prefix

    def _get_key(self, peer_id: int) -> str:
        return f"{self.prefix}{peer_id}"

    async def get(self, peer_id: int) -> Optional[StatePeer]:
        key = self._get_key(peer_id)
        data = await self.redis.get(key)

        if not data:
            return None

        parsed = json.loads(data)
        state = FeedbackState(parsed["state"])
        return StatePeer(
            peer_id=peer_id,
            state=state,
            payload=parsed.get("payload", {})
        )


    async def set(
            self,
            peer_id: int,
            state: BaseStateGroup = None,
            **payload
    ) -> None:
        key = self._get_key(peer_id)

        if state is None:
            await self.delete(peer_id)
            return
        data = {
            "state": state.value,
            "payload": payload
        }

        await self.redis.set(key, json.dumps(data))


    async def delete(self, peer_id: int) -> None:
        key = self._get_key(peer_id)
        await self.redis.delete(key)
