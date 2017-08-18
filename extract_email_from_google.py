#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from database import db
from bs4 import BeautifulSoup
import urllib
import re


for entry in db().entreprise.find({"email_txt": {"$exists": True, "$ne": ""}}):

    email = str(entry["email_txt"])
    email_encoded = urllib.quote_plus(email)
    search_url = "https://www.google.fr/search?q=" + '"' + email_encoded + '"'

    html = requests.request("GET", search_url).text
    soup = BeautifulSoup(html, "html.parser")

    try:
        em_tag = soup.find(class_="g").find_next(class_="st").find_next("b").text
        em_tag2 = soup.find(class_="g").find_next(class_="st").text
        match = re.search(r'[\w\.-]+@[\w\.-]+', em_tag2)
        result = match.group(0)
        print "Success | " + result + " | " + em_tag + " | " + search_url + " | " + entry["email_txt"]

        #db().entreprise.update({"_id": entry["_id"]}, {"$set": {"email_txt_regex_google": result, "email_txt_soup_google": em_tag}}, upsert=True)

    except AttributeError:
        print "Error | " + search_url

       #db().entreprise.update({"_id": entry["_id"]}, {"$set": {"email_txt_regex_google": "Error", "email_txt_soup_google": "Error"}}, upsert=True)
