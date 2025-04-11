from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db_config import recipes
import json
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class CustomJsonResponse(JsonResponse):
    def __init__(self, data, ensure_ascii=False, **kwargs):
        super().__init__(data, **kwargs)
        self.content = json.dumps(data, ensure_ascii=ensure_ascii).encode('utf-8')

@csrf_exempt
@require_http_methods(["GET", "POST"])
def recipes_api(request):
    if recipes is None:
        logger.error("Ошибка подключение к Бд")
        return JsonResponse({"Ошбика подключения к БД"}, status=503, ensure_ascii=False)
    if request.method == 'GET':
        return _handle_get_recipes(request)
    elif request.method == 'POST':
        return _handle_post_recipe(request)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def recipe_id(request, id):
    if recipes is None:
        logger.error("Ошибка подключение к Бд")
        return JsonResponse({"Ошбика подключения к БД"}, status=503, ensure_ascii=False)
    if request.method == 'GET':
        return _handle_get_recipe_detail(request, id)
    elif request.method == 'PUT':
        return _handle_put_recipe(request, id)
    elif request.method == 'DELETE':
        return _handle_delete_recipe(request, id)

def _handle_get_recipes(request):
    try:
        recipes_cursor = recipes.find({})
        recipes_list = []
        for recipe in recipes_cursor:
            if '_id' in recipe:
                recipe['_id'] = str(recipe['_id'])
            recipes_list.append(recipe)
        return CustomJsonResponse(recipes_list, safe=False, ensure_ascii=False, status=200)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        return JsonResponse({"Неизвестная ошибка"}, status=500)

def _handle_post_recipe(request):
    try:
        data = json.loads(request.body)
        insert_result = recipes.insert_one(data)
        inserted_id = str(insert_result.inserted_id)
        logger.info(f"Рецепт успешно добавлен по id: {inserted_id}")
        return JsonResponse({
            "message": "Recipe added successfully",
            "id": inserted_id
        }, status=201)
    except json.JSONDecodeError:
        logger.error("неверный json формат")
        return JsonResponse({"неверный json формат"}, status=400)
    except Exception as e:
        logger.error(f"Ошибка добавления: {e}", exc_info=True)
        return JsonResponse({"Ошибка добавления"}, status=500)

def _handle_get_recipe_detail(request, id):
    try:
        recipe = recipes.find_one({"_id": ObjectId(id)})
        if recipe:
            recipe['_id'] = str(recipe['_id'])
            return CustomJsonResponse(recipe, safe=False, ensure_ascii=False, status=200)
        else:
            return JsonResponse({"Рецепт не найден"}, status=404)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        return JsonResponse({"Неизвестная ошибка"}, status=500)

def _handle_put_recipe(request, id):
    try:
        data = json.loads(request.body)
        updated_result = recipes.update_one({"_id": ObjectId(id)}, {"$set": data})
        if updated_result.modified_count == 1:
            logger.info(f"Рецепт добавлен по id: {id}")
            return JsonResponse({"Рецепт добавлен"}, status=200)
        else:
            return JsonResponse({"рецепт не найден"}, status=404)
    except json.JSONDecodeError:
        logger.error("неверный json формат")
        return JsonResponse({"неверный json формат"}, status=400)
    except Exception as e:
        logger.error(f"ошбка добавления {e}", exc_info=True)
        return JsonResponse({"ошибка добавления"}, status=500)

def _handle_delete_recipe(request, id):
    try:
        delete_result = recipes.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 1:
            logger.info(f"рецепт успешно удален по id: {id}")
            return JsonResponse("рецепт успешно удален", status=200)
        else:
            return JsonResponse("рецепт не найден", status=404)
    except Exception as e:
        logger.error("ошибка удаления рецепта", exc_info=True)
        return JsonResponse("ошибка удаления рецепта", status=500)