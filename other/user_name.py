from base.vk_base import vk


def get_user_name(user_id):
    user_get = vk.users.get(user_ids=user_id)
    user_get = user_get[0]

    first_name = user_get['first_name']  # Имя пользователя
    last_name = user_get['last_name']  # Фамилия

    return [first_name, last_name]
