from pymongo.collection import Collection
from db_config import mongo_client

# Получаем коллекцию рецептов
recipes_collection = mongo_client['culinary_website']['recipes']

class Recipe:
    @staticmethod
    def get_all_recipes():
        return list(recipes_collection.find({}))