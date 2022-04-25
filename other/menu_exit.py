from accepts.user_accept import user_response_accept
from other.start import start


def menu_exit(user_id):
    choice, _ = user_response_accept()

    if choice == 'Вернуться в меню':
        start(user_id, 'Начать', start=False)
