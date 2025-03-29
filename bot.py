import asyncio
from datetime import datetime, timedelta, timezone, time
from pyexpat.errors import messages
from random import randint
from token import NUMBER
from typing import Union
from zoneinfo import ZoneInfo
from annotated_types import Timezone
from taskiq import ScheduledTask
from vkbottle import BaseStateGroup, ABCRule
from vkbottle.bot import Bot, Message

from broker import scheduler_storage, worker
from config import load_config
from filters import TimeFilter
from fsm import FeedbackState
from lexicon import LEXICON
from mail import send_email

config = load_config()

bot = Bot(token=config.bot.token)

@bot.on.message(text=['1', '2', '3', '4', '5'])
async def process_ask_grade_information(message: Message):
    """ В зависимости от введенной оценки устанавливаем состояние"""
    await message.answer(LEXICON['question_of_opinion'])
    if message.text in ['1', '2', '3']:
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.BAD)
    else:
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.GOOD)

@bot.on.message(state=FeedbackState.GOOD)
async def process_good_grade(message: Message):
    """ Оценка 4-5. Просим написать свое мнение"""
    await message.answer(LEXICON['rating_point_3-5'])
    await bot.state_dispenser.delete(peer_id=message.peer_id)

@bot.on.message(state=FeedbackState.BAD)
async def process_bad_grade(message: Message):
    """ Оценка 1-3. Просим написать свое мнение и отправляем ответ на почту """
    user_info = await bot.api.users.get(user_id=message.from_id)
    header, body = LEXICON['letter_header'], LEXICON['letter_body'].format(user_info[0].first_name,
                                                                           user_info[0].last_name,
                                                                           message.text)

    send_email(config.mail.mail_user, config.mail.mail_password, config.mail.to_email, header, body)
    await message.answer(LEXICON['rating_point_1-2'])
    await bot.state_dispenser.delete(peer_id=message.peer_id)


@bot.on.message(TimeFilter())
async def process_sleep_bot(message: Message):
    """ Нерабочее время. Ответ - заглушка"""
    await message.answer(LEXICON['sleep_bot'])
    await message.answer(LEXICON['wait_result'])


@bot.on.message()
async def process_work_with_taskiq(message: Message):
    """ Для каждого нового сообщения устанавливаем уведомление, а для старого сообщения удаляем"""

    user_id = message.from_id

    await scheduler_storage.startup()
    print('BEFORE', await scheduler_storage.get_schedules())

    list_schedules_id = set()
    for schedule in (await scheduler_storage.get_schedules()):
        list_schedules_id.add(list(schedule.labels.values())[0])

    if user_id in list_schedules_id:
        await scheduler_storage.delete_schedule(f'service_{user_id}')

    await scheduler_storage.add_schedule(
        ScheduledTask(task_name='schedule_sending_questions',
                      labels={'user_id': user_id},
                      args=[],
                      kwargs={'peer_id': message.peer_id},
                      schedule_id=f'service_{user_id}',
                      time=datetime.now(ZoneInfo('Europe/Moscow')) + timedelta(seconds=5))
    )

    # print(f"Новое сообщение: {message.text}")  # Логируем сообщение
    print('AFTER', await scheduler_storage.get_schedules())
    # await message.answer(f"Id = {message.from_id}\n"
                         # f"Name = {user[0].first_name}")

if __name__ == "__main__":
    bot.run_forever()
