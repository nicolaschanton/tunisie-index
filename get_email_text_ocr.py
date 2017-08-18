#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import db
import requests


for entreprise in db().entreprise.find({"email_img": {"$not": ""}}):

    if db().ocr_results.find_one({"entreprise": entreprise["_id"]}) == "":

        image_url = entreprise["email_img"]

        url = "https://vision.googleapis.com/v1/images:annotate"

        querystring = {"key": "XXXXXXXXXXXXXXXXXXXX"}

        payload = """{\n  \"requests\": [\n    {\n      \"image\": {\n        \"source\":{\n          \"imageUri\":\n \"""" + image_url + """\"}},\n      \"features\": [\n        {\n          \"type\": \"TEXT_DETECTION\"\n        }\n      ]\n    }\n  ]\n}"""

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        db().ocr_results.update({"entreprise": entreprise["_id"]}, {"$set": {"results": response.json()}}, upsert=True)

        db().entreprise.update({"_id": entreprise["_id"]}, {"$set": {"email_txt": response.json()["responses"][0]["fullTextAnnotation"]["text"].rstrip().lstrip().replace("\n", "")}}, upsert=True)

    else:
        db().entreprise.update({"_id": entreprise["_id"]}, {"$set": {"email_txt": db().ocr_results.find_one({"entreprise": entreprise["_id"]})["results"]["responses"][0]["fullTextAnnotation"]["text"].rstrip().lstrip().replace("\n", "")}}, upsert=True)
