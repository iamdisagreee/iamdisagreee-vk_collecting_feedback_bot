from vkbottle import BaseStateGroup


class FeedbackState(BaseStateGroup):
    WAIT = '1'
    GOOD = '2'
    BAD = '3'
    PAUSE = '4'
