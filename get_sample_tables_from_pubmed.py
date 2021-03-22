def search_articles(query) -> []:
    import requests
    from bs4 import BeautifulSoup as bs

    session = requests.Session()
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pmc",
        "retmax": "20",
        "term": query
    }

    response = session.get(url=url, params=params)
    # print(response.text)

    soup = bs(response.text, "lxml")
    tags = soup.findAll("id")
    result = []
    for tag in tags:
        result.append(tag.text)

    # print(result)
    return result


def get_article(pmcid) -> str:
    import requests

    session = requests.Session()
    url = "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"

    params = {
        "verb": "GetRecord",
        "identifier": "oai:pubmedcentral.nih.gov:" + pmcid,
        "metadataPrefix": "pmc"
    }

    response = session.get(url=url, params=params)
    return response.text


def parse_html_table(table):
    import pandas as pd

    n_columns = 0
    n_rows = 0
    column_names = []
    try:
        # Find number of rows and columns
        # Find column titles as possible
        for row in table.find_all('tr'):

            # Determine the number of rows in the table
            td_nodes = row.find_all('td')
            if len(td_nodes) > 0:
                n_rows += 1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_nodes)

            # Handle column names as possible
            th_nodes = row.find_all('th')
            if len(th_nodes) > 0 and len(column_names) == 0:
                for th in th_nodes:
                    content = th.get_text().replace("\n", " ").strip()
                    column_names.append(content)

        # Safeguard on the column titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            # raise Exception("Column titles do not match the number of columns")
            return

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns, index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                content = column.get_text().replace("\n", " ").strip()
                df.iat[row_marker, column_marker] = content
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1

        return df
    except:
        pass


def convert_table_from_html_to_json(table):
    print("get table here")


pcmids = search_articles("cancer")
# pcmids = ['156895']
print(pcmids)

from bs4 import BeautifulSoup as bs
import json

try:
    for pcmid in pcmids:
        text = get_article(pcmid)

        text = text.encode('latin-1')
        bs_content = bs(text, "lxml")

        table_nodes = bs_content.findAll("table")
        if len(table_nodes) > 0:
            print(len(table_nodes), "tables detected in", pcmid)
            for table_node in table_nodes:
                df = parse_html_table(table_node)
                if df is not None:
                    print(df)
                    result = df.to_json(orient="records", force_ascii=False)
                    parsed = json.loads(result)
                    json_string = json.dumps(parsed, indent=4, ensure_ascii=False).encode('utf8')
                    print(json_string.decode())
except:
    pass
