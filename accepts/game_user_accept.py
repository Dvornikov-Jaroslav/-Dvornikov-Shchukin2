from other.marks import quote_marks
from other.send_message import send_message


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
            send_message(user_id, f"Вы не угадали, это — {correct_answer}", keyboard)