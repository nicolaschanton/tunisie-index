#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from database import db


export_file = open("/Users/nicolaschanton/PycharmProjects/tunisie_index/extract.csv", "wb")
export_writer = csv.writer(export_file, delimiter="|", quotechar='"', quoting=csv.QUOTE_ALL)

header = ["NOM", "CATEGORIE", "DOMAINE", "URL", "TEL", "EMAIL", "RUE", "CP", "GOUV"]
export_writer.writerow(header)

for entry in db().entreprise.find({"email_txt": {"$exists": True, "$ne": ""}}):

    data = [entry["nom"].encode('ascii', 'ignore'),
            db().categorie.find_one({"_id": entry["categorie"]})["nom"].encode('ascii', 'ignore'),
            db().domaine.find_one({"_id": db().categorie.find_one({"_id": entry["categorie"]})["domaine"]})["nom"].encode('ascii', 'ignore'),
            entry["url"].encode('ascii', 'ignore'),
            entry["telephone"].encode('ascii', 'ignore'),
            entry["email_txt"].encode('ascii', 'ignore'),
            entry["adresse_rue"].encode('ascii', 'ignore'),
            entry["adresse_cp"].encode('ascii', 'ignore'),
            entry["adresse_gouvernora"].encode('ascii', 'ignore'),
            ]
    export_writer.writerow(data)
