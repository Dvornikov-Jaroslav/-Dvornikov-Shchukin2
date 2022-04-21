import requests
from bs4 import BeautifulSoup
import pymorphy2
import random
from marks import quote_marks

morph = pymorphy2.MorphAnalyzer()
all_text = list()


class Bot:
    def __init__(self):
        self.url = 'https://ilibrary.ru/text/12/index.html'

    def get_text(self, page):
        rs = requests.get(page)
        root = BeautifulSoup(rs.content, 'html.parser')

        article = root.find_all('span', {'class': 'p'})
        clear_article = list()
        for elem in article:
            if elem != '' and elem != '\n':
                clear_article.append(elem.text)
        if len(clear_article) == 1:
            clear_article[0] = color.BLUE, color.BOLD + clear_article[0] + color.END
        return clear_article

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
        itog = []
        coincidence = list(dict.fromkeys(coincidence))
        for i in range(len(coincidence)):
            coincidence[i] = coincidence[i].split('\n')
            for j in range(len(coincidence[i])):
                if name[0] in coincidence[i][j]:
                    itog.append(coincidence[i][j])
        itog = set(itog)
        return itog

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

        try:
            for _ in range(4):
                correct_text[l][1].remove(correct_text[l][1][len(correct_text[l][1]) - 1])
        except BaseException:
            pass

        number_of_chapters = len(text)
        if number_of_chapters != 1:
            number_of_chapters -= 1

        # склоняем слово под получившеюся цифру
        word = morph.parse('глава')[0]
        word = word.make_agree_with_number(number_of_chapters).word
        # Получаем случайный отрывок из произведения
        if len(correct_text) - 1 == 0:
            chapter = 0
        else:
            chapter = random.randint(0, len(correct_text) - 1)
        if len(correct_text[chapter][1]) - 1 < 1:
            p_ch = 0
        else:
            p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
        p = correct_text[chapter][1][p_ch]
        while len(p) == 0:
            if len(correct_text[chapter][1]) - 1 < 1:
                p_ch = 0
            else:
                p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
            p = text[chapter][1][p_ch]
        # Захватываем следущий абзац, если в изначально выбранном меньше 150 символов
        while len(p) < 150 or (p[len(p) - 1] != '.' and p[len(p) - 1] != '!' and p[len(p) - 1] != '?'):
            # если выбранный абзац является последним в выбранной главе, то сбрасываем
            # выделенный абзац и выбираем передыдущий
            if len(correct_text[chapter][1]) - 1 != p_ch:
                p_ch += 1

            else:
                p_ch = random.randint(0, len(correct_text[chapter][1]) - 1)
                p = ''

            p = (p + '\n' + correct_text[chapter][1][p_ch]).split('\n')
            par = list()
            for elem in p:
                if elem != '':
                    par.append(elem)
            p = '\n'.join(par)
            if p.find('Email:') != -1:
                p = ''.join(p.split('Email:')[0])

        p1 = list()
        if len(p) > 300:
            for i in range(len(list(p[300:]))):
                if list(p[300:])[i] != '.' and list(p[300:])[i] and '!' and list(p[300:])[i] != '?':
                    p1.append(list(p[300:])[i])
                else:
                    p1.append(list(p[300:])[i])
                    break
        fragment = p[:300] + ''.join(p1)

        self.game = game

        return [
            f'Это произведенеие написано в {date} году, автор: {game.author_name},'
            f' в нем {number_of_chapters} {word}, отрывок из произведения:', '',
            fragment, '', 'Напишите его название:'
        ]

        # game.response_accept(input())


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




class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


'''
bot = Bot()
bot.createMiniGame()
'''
# В ответе(quotes) очень много текста(целый абзац для каждого ответа), т.е нужно обрезать строки
# (думаю, что нужно сделать алгоритм, отслеживающий конец кавычки/или точку(для тире или двоеточия)
# и обрезающий ненужное)


# можно сделать ее одну мини-игру: угадай век(дату) написания произведения(с указанием автора)
