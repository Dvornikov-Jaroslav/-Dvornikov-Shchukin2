import requests
from bs4 import BeautifulSoup


all_text = list()


def get_text(url):
    text = list()
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    article = root.find_all('span', {'class': 'vl'})
    for elem in article:
        text.append(elem.text)
    return text


def get_paragraphs(url):
    text = list()
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')

    article = root.find_all('div', {'class': 'd2'})
    for p in article:
        text.append(p.find('a').get('href'))
    return text


url = 'https://ilibrary.ru/text/436/index.html#toc'
url = url[:url.find('/index')]
# https://ilibrary.ru/text/436
pages = get_paragraphs(url)
for page in pages:
    page = 'https://ilibrary.ru' + page
    text = get_text(page)
    for elem in text:
        all_text.append(" ".join(elem.split()))
print(all_text)