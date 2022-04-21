import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
from token_box import token
from vk_bot import Bot
from marks import quote_marks

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 212770687)


def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randint(0, 2 ** 64)
    }

    if keyboard is not None:
        post["keyboard"] = keyboard.get_keyboard()

    vk_session.method("messages.send", post)


def get_user_name(user_id):
    user_get = vk.users.get(user_ids=user_id)
    user_get = user_get[0]

    first_name = user_get['first_name']  # Имя пользователя
    last_name = user_get['last_name']  # Фамилия

    return [first_name, last_name]


def start(user_id, text, start=True):
    if text == 'Начать':
        keyboard = VkKeyboard(one_time=True)
        buttons = ['Найти фрагмент текста', 'Мини-Игра']
        buttons_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE]

        for btn, btn_color in zip(buttons, buttons_colors):
            keyboard.add_button(btn, btn_color)

        user_name = get_user_name(user_id)[0]

        if start:
            message = [f'Привет, {user_name}, я — твой бот-помощник по миру литуратуры',
                       'Я активно развиваюсь и у меня появляются новый функции.',
                       'На сегодняшний момент доступно 2 действия:',
                       '1) Найти фрагмент текста',
                       '2) Мини-Игра']
        else:
            message = ['Главное меню']

        send_message(user_id, '\n'.join(message), keyboard)

    '''
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            for elem in message:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=elem,
                                 random_id=random.randint(0, 2 ** 64))
            '''


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
            if text == 'Мини-Игра':
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Угадай произведение', VkKeyboardColor.NEGATIVE)
                send_message(user_id, 'Выберите мини-игру', keyboard)

                game = game_choosing()

                if game == 'Угадай произведение':
                    create_mini_game(bot, user_id)

                    choice = user_response_accept()[0]

                    if choice == 'Вернуться в меню':
                        start(user_id, 'Начать', start=False)

                else:
                    send_message(user_id, 'Такой игры еще нет')

            elif text == 'Найти фрагмент текста':
                pass

            elif text == 'Начать':
                pass

            else:
                send_message(user_id, 'Странно, я не знаю этой команды...')


def game_choosing():
    text, _ = user_response_accept()

    if text == 'Угадай произведение':
        return 'Угадай произведение'

    else:
        return ''


def user_response_accept():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']
            return [text, user_id]


def game_user_response_accept(response, composition_name, user_id, keyboard):
    correct_answer = list(composition_name.lower().capitalize())
    response = response.lower().capitalize()
    for b in correct_answer:
        if b in quote_marks:
            correct_answer.remove(b)
    correct_answer = ''.join(correct_answer)
    if response == correct_answer:
        send_message(user_id, f"Да вы знаток русской литературы! Это и вправду {correct_answer}!", keyboard)
    else:
        response = response.split(' ')
        correct_answer = correct_answer.split(' ')
        count_of_correct_words = len(correct_answer)
        count_of_correct_response_words = 0
        for elem in response:
            for el in correct_answer:
                if elem == el:
                    count_of_correct_response_words += 1
        correct_answer = ' '.join(correct_answer)
        if count_of_correct_response_words != 0:
            if count_of_correct_response_words / count_of_correct_words > 0.6:
                send_message(user_id, f'Вы почти угадали, это — {correct_answer}', keyboard)
            else:
                send_message(user_id, f'Ну вы хоть попытались... Это — {correct_answer}', keyboard)
        else:
            send_message(user_id, f"Вы не угадали, это {correct_answer}", keyboard)


def create_mini_game(bot, user_id):
    message = '\n'.join(bot.createMiniGame())
    send_message(user_id, message)
    user_response = user_response_accept()[0]
    composition_name = bot.game.composition_name
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Вернуться в меню', VkKeyboardColor.NEGATIVE)
    game_user_response_accept(user_response, composition_name, user_id, keyboard)


if __name__ == '__main__':
    main()
