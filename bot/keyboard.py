from vkbottle import Keyboard, Text, KeyboardButtonColor

keyboard = (
    Keyboard(one_time=True)
    .add(Text("1"), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("2"), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("3"), color=KeyboardButtonColor.NEGATIVE)
    .add(Text("4"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("5"), color=KeyboardButtonColor.POSITIVE)
)