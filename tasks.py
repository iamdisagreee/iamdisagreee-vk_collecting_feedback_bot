from pyexpat.errors import messages
from random import randint

from vkbottle import Bot, BaseStateGroup, Keyboard, Text, KeyboardButtonColor
from taskiq import TaskiqDepends, Context

from bot import bot, FeedbackState
from broker import worker
from lexicon import LEXICON


@worker.task(task_name='schedule_sending_questions')
async def schedule_sending_questions(peer_id: int = 174127098):

    keyboard = (
        Keyboard(one_time=True)
        .add(Text("1"), color=KeyboardButtonColor.NEGATIVE)
        .add(Text("2"), color=KeyboardButtonColor.NEGATIVE)
        .add(Text("3"), color=KeyboardButtonColor.NEGATIVE)
        .add(Text("4"), color=KeyboardButtonColor.POSITIVE)
        .add(Text("5"), color=KeyboardButtonColor.POSITIVE)
    )

    await bot.api.messages.send(peer_id=peer_id,
                                message=LEXICON['quality_assessment'],
                                keyboard=keyboard,
                                random_id=randint(1, 2**31)
                                )
