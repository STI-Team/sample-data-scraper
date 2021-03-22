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
        "cmlimit": "1000",
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
                for table in tables:
                    print(table.name, table.head)
                    print(table.json())
                all_tables = all_tables + tables

        return all_tables
    except:
        pass


root_category = "Category:Birds"
get_tables(root_category)

subcategories = get_subcategories(root_category)
for subcategory in subcategories:
    get_tables(subcategory["title"])

