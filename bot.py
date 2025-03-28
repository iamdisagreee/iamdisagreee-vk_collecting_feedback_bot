import asyncio
from datetime import datetime, timedelta, timezone
from pyexpat.errors import messages
from random import randint

from taskiq import ScheduledTask
from vkbottle import BaseStateGroup
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import StateRule

from broker import scheduler_storage, worker

class FeedbackState(BaseStateGroup):
    GRADE = "grade"
    REVIEW = "review"

bot = Bot(token='...')


@bot.on.message(StateRule(FeedbackState.GRADE))
async def process_ask_grade_information(message: Message):
    await message.answer(f'Вы ввели: {message.text}')


@bot.on.message()
async def process_work_with_taskiq(message: Message):

    user_id = message.from_id
    user = await bot.api.users.get(user_ids=user_id)

    await scheduler_storage.startup()
    print(await scheduler_storage.get_schedules())


    list_schedules_id = set()
    for schedule in (await scheduler_storage.get_schedules()):
        list_schedules_id.add(list(schedule.labels.values())[0])

    if user_id in list_schedules_id:
        await scheduler_storage.delete_schedule(f'service_{user_id}')

    await scheduler_storage.add_schedule(ScheduledTask(task_name='schedule_sending_questions',
                                         labels={'id': user_id},
                                         args=[],
                                         kwargs={'peer_id': message.peer_id},
                                         schedule_id=f'service_{user_id}',
                                         time=datetime.now(timezone.utc) + timedelta(seconds=10))
                                         )
    # print(f"Новое сообщение: {message.text}")  # Логируем сообщение
    print(await scheduler_storage.get_schedules())
    await message.answer(f"Id = {message.from_id}\n"
                         f"Name = {user[0].first_name}")


if __name__ == "__main__":
    bot.run_forever()

