from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from other.user_name import get_user_name
from other.send_message import send_message


def start(user_id, text, start=True):
    if text == 'Начать':
        keyboard = VkKeyboard(one_time=True)
        buttons = ['Найти фрагмент текста📰', 'Мини-Игра🎲']
        buttons_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE]

        for btn, btn_color in zip(buttons, buttons_colors):
            keyboard.add_button(btn, btn_color)

        user_name = get_user_name(user_id)[0]

        if start:
            message = [f'Привет, {user_name}, я — твой бот-помощник по миру литуратуры',
                       'Я активно развиваюсь и у меня появляются новый функции.',
                       'На данный момент доступно 2 действия:',
                       '1) Найти фрагмент текста📰',
                       '2) Мини-Игра🎲;']
        else:
            message = ['Главное меню&#128203;']

        send_message(user_id, '\n'.join(message), keyboard)