from pymongo import MongoClient

client = MongoClient('mongodb://7characters:Karacosta1@ds121565.mlab.com:21565/wheeldata')

db = client['wheeldata']
session = db.dataset

session.insert({"poo": "wee"})


