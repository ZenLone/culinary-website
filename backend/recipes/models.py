from pymongo.collection import Collection
from db_config import culinary_db

class Recipe:
    @staticmethod
    def get_all_recipes():
        return list(culinary_db['recipes'].find())