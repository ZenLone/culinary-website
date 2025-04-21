from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from gridfs import GridFS

# Initialize variables as None to indicate uninitialized state
client = None
culinary_db = None
recipes = None
try:
    # client = MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=5000)
    client = MongoClient('mongodb+srv://ZenLone:R22E05D2007k@zenlone.ckgp0oh.mongodb.net/?retryWrites=true&w=majority&appName=ZenLone')
    client.admin.command('ismaster')
    culinary_db = client["culinary-website"]
    recipes = culinary_db["recipes"]
    profiles = culinary_db["profiles"]
    photo = culinary_db["photo"]
    fs = GridFS(photo)
    if recipes is None:
        print("коллекция recepies не найдена")
    if profiles is None:
        print("коллекция profiles не найдена")
    if photo is None:
        print("коллекция photo не найдена")

except ConnectionFailure as e:
    print(f"Ошибка подключения к БД: {e}")
except Exception as e:
    print(f"Ошибка загрузки данных из БД: {e}")
