# This param can sufficiently affect a number of tables scrapped from the source
max_of_pages = 1000


def get_subcategories(category_title) -> []:
    import requests

    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "cmtitle": category_title,
        "cmtype": "subcat",
        "list": "categorymembers",
        "format": "json"
    }

    response = session.get(url=url, params=params)
    data = response.json()

    pages = data["query"]["categorymembers"]

    return pages


def get_pages(category_title) -> []:
    import requests

    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "cmtitle": category_title,
        "cmlimit": max_of_pages,
        "list": "categorymembers",
        "format": "json"
    }

    response = session.get(url=url, params=params)
    data = response.json()

    pages = data['query']['categorymembers']

    return pages


def get_tables(category_title) -> []:
    from wikitables import import_tables

    try:
        pages = get_pages(category_title)
        all_tables = []
        for page in pages:
            page_title = page['title']
            tables = import_tables(page_title)
            print(len(tables), "tables detected in", category_title, " -> ", page_title)
            if len(tables) > 0:
                all_tables = all_tables + tables

        return all_tables
    except:
        pass


def save_tables(directory_for_tables, root_category):
    """
    Сохранение извлекаемых таблиц в каталог
    :param directory_for_tables: каталог для сохранения таблиц
    :param root_category: название корневой категории
    :return:
    """
    import pathlib

    tables = get_tables(root_category)
    if tables is not None:
        index = 0
        for table in tables:
            index += 1
            file_name = "root_category_" + str(index) + ".json"
            path = directory_for_tables + file_name
            if not pathlib.Path(path).exists():
                pathlib.Path(path).write_text(table.json(), encoding="utf-8")
                print("New table is saved to " + file_name)
            else:
                print(file_name + " exists.")

    subcategories = get_subcategories(root_category)
    for subcategory in subcategories:
        tables = get_tables(subcategory["title"])
        if tables is not None:
            index = 0
            for table in tables:
                index += 1
                subcategory_title = subcategory["title"].split(":")
                file_name = subcategory_title[1] + " " + str(index) + ".json"
                path = directory_for_tables + file_name
                if not pathlib.Path(path).exists():
                    pathlib.Path(path).write_text(table.json(), encoding="utf-8")
                    print("New table is saved to " + file_name)
                else:
                    print(file_name + " exists.")


save_tables("C:/Users/79501/datasets/wikipedia/", "Category:Birds")
