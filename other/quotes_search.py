from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from other.send_message import send_message


def quotes_search(bot, name, user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
    message = None
    while not message:
        message = '\n'.join(bot.quotes(name))
    if message == '':
        message = 'Результатов не найдено'
    send_message(user_id, message, keyboard)
