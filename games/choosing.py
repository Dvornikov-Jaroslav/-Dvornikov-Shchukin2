from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from other.send_message import send_message
from accepts.user_accept import user_response_accept


def game_choosing(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Угадай произведение', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Угадай дату написания произведения', VkKeyboardColor.PRIMARY)
    send_message(user_id, 'Выберите мини-игру', keyboard)

    choice, _ = user_response_accept()

    if choice == 'Угадай произведение':
        return 'Угадай произведение'

    elif choice == 'Угадай дату написания произведения':
        return 'Угадай дату написания произведения' \
               ''
    else:
        return
