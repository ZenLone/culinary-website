from django.shortcuts import render
from backend import settings
from db_config import profiles
from django.http import HttpResponse, JsonResponse
import logging
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger(__name__)

def login_api(request):
    if profiles is None:
        logger.error("Ошибка подключения к БД")
        return JsonResponse({"error": "Ошибка подключения к БД"}, status=503, ensure_ascii=False)
    if request.method == 'GET':
        return user_login_POST(request)
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)

def user_login_POST(request):
    # Получаем данные из запроса
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Проверяем, что все обязательные поля переданы
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

def autificate_user(username, password, email):
    user = profiles.find_one({"username": username})
    if user and email != user['email']:
        return None
    if user and check_password(password, user['password']):
        return user
    else:
        return None

def token_required(view_func):
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

# @token_required
# def protected_view(request):
#     user_id = request.user_id  # ID пользователя из декодированного токена
#     return JsonResponse(
#         {"message": f"Доступ разрешен для пользователя с ID {user_id}"},
#         status=200,
#         ensure_ascii=False
#     )

def validate_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidTokenError:
        return False, None