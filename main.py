from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from base.vk_bot import Bot
from base.vk_base import longpoll
from other.send_message import send_message
from other.start import start
from games.choosing import game_choosing
from games.game_1 import create_mini_game_1
from other.menu_exit import menu_exit
from games.game_2 import create_mini_game_2
from other.error import command_error
from accepts.user_accept import user_response_accept
from other.quotes_search import quotes_search


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']

            # Знакомимся с пользователем
            start(user_id, text)
            # Запускаем бота
            bot = Bot()
            # Выбираем нужное действие
            if text == 'Мини-Игра🎲':

                game = game_choosing(user_id)

                if game == 'Угадай произведение':
                    create_mini_game_1(user_id)

                    menu_exit(user_id)

                elif game == 'Угадай дату написания произведения':
                    create_mini_game_2(user_id)

                    menu_exit(user_id)

                else:
                    command_error(user_id)

                    menu_exit(user_id)

            elif text == 'Найти фрагмент текста📰':
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Найти цитаты', VkKeyboardColor.POSITIVE)
                send_message(user_id, 'Выберите нужное действие', keyboard)

                text, _ = user_response_accept()

                if text == 'Найти цитаты':
                    send_message(user_id, 'Введите ссылку на нужное произведение с сайта ilibrary.ru'
                                          '\nСсылка должна иметь формат:'
                                          ' https://ilibrary.ru/text/ID_ТЕКСТА/index.html')

                    url, _ = user_response_accept()
                    bot.url = url
                    send_message(user_id, 'Введите имя искомого персонажа')

                    name, _ = user_response_accept()
                    try:
                        quotes_search(bot, name, user_id)
                    except BaseException:
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
                        send_message(user_id, '&#9940;Произошла ошибка...', keyboard)

                    menu_exit(user_id)

                else:
                    command_error(user_id)

                    menu_exit(user_id)

            elif text == 'Начать':
                pass

            else:
                command_error(user_id)

                menu_exit(user_id)


if __name__ == '__main__':
    main()
