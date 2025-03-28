import asyncio

from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState
from taskiq_nats import PullBasedJetStreamBroker, NATSObjectStoreResultBackend, NATSKeyValueScheduleSource
from vkbottle import Bot

worker = PullBasedJetStreamBroker(
    servers='localhost',
    queue='taskiq_queue').with_result_backend(
    result_backend=NATSObjectStoreResultBackend(servers='localhost')
)

scheduler_storage = NATSKeyValueScheduleSource(servers="localhost")
scheduler = TaskiqScheduler(worker, sources=[scheduler_storage])

# @worker.on_event(TaskiqEvents.WORKER_STARTUP)
# async def startup(state: TaskiqState) -> None:
#     state.bot = Bot(
#         token='vk1.a.gNtCaTJJjfmpNHrG70BQYCqx01mdHqImNhWz0F_PY7pWsP15Hofb19jVrIeZKpLigJIIvtXoppjUWIKU97ctPJixistg8-4L8dx4aElQTYvOCxzP9rMe74lfhj6kKOJJOtuFGes0FUCvB3wO9tKdm44zQykINxQhgFSlGaOdh0coEHkI-rsVs325jGbx4Sqldlgch-hXSUjICuZnMdDoVg')
#     state.bot.run_polling()

