from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db_config import recipes
import json
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def recipes_api(request):
    if recipes is None:
        logger.error("Ошибка подключение к Бд")
        return JsonResponse({"error": "Database service unavailable"}, status=503, ensure_ascii=False)
    if request.method == 'GET':
        return _handle_get_recipes(request)
    elif request.method == 'POST':
        return _handle_post_recipe(request)
    elif request.method == "DELETE":
        return _handle_delete_recipe(request)


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
                recipe['_id'] = str(recipe['_id']) 
            recipes_list.append(recipe)
        # Используем CustomJsonResponse
        return CustomJsonResponse(recipes_list, ensure_ascii=False, safe=False, status=200)
    
    except Exception as e:
        logger.error(f"Error fetching recipes from MongoDB: {e}", exc_info=True)
        return CustomJsonResponse({"error": "Failed to fetch recipes"}, ensure_ascii=False, status=500)

def _handle_post_recipe(request):
    data = json.loads(request.body)
        # Insert into MongoDB
    insert_result = recipes.insert_one(data)
    inserted_id = str(insert_result.inserted_id)
    logger.info(f"Successfully added new recipe with ID: {inserted_id}")

        # Return success response
    return JsonResponse({
            "message": "Recipe added successfully",
            "inserted_id": inserted_id
        }, status=201)

def _handle_delete_recipe(request):
    data = json.loads(request.body)
    recipes_id = data.get("id")
    Object_Id = ObjectId(recipes_id)
    delete_recipes = recipes.delete_one({"id": Object_Id})
    if delete_recipes.deleted_count == 1:
        logger.info(recipes_id, " Id успешно удалено")
        return JsonResponse({"message": "Recipe deleted successfully"}, status=200, ensure_ascii=False)
    else:
        logger.warning( recipes_id, "Это id не удалось удалить")
        return JsonResponse({"error": "Recipe not found"}, status=404, ensure_ascii=False)