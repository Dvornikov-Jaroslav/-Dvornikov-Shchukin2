import requests
from bs4 import BeautifulSoup
import pymorphy2


morph = pymorphy2.MorphAnalyzer()
all_text = list()
quote_marks = ['"', '«', '»', "'", ':', '—']
url = 'https://ilibrary.ru/text/12/index.html#toc'


def get_text(url):
    text = list()
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    article = root.find_all(('span', {'class': 'vl'}) or 'span', {'class': 'p'})
    for elem in article:
        text.append(elem.text)
    return text


def get_paragraphs(url):
    text = list()
    paragraphs = {}
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    article = root.find_all('div', {'class': 'd2'})
    for p in article:
        text.append([p.find('a').text, p.find('a').get('href')])

    # Убираем повторы, преобразую список в словарь и обратно
    for elem in text:
        paragraphs[elem[1]] = elem[0]
    text = list()
    for key in paragraphs:
        text.append([paragraphs[key], key])

    return text


def get_all_text(url):
    url = url[:url.find('/index')]
    pages = get_paragraphs(url)
    for page in pages:
        chapter = list()
        chapter.append(page[0])
        page = 'https://ilibrary.ru' + page[1]
        text = get_text(page)
        chapter.append(text)
        all_text.append(chapter)
    return all_text


def declination(text):
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


def quotes(name):
    all_text = get_all_text(url)
    name = declination(name)
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


quotes('Максим Максимыч')






