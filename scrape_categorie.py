import requests
from database import db
from bs4 import BeautifulSoup


for entry in db().domaine.find({}):
    url = entry["url"]

    html_categorie = requests.request("GET", url).text
    soup_categorie = BeautifulSoup(html_categorie, "html.parser")

    try:
        table = soup_categorie.find(style="margin-left: auto;margin-right: auto;text-align: left;")

        for row in table.find_all("tr"):
            td = row.find_all("td")
            for a in td:
                url_cible = a.find("a").get("href")
                title = a.find("img").get("alt", "")

                db().categorie.update({"url": url_cible}, {"$set": {"nom": title, "url": url_cible, "domaine": entry["_id"]}}, upsert=True)

    except AttributeError:
        db().categorie.update({"url": url}, {"$set": {"nom": entry["nom"], "url": url, "domaine": entry["_id"]}}, upsert=True)
        continue
