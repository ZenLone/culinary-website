from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Initialize variables as None to indicate uninitialized state
client = None
culinary_db = None
recipes = None

print("Attempting to connect to MongoDB at localhost:27017...")
try:
    # client = MongoClient(host="localhost", port=27017, serverSelectionTimeoutMS=5000)
    client = MongoClient('mongodb+srv://ZenLone:R22E05D2007k@zenlone.ckgp0oh.mongodb.net/?retryWrites=true&w=majority&appName=ZenLone')
    client.admin.command('ismaster')
    print("MongoDB connection successful.")

    culinary_db = client["culinary-website"]
    print(f"Selected database: {culinary_db.name}")

    recipes = culinary_db["recipes"]
    print(f"Selected collection: {recipes.name}")

    if recipes is None:
        # This case should ideally not happen if the above lines succeed
        print("ERROR: 'recipes' collection object is None even after assignment.")

except ConnectionFailure as e:
    print(f"ERROR: Could not connect to MongoDB: {e}")
    # Keep recipes as None to indicate failure
except Exception as e:
    print(f"ERROR: An unexpected error occurred during MongoDB setup: {e}")
    # Keep recipes as None to indicate failure
