from base.vk_base import longpoll
from vk_api.bot_longpoll import VkBotEventType


def user_response_accept():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            user_id = event.obj.message['from_id']
            text = event.obj.message['text']
            return [text, user_id]