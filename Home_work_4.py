# Возьмем, например, список стран и их столиц с википедии

import requests
from lxml import html
import csv

# URL для запроса данных
url = 'https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_and_their_capitals_in_native_languages'

# Заголовки запроса, включая строку агента пользователя
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # Отправление запроса на получение данных с указанными заголовками
    response = requests.get(url, headers=headers)

    # Проверка, что запрос был успешным
    response.raise_for_status()

    # Использование lxml для анализа полученного HTML
    tree = html.fromstring(response.content)

    # Определение XPath для выбора интересующих нас данных таблицы
    # Например, для википедии пути могут быть следующими:
    countries = tree.xpath(
        '//table[contains(@class,"wikitable")]/tbody/tr/td[1]//text()')
    capitals = tree.xpath(
        '//table[contains(@class,"wikitable")]/tbody/tr/td[2]//text()')

    # Сравнение стран и столиц (предполагается, что каждой стране соответствует столица)
    data = zip(countries, capitals)

    # Сохранение данные в CSV
    with open('countries_and_capitals.csv', 'w', newline='',
              encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Country", "Capital"])  # Заголовки столбцов
        csvwriter.writerows(data)

# проверки
except requests.HTTPError as e:
    print(f"Ошибка запроса HTTP: {e}")
except requests.RequestException as e:
    print(f"Ошибка запроса: {e}")
except lxml.etree.ParserError as e:
    print(f"Ошибка парсинга HTML: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
