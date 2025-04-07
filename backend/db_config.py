from pymongo import MongoClient
client = MongoClient(host="localhost", port=27017)

culinary_db = client["culinary-website"]

recipes = culinary_db["recipes"]