from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db_config import recipes
import json
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def recipes_api(request):
    if recipes is None:
        logger.error("Attempted API access while database connection is unavailable.")
        return JsonResponse({"error": "Database service unavailable"}, status=503, ensure_ascii=False)

    if request.method == 'GET':
        return _handle_get_recipes(request)
    elif request.method == 'POST':
        return _handle_post_recipe(request)


class CustomJsonResponse(JsonResponse):
    def __init__(self, data, ensure_ascii=False, **kwargs):
        # Сериализация данных с ensure_ascii
        super().__init__(data, **kwargs)
        self.content = json.dumps(data, ensure_ascii=ensure_ascii).encode('utf-8')

def _handle_get_recipes(request):
    try:
        recipes_cursor = recipes.find({})
        recipes_list = []
        for recipe in recipes_cursor:
            if '_id' in recipe:
                recipe['_id'] = str(recipe['_id'])  # Convert ObjectId to string
            recipes_list.append(recipe)
        
        logger.info(f"Successfully fetched {len(recipes_list)} recipes.")
        
        # Используем CustomJsonResponse
        return CustomJsonResponse(recipes_list, ensure_ascii=False, safe=False, status=200)
    
    except Exception as e:
        logger.error(f"Error fetching recipes from MongoDB: {e}", exc_info=True)
        return CustomJsonResponse({"error": "Failed to fetch recipes"}, ensure_ascii=False, status=500)

def _handle_post_recipe(request):
    """Handles POST requests to add a new recipe."""
    logger.info("Handling POST request to add a new recipe")
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)
        logger.debug(f"Received data for new recipe: {data}")

        # Basic Validation
        required_fields = ['name', 'ingredients', 'time']
        missing = [field for field in required_fields if field not in data or not data[field]]
        if missing:
            logger.warning(f"Missing or empty required fields in POST request: {missing}")
            return JsonResponse(
                {"error": f"Missing or empty required fields: {', '.join(missing)}"},
                status=400,
                ensure_ascii=False
            )

        # Data Processing
        if 'ingredients' in data and isinstance(data['ingredients'], str):
            data['ingredients'] = [ing.strip() for ing in data['ingredients'].split(',') if ing.strip()]
            logger.debug(f"Processed ingredients string into list: {data['ingredients']}")
        elif 'ingredients' not in data or not isinstance(data['ingredients'], list):
            logger.warning("Ingredients field missing or not a list/string.")
            data['ingredients'] = []

        # Insert into MongoDB
        insert_result = recipes.insert_one(data)
        inserted_id = str(insert_result.inserted_id)
        logger.info(f"Successfully added new recipe with ID: {inserted_id}")

        # Return success response
        return JsonResponse({
            "message": "Recipe added successfully",
            "inserted_id": inserted_id
        }, status=201)

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in POST request body.")
        return JsonResponse({"error": "Invalid JSON format in request body"}, status=400, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error processing POST request to add recipe: {e}", exc_info=True)
        return JsonResponse({"error": "An internal server error occurred"}, status=500, ensure_ascii=False)


