#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from utils import db, get_proxy, random_ua
from bs4 import BeautifulSoup


for entry in db().entreprise.find({}):
    profile_url = entry["url"]

    html = requests.request("GET", profile_url, proxies=get_proxy(), headers={"user-agent": random_ua()},).text
    soup = BeautifulSoup(html, "html.parser")

    try:
        date_indexation = soup.find("b", string="société indexée le :").next_sibling.replace("\n", "").lstrip()
    except AttributeError:
        date_indexation = ""

    try:
        date_creation = soup.find("b", string="Année de Création :").next_sibling.replace(" ", "")
    except AttributeError:
        date_creation = ""

    try:
        adresse_rue = soup.find(itemprop="streetAddress").text
    except AttributeError:
        adresse_rue = ""

    try:
        adresse_cp = soup.find(itemprop="postalCode").text.replace(" ", "")
    except AttributeError:
        adresse_cp = ""

    try:
        adresse_gouvernora = soup.find(itemprop="addressRegion").text
    except AttributeError:
        adresse_gouvernora = ""

    try:
        telephone = soup.find_all(itemprop="telephone")[0].text
    except AttributeError:
        telephone = ""

    try:
        fax = soup.find_all(itemprop="telephone")[1].text
    except (AttributeError, IndexError):
        fax = ""

    try:
        website_url = soup.find(itemprop="url").text.replace(" Site : ", "").replace("\n", "").lstrip().rstrip()
    except AttributeError:
        website_url = ""

    try:
        lectures = soup.find("b", string="Lectures :").next_sibling.replace("\n", "").replace(" ", "").rstrip()
    except AttributeError:
        lectures = ""

    try:
        note = soup.find("b", string="Note :").find_next("img").get("title")
    except AttributeError:
        note = ""

    try:
        email_img = soup.find("b", string="email :").find_next("img").get("src")
    except AttributeError:
        email_img = ""

    try:
        unwanted = soup.find(itemtype="http://schema.org/LocalBusiness").find_all("tr", style="background: #F0EFF2;")[6].find("script").text
        description = soup.find(itemtype="http://schema.org/LocalBusiness").find_all("tr", style="background: #F0EFF2;")[6].text.replace(unwanted, "").rstrip()
    except AttributeError:
        unwanted = ""
        description = ""

    db().entreprise.update({"url": profile_url},
                           {"$set": {"date_indexation": date_indexation,
                                     "date_creation": date_creation,
                                     "adresse_rue": adresse_rue,
                                     "adresse_cp": adresse_cp,
                                     "adresse_gouvernora": adresse_gouvernora,
                                     "telephone": telephone,
                                     "fax": fax,
                                     "website_url": website_url,
                                     "lectures": lectures,
                                     "note": note,
                                     "email_img": email_img,
                                     "description": description}},
                           upsert=True)
