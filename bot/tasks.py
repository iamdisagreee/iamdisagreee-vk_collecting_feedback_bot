from random import randint

from bot import bot, FeedbackState
from broker import worker
from keyboard import keyboard
from lexicon import LEXICON


@worker.task(task_name='schedule_sending_questions')
async def schedule_sending_questions(peer_id: int = 174127098):
    """ В таске меняется состояние на FeedbackState.WAIT - ожидаем ввода оценки"""
    await bot.state_dispenser.set(peer_id=peer_id, state=FeedbackState.WAIT)
    # print(await bot.state_dispenser.get(peer_id=peer_id))
    await bot.api.messages.send(peer_id=peer_id,
                                message=LEXICON['quality_assessment'],
                                keyboard=keyboard,
                                random_id=randint(1, 2 ** 31)
                                )
