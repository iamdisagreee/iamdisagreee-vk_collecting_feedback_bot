from random import randint

from .bot import bot
from .fsm import FeedbackState
from .broker import worker
from .keyboard import keyboard
from .lexicon import LEXICON


@worker.task(task_name='schedule_sending_questions')
async def schedule_sending_questions(peer_id: int):
    """ В таске меняется состояние на FeedbackState.WAIT - ожидаем ввода оценки"""
    await bot.state_dispenser.set(peer_id=peer_id, state=FeedbackState.WAIT)
    await bot.api.messages.send(peer_id=peer_id,
                                message=LEXICON['quality_assessment'],
                                keyboard=keyboard,
                                random_id=randint(1, 2 ** 31)
                                )

@worker.task(task_name='resume_sending_survey')
async def resume_sending_survey(peer_id: int):
    """ Удаляем состояние ожидания спустя 30 дней"""
    await bot.state_dispenser.delete(peer_id=peer_id)
