import json
import pathlib
from typing import Any

import requests
from wikitables import import_tables


max_pages = 1000  # this param can sufficiently affect a number of tables scrapped from the source
directory_for_tables = 'C:/Users/79501/datasets/wikipedia/'  # directory to save tables
en_api_url = 'https://en.wikipedia.org/w/api.php'  # URL for English Wikipedia API
ru_api_url = 'https://ru.wikipedia.org/w/api.php'  # URL for Russia Wikipedia API


def get_subcategories(category_title: str, api_url: str) -> list:
    session = requests.Session()
    url = api_url
    params = {
        'action': 'query',
        'cmtitle': category_title,
        'cmtype': 'subcat',
        'list': 'categorymembers',
        'format': 'json'
    }
    response = session.get(url=url, params=params)
    data = response.json()
    pages = data['query']['categorymembers']
    return pages


def get_pages(category_title: str, api_url: str) -> list:
    session = requests.Session()
    url = api_url
    params = {
        'action': 'query',
        'cmtitle': category_title,
        'cmlimit': max_pages,
        'list': 'categorymembers',
        'format': 'json'
    }
    response = session.get(url=url, params=params)
    data = response.json()
    pages = data['query']['categorymembers']
    return pages


def get_tables(category_title: str, api_url: str, lang: str) -> list:
    pages = get_pages(category_title, api_url)
    all_tables = []
    for page in pages:
        page_title = page['title']
        tables = import_tables(article=page_title, lang=lang)
        print(len(tables), 'tables detected in', category_title, ' -> ', page_title)
        if len(tables) > 0:
            all_tables = all_tables + tables
    return all_tables


def save_file(file_name: str, table: Any) -> None:
    path = directory_for_tables + file_name
    if not pathlib.Path(path).exists():
        parsed = json.loads(table.json())
        json_string = json.dumps(parsed, indent=4, ensure_ascii=False).encode("utf8")
        pathlib.Path(path).write_text(json_string.decode(), encoding="utf-8")
        print('New table is saved to ' + file_name)
    else:
        print(file_name + ' exists.')


def save_tables(root_category: str, api_url: str, lang: str) -> None:
    """
    Сохранение извлекаемых таблиц в каталог.
    :param root_category: название корневой категории
    :param api_url: URL для API Википедии
    :param lang: на каком языке будет осуществляться поиск таблиц (возможные значения: 'en' и 'ru')
    :return:
    """
    tables = get_tables(root_category, api_url, lang)
    if tables is not None:
        index = 0
        for table in tables:
            index += 1
            file_name = 'root_category_' + str(index) + '.json'
            save_file(file_name, table)

    subcategories = get_subcategories(root_category, api_url)
    for subcategory in subcategories:
        tables = get_tables(subcategory['title'], api_url, lang)
        if tables is not None:
            index = 0
            for table in tables:
                index += 1
                subcategory_title = subcategory['title'].split(':')
                file_name = subcategory_title[1] + ' ' + str(index) + '.json'
                save_file(file_name, table)


save_tables('Категория:Списки_самолётов', ru_api_url, 'ru')
