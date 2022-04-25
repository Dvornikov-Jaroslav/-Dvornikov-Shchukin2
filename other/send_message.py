import random
from base.vk_base import vk_session


def send_message(user_id, message, keyboard=None):
    post = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randint(0, 2 ** 64)
    }

    if keyboard is not None:
        post["keyboard"] = keyboard.get_keyboard()

    vk_session.method("messages.send", post)