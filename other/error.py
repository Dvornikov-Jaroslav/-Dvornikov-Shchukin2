from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from other.send_message import send_message


def command_error(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
    send_message(user_id, 'Странно, я не знаю этой команды...', keyboard)
