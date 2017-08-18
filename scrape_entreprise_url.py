import requests
from database import db
from bs4 import BeautifulSoup


for entry in db().categorie.find({}):

    for nb in range(0, entry["max_page"]):
        urll = entry["url"]+"societes-classees-par-date-page-"+str(nb)+".html"

        html_categorie = requests.request("GET", urll).text
        soup_categorie = BeautifulSoup(html_categorie, "html.parser")

        tables_list = soup_categorie.find_all(style="background: #FFFFFF;", width="100%")

        for table in tables_list:
            td_list = table.find_all(class_="entreprises")
            for td in td_list:
                url_entreprise = td.find("a").get("href")
                nom_entreprise = td.find("a").text.replace(":", "")

                db().entreprise.update({"url": url_entreprise}, {"$set": {"url": url_entreprise, "nom": nom_entreprise, "categorie": entry["_id"]}}, upsert=True)