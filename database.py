from pymongo import MongoClient


def db():
    client = MongoClient("XXXXXXXXXX")
    tn = client.tunisie

    return tn

