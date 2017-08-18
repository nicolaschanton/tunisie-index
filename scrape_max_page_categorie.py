import requests
from database import db
from bs4 import BeautifulSoup


for entry in db().categorie.find({}):
    url = entry["url"]

    html_categorie = requests.request("GET", url).text
    soup_categorie = BeautifulSoup(html_categorie, "html.parser")

    try:
        table = soup_categorie.find(style="margin-left: auto;margin-right: auto;text-align: left;", width="90%")

        page_list = []

        for a_tag in table.find_all("a"):
            string_page = a_tag.text

            if string_page == ">":
                continue
            else:
                int_page = int(string_page)
                page_list.append(int_page)
                max_page = max(page_list)

        db().categorie.update({"url": url}, {"$set": {"max_page": max_page}}, upsert=True)

        print url, max_page

    except AttributeError:
        db().categorie.update({"url": url}, {"$set": {"max_page": 1}}, upsert=True)
