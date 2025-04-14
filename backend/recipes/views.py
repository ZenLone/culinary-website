from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from db_config import recipes
from backend import settings
import json
from bson import ObjectId
import logging
import jwt

logger = logging.getLogger(__name__)

class CustomJsonResponse(JsonResponse):
    def __init__(self, data, ensure_ascii=False, **kwargs):
        super().__init__(data, **kwargs)
        self.content = json.dumps(data, ensure_ascii=ensure_ascii).encode('utf-8')

def _decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError: # Токен истек
        return None
    except jwt.InvalidTokenError: # Неверный токен
        return None

def _get_user_id_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    parts = auth_header.split(' ')
    if len(parts) != 2:
        return None

    token = parts[1]
    if not token:
        return None
    payload = _decode_jwt(token)
    if payload:
        return payload.get('user_id')
    return None

@csrf_exempt
@require_http_methods(["GET", "POST"])
def recipes_api(request):
    if recipes is None:
        logger.error("Ошибка подключение к Бд")
        return CustomJsonResponse({"message": "Ошбика подключения к БД"}, status=503)
    
    user_id = _get_user_id_from_token(request)
    if not user_id:
        return CustomJsonResponse({"message": "Ошибка авторизации"}, status=401)

    if request.method == 'GET':
        return _handle_get_recipes(request, user_id)
    elif request.method == 'POST':
        return _handle_post_recipe(request, user_id)

@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def recipe_id(request, id):
    if recipes is None:
        logger.error("Ошибка подключение к Бд")
        return CustomJsonResponse({"message": "Ошбика подключения к БД"}, status=503)
    
    user_id = _get_user_id_from_token(request)
    if not user_id:
        return CustomJsonResponse({"message": "Ошибка авторизации"}, status=401)

    if request.method == 'GET':
        return _handle_get_recipe_detail(request, id, user_id)
    elif request.method == 'DELETE':
        return _handle_delete_recipe(request, id, user_id)

def _handle_get_recipes(request, user_id):
    try:
        recipes_cursor = recipes.find({"user_id": user_id})
        recipes_list = []
        for recipe in recipes_cursor:
            if '_id' in recipe:
                recipe['_id'] = str(recipe['_id'])
            recipes_list.append(recipe)
        return CustomJsonResponse(recipes_list, safe=False, status=200)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        return CustomJsonResponse({"message": "Неизвестная ошибка"}, status=500)

def _handle_post_recipe(request, user_id):
    try:
        data = json.loads(request.body)
        data['user_id'] = user_id   # Добавляем user_id к данным рецепта
        insert_result = recipes.insert_one(data)
        inserted_id = str(insert_result.inserted_id)
        logger.info(f"Рецепт успешно добавлен по id: {inserted_id}")
        return CustomJsonResponse({
            "message": "Recipe added successfully",
            "id": inserted_id
        }, status=201)
    except json.JSONDecodeError:
        logger.error("неверный json формат")
        return CustomJsonResponse({"message": "неверный json формат"}, status=400)
    except Exception as e:
        logger.error(f"Ошибка добавления: {e}", exc_info=True)
        return CustomJsonResponse({"message": "Ошибка добавления"}, status=500)

def _handle_get_recipe_detail(request, id, user_id):
    try:
        recipe = recipes.find_one({"_id": ObjectId(id), "user_id": user_id})
        if recipe:
            recipe['_id'] = str(recipe['_id'])
            return CustomJsonResponse(recipe, safe=False, status=200)
        else:
            return CustomJsonResponse({"message": "Рецепт не найден"}, status=404)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
        return CustomJsonResponse({"message": "Неизвестная ошибка"}, status=500)

def _handle_delete_recipe(request, id, user_id):
    try:
        delete_result = recipes.delete_one({"_id": ObjectId(id), "user_id": user_id})
        if delete_result.deleted_count == 1:
            logger.info(f"рецепт успешно удален по id: {id}")
            return CustomJsonResponse({"message": "рецепт успешно удален"}, status=200)
        else:
            return CustomJsonResponse({"message": "рецепт не найден"}, status=404)
    except Exception as e:
        logger.error("ошибка удаления рецепта", exc_info=True)
        return CustomJsonResponse({"message": "ошибка удаления рецепта"}, status=500)
