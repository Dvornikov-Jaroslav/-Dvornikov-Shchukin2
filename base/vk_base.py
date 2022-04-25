import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from other.token_box import token


vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 212770687)
