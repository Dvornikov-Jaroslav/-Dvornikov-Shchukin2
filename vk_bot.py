import requests
from bs4 import BeautifulSoup
import pymorphy2
import random


morph = pymorphy2.MorphAnalyzer()
all_text = list()
quote_marks = ['"', '«', '»', "'", ':', '—']


class Bot:
    def __init__(self):
        self.url = 'https://ilibrary.ru/text/1118/index.html'

    def get_text(self, page):
        text = list()
        rs = requests.get(page)
        root = BeautifulSoup(rs.content, 'html.parser')

        article = root.find_all(('span', {'class': 'vl'}) or ('span', {'class': 'p'}))
        for elem in article:
            text.append(elem.text)
        return text

    def get_paragraphs(self, url):
        text = list()
        paragraphs = {}
        rs = requests.get(url)
        root = BeautifulSoup(rs.content, 'html.parser')

        article1 = root.find_all('div', {'class': 'd2'})
        article2 = root.find_all('a', {'class': 'bttn'})
        for p in article1:
            text.append([p.find('a').text, p.find('a').get('href')])
        for p in article2:
            text.append(['', p.get('href')])

        # Убираем повторы, преобразовав список в словарь и обратно
        for elem in text:
            paragraphs[elem[1]] = elem[0]
        text = list()
        for key in paragraphs:
            text.append([paragraphs[key], key])

        return text

    def get_all_text(self, url):
        pages = self.get_paragraphs(url)
        for page in pages:
            chapter = list()
            chapter.append(page[0])
            page = 'https://ilibrary.ru' + page[1]
            text = self.get_text(page)
            chapter.append(text)
            all_text.append(chapter)
        return all_text

    def declination(self, text):
        text = text.split()
        for i in range(len(text)):
            morph_name = morph.parse(text[i])[0]
            phorms = [part.word for part in morph_name.lexeme]
            for part in phorms:
                text.append(part)
            phorms.clear()
        # Убираем повторы
        text = list(dict.fromkeys(text))
        return text

    def quotes(self, name):
        all_text = self.get_all_text(self.url)
        name = self.declination(name)
        coincidence = list()

        for elem in all_text:
            for string in elem[1]:
                for part in name:
                    if part in string or part.capitalize() in string:
                        for mark in quote_marks:
                            if mark in string:
                                coincidence.append(string)
        # Убираем повторы
        coincidence = list(dict.fromkeys(coincidence))
        for elem in coincidence:
            print(elem)

    def createMiniGame(self):
        game = MiniGame('easy')
        game.level_formation()
        # url оглавления произведения
        url = game.composition_url.split('p.')[0] + 'index.html'
        # подключаемся к оглавлению произведения, чтобы определить дату его написания
        rs = requests.get(url)
        root = BeautifulSoup(rs.content, 'html.parser')

        date = root.find('div', {'class': 'tabout'})
        if date:
            date = date.text.split(' ')[2].split('\xa0')[0]
            # Проверка на правильность определения даты
            try:
                date = int(date)
            except BaseException:
                date = '***'
        else:
            date = '***'

        text = self.get_all_text(url)
        # Проверка на ошибку получения данных с сайта
        while len(text) == 0:
            game = MiniGame('easy')
            game.level_formation()
            # url оглавления произведения
            url = game.composition_url.split('p.')[0] + 'index.html'
            # подключаемся к оглавлению произведения, чтобы определить дату его написания
            rs = requests.get(url)
            root = BeautifulSoup(rs.content, 'html.parser')

            date = root.find('div', {'class': 'tabout'}).text.split(' ')[2].split('\xa0')[0]

            text = self.get_all_text(url)

        # Удаляем ненужные элементы
        correct_text = list()
        for i in range(len(text)):
            correct_text.append(['', []])
            if text[i] != ['', []]:
                correct_text[i][0] = text[i][0]
                for j in range(len(text[i][1])):
                    if text[i][1][j] != '' and text[i][1][j] != '\n':
                        correct_text[i][1].append(text[i][1][j])
        # Удаляем рекламную информацию
        if len(correct_text) != 1:
            correct_text.remove(correct_text[len(correct_text) - 1])
        l = len(correct_text) - 1
        correct_text[l][1].remove(correct_text[l][1][len(correct_text[l][1]) - 1])
        correct_text[l][1].remove(correct_text[l][1][len(correct_text[l][1]) - 1])
        correct_text[l][1].remove(correct_text[l][1][len(correct_text[l][1]) - 1])
        correct_text[l][1].remove(correct_text[l][1][len(correct_text[l][1]) - 1])

        number_of_chapters = len(text)
        if number_of_chapters != 1:
            number_of_chapters -= 1

        # склоняем слово под получившеюся цифру
        word = morph.parse('глава')[0]
        word = word.make_agree_with_number(number_of_chapters).word
        # Получаем случайный отрывок из произведения
        print(game.composition_name)
        print(correct_text)
        print(len(correct_text))
        chapter = random.randint(0, len(correct_text) - 1)
        print(f'chapter {chapter}')
        p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
        p = text[chapter][1][p_ch]
        while len(p) == 0:
            p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
            p = text[chapter][1][p_ch]
        # Захватываем следущий абзац, если в изначально выбранном меньше 150 символов
        while len(p) < 150 or (p[len(p) - 1] != '.' and p[len(p) - 1] != '!' and p[len(p) - 1] != '?'):
            # если выбранный абзац является последним в выбранной главе, то сбрасываем
            # выделенный абзац и выбираем передыдущий
            if len(correct_text[chapter][1]) - 1 != p_ch:
                p_ch += 1
                print('+', p_ch)

            else:
                print('-')
                p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
                p = ''

            p = (p + '\n' + correct_text[chapter][1][p_ch]).split('\n')
            print(p)
            par = list()
            for elem in p:
                if elem != '':
                    par.append(elem)
            p = '\n'.join(par)
            if p.find('Email:') != -1:
                print('email error', p.split('Email:'))
                p = ''.join(p.split('Email:')[0])

        p1 = list()
        if len(p) > 300:
            print(list(p[300:]))
            for i in range(len(list(p[300:]))):
                if list(p[300:])[i] != '.' and list(p[300:])[i] and '!' and list(p[300:])[i] != '?':
                    p1.append(list(p[300:])[i])
                    print('if')
                else:
                    print('else')
                    p1.append(list(p[300:])[i])
                    break
        p = p[:300] + ''.join(p1)

        print(f'Это произведенеие написано в {date} году, '
              f'автор: {game.author_name}, в нем {number_of_chapters} {word}, отрывок из произведения:')
        print(p)
        print(f'Название произведения: {game.composition_name}')

        game.response_accept(input())


