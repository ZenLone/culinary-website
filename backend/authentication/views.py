from django.shortcuts import render
from backend import settings
from db_config import profiles
from django.http import HttpResponse, JsonResponse
import logging
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
import json

logger = logging.getLogger(__name__)

@csrf_exempt
def login_api(request):
    """
    API для входа пользователя.
    Обрабатывает POST запросы с username, email и password.
    """
    if profiles is None:
        logger.error("Ошибка подключения к БД")
        return JsonResponse({"error": "Ошибка подключения к БД"}, status=503, ensure_ascii=False)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('mail')
            password = data.get('password')
            print(username, email, password)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат запроса"}, status=400)
        if not username or not email or not password:
            return JsonResponse(
                {"error": "Необходимо передать username, email и password"},
                status=400
            )
        user = autificate_user(username, password, email)
        if user:
            # Генерация JWT
            expiration_time = datetime.utcnow() + timedelta(hours=1)
            payload = {
                'user_id': str(user['_id']),
                'exp': expiration_time
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return JsonResponse(
                {"message": "Вход успешно выполнен", "token": jwt_token},
                status=200
            )
        else:
            return JsonResponse({"error": "Неверный username или password или email"}, status=401)
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)

@csrf_exempt
def autificate_user(username, password, email):
    user = profiles.find_one({"username": username})
    if not user:
        return None

    # Проверка email
    if email != user.get('mail'):
        return None

    # Проверка password
    if not check_password(password, user.get('password')):
        return None

    return user

@csrf_exempt
def token_required(view_func):
    """
    Декоратор для проверки JWT токена в заголовке Authorization.
    """
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Ошибка авторизации"}, status=401)
        token = auth_header.split(' ')[1]  # Извлекаем токен после "Bearer "
        try:
            # Декодируем токен
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']  # Добавляем user_id в объект запроса
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Токен истек"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Неверный токен"}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper

@csrf_exempt
def validate_token(token):
    """
    Функция для проверки валидности JWT токена.
    Возвращает True, если токен валиден, и False в противном случае.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return JsonResponse({"valid": True, "payload": payload})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"valid": False, "error": "Токен истек"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"valid": False, "error": "Неверный токен"}, status=401)