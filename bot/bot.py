from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from taskiq import ScheduledTask
from vkbottle.bot import Bot, Message

from config import load_config

from .broker import scheduler_storage
from .filters import TimeFilter, NoState
from .fsm import FeedbackState
from .lexicon import LEXICON
from .mail import send_email
from .redis_storage import RedisStateDispenser

import redis.asyncio as redis


config = load_config()
redis_client = redis.Redis.from_url(config.redis.token)
dispenser = RedisStateDispenser(redis_client)

bot = Bot(token=config.bot.token)
bot.state_dispenser = dispenser

@bot.on.message(state=FeedbackState.WAIT)
async def process_ask_grade_information(message: Message):
    """ В зависимости от введенной оценки устанавливаем состояние"""
    if message.text in ['1', '2', '3']:
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.BAD)
        await message.answer(LEXICON['question_of_opinion_1-3'])
    elif message.text == '4':
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.GOOD)
        await message.answer(LEXICON['question_of_opinion_4'])
    elif message.text == '5':
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.GOOD)
        await message.answer(LEXICON['question_of_opinion_5'])
    else:
        await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.PAUSE)
        await scheduler_storage.add_schedule(
            ScheduledTask(task_name='resume_sending_survey',
                          labels={'user_id': message.from_id},
                          args=[],
                          kwargs={'peer_id': message.peer_id},
                          schedule_id=f'pause_{message.from_id}',
                          time=datetime.now(ZoneInfo('Europe/Moscow')) + timedelta(days=30))
        )


@bot.on.message(state=FeedbackState.GOOD)
async def process_good_grade(message: Message):
    """ Оценка 4-5. Просим написать свое мнение"""
    await message.answer(LEXICON['rating_point_3-5'])
    await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.PAUSE)
    await scheduler_storage.add_schedule(
        ScheduledTask(task_name='resume_sending_survey',
                      labels={'user_id': message.from_id},
                      args=[],
                      kwargs={'peer_id': message.peer_id},
                      schedule_id=f'pause_{message.from_id}',
                      time=datetime.now(ZoneInfo('Europe/Moscow')) + timedelta(days=30))
    )

@bot.on.message(state=FeedbackState.BAD)
async def process_bad_grade(message: Message):
    """ Оценка 1-3. Просим написать свое мнение и отправляем ответ на почту """
    user_info = await bot.api.users.get(user_id=message.from_id)
    header, body = LEXICON['letter_header'], LEXICON['letter_body'].format(user_info[0].first_name,
                                                                           user_info[0].last_name,
                                                                           message.text)

    send_email(config.mail.mail_user, config.mail.mail_password, config.mail.to_email, header, body)
    await message.answer(LEXICON['rating_point_1-2'])
    await bot.state_dispenser.set(peer_id=message.peer_id, state=FeedbackState.PAUSE)
    await scheduler_storage.add_schedule(
        ScheduledTask(task_name='resume_sending_survey',
                      labels={'user_id': message.from_id},
                      args=[],
                      kwargs={'peer_id': message.peer_id},
                      schedule_id=f'pause_{message.from_id}',
                      time=datetime.now(ZoneInfo('Europe/Moscow')) + timedelta(days=30))
    )


@bot.on.message(TimeFilter())
async def process_sleep_bot(message: Message):
    """ Нерабочее время. Ответ - заглушка"""
    await message.answer(LEXICON['sleep_bot'])
    await message.answer(LEXICON['wait_result'])

@bot.on.message(NoState())
async def process_work_with_taskiq(message: Message):
    """ Для каждого нового сообщения устанавливаем уведомление, а для старого сообщения удаляем"""

    user_id = message.from_id

    await scheduler_storage.startup()

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
                      time=datetime.now(ZoneInfo('Europe/Moscow')) + timedelta(days=2))
    )

if __name__ == "__main__":
    bot.run_forever()
