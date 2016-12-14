import pymongo
import json
from pprint import pprint

with open('items.json', 'r') as f:
    questions = json.load(f)

client = pymongo.MongoClient('localhost', 27017)
db = client['stackoverflow']
collection = db['questions']


for question in questions:
    collection.insert_one(question)