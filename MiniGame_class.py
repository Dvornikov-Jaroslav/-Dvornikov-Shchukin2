from bs4 import BeautifulSoup
import requests
import random


class MiniGame:
    def __init__(self):
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

        self.composition_url = composition[0][:composition[0].find('p.')] + 'index.html'
        self.composition_name = composition[1]