class MiniGame:
    def __init__(self, level):
        self.level = level
        self.author_url = 'https://ilibrary.ru/author.html'

    def level_formation(self):
        composition = list()
        author = list()
        rs = requests.get(self.author_url)
        root = BeautifulSoup(rs.content, 'html.parser')
        # Получаем список ссылок на всех доступнх авторов
        article = root.find_all('div', {'class': 'ab'})
        for p in article:
            authors = p.find_all('a')
            for auth in authors:
                author.append([('https://ilibrary.ru' + auth.get('href')), auth.text])
        # Выбираем случайную ссылку
        author = random.choice(author)
        self.author_name = author[1]
        # Подключаемя к списку произведений выбранного автора
        rs = requests.get(author[0])
        root = BeautifulSoup(rs.content, 'html.parser')
        article = root.find_all('div', {'class': 'list'})
        for p in article:
            compositions = p.find_all('a')
            for comp in compositions:
                composition.append(['https://ilibrary.ru' + comp.get('href'), comp.text])
        # Выбираем случайную ссылку
        composition = random.choice(composition)
        self.composition_url = composition[0]
        self.composition_name = composition[1]

    def response_accept(self, response):
        correct_answer = list(self.composition_name)
        for b in correct_answer:
            if b in quote_marks:
                correct_answer.remove(b)
        correct_answer = ''.join(correct_answer)
        if response == correct_answer:
            print(f"Да вы знаток русской литературы! Это и вправду {correct_answer}!")
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
                    print(f'Вы почти угадали, это — {correct_answer}')
                else:
                    print(f'Ну вы хоть попытались... Это — {correct_answer}')
            else:
                print(f"Вы не угадали, это {correct_answer}")


bot = Bot()
bot.createMiniGame()

# В ответе(quotes) очень много текста(целый абзац для каждого ответа), т.е нужно обрезать строки
# (думаю, что нуужно сделать алгоритм, отслеживающий конец кавычки/или точку(для тире или двоеточия)
# и обрезающий ненужное)




