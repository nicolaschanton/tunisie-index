import requests
from utils import db
from bs4 import BeautifulSoup


html_domaine = requests.request("GET", "http://www.tunisieindex.com/annuaire-entreprises/").text
soup_domaine = BeautifulSoup(html_domaine, "html.parser")

table = soup_domaine.find(style="margin-left: auto;margin-right: auto;text-align: left;")

for row in table.find_all("tr"):
    td = row.find_all("td")
    for a in td:
        url = a.find("a").get("href")
        title = a.find("img").get("alt", "")

        db().domaine.update({"url": url}, {"$set": {"nom": title, "url": url}}, upsert=True)
