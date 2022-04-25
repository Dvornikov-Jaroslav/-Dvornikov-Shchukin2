from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from other.send_message import send_message
from accepts.user_accept import user_response_accept
from base.vk_bot import Bot
import math


def create_mini_game_2(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Легко', VkKeyboardColor.POSITIVE)
    keyboard.add_button('Нормально', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сложно', VkKeyboardColor.NEGATIVE)
    send_message(user_id, 'Выберите сложность', keyboard)

    difficult, _ = user_response_accept()

    bot = Bot()
    true_date = bot.date_predict(difficult)

    composition_name = true_date[1]
    author_name = true_date[2]
    true_date = true_date[0]

    if difficult == 'Легко':
        send_message(user_id, f'Произвдение: {composition_name}, автор: {author_name}.\n'
                              f'Напишите век, в котором оно создано.')

        user_response = user_response_accept()[0].split(' ')
        for word in user_response:
            try:
                word = int(word)
                user_response = word
                break
            except BaseException:
                word = None
            if not word:
                user_response = word
                break

        if user_response:
            if int(user_response) == int(true_date):
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, 'Точно! Вы угадали.', keyboard)
            else:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, f'Вы не правы, это произведение написано в {true_date} веке', keyboard)
        else:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
            send_message(user_id, f'Вы не правы, это произведение написано в {true_date} веке', keyboard)

    elif difficult == 'Нормально':
        send_message(user_id, f'Произвдение: {composition_name}, автор: {author_name}.\n'
                              f'Напишите порядок десятилетия {math.ceil(true_date / 10)} века, в котором оно создано.')

        user_response = user_response_accept()[0].split(' ')
        for word in user_response:
            try:
                word = int(word)
                user_response = word
                break
            except BaseException:
                word = None
            if not word:
                user_response = word
                break

        if user_response:
            if int(user_response) == int(str(true_date)[2:]):
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, 'Точно! Вы угадали.', keyboard)
            else:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, f'Вы не правы, это произведение написано в {int(str(true_date)[2:])} '
                                      f'десятилетии {math.ceil(true_date / 10)} века', keyboard)
        else:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
            send_message(user_id, f'Вы не правы, это произведение написано в {int(str(true_date)[2:])} '
                                  f'десятилетии {math.ceil(true_date / 10)} века', keyboard)

    elif difficult == 'Сложно':
        send_message(user_id, f'Произвдение: {composition_name}, автор: {author_name}.\n'
                              f'Напишите год, в котором оно создано.')

        user_response = user_response_accept()[0].split(' ')
        for word in user_response:
            try:
                word = int(word)
                user_response = word
                break
            except BaseException:
                word = None
            if not word:
                user_response = word
                break

        if user_response:
            if int(user_response) == int(true_date):
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, 'Точно! Вы угадали.', keyboard)
            else:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                send_message(user_id, f'Вы не правы, это произведение написано в {true_date} году', keyboard)

        else:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
            send_message(user_id, f'Вы не правы, это произведение написано в {true_date} году', keyboard)