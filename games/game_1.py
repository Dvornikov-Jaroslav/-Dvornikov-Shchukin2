from base.vk_bot import Bot
from other.send_message import send_message
from accepts.user_accept import user_response_accept
from accepts.game_user_accept import game_user_response_accept
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def create_mini_game_1(user_id):
    bot = Bot()
    message = None
    while not message:
        message = '\n'.join(bot.predict_the_work())

    if message == '':
        message = 'Результатов не найдено'
    send_message(user_id, message)
    user_response = user_response_accept()[0]
    composition_name = bot.game.composition_name
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
    game_user_response_accept(user_response, composition_name, user_id, keyboard)