from django.shortcuts import render
from backend import settings
from db_config import profiles
from django.http import HttpResponse, JsonResponse
import logging
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
import json
from bson import ObjectId

logger = logging.getLogger(__name__)

@csrf_exempt
def login_api(request):
    if profiles is None:
        logger.error("Ошибка подключения к БД")
        return JsonResponse({"error": "Ошибка подключения к БД"}, status=503)
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
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "Отсутствует заголовок авторизации или неверный формат"}, status=401)

        token = auth_header.split(' ')[1]  # Извлекаем токен после "Bearer "
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')  # Получаем user_id из payload
            if not user_id:
                return JsonResponse({"error": "Неверный токен: отсутствует user_id"}, status=401)
            request.user_id = user_id  # Добавляем user_id в объект запроса
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Токен истек"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Неверный токен"}, status=401)
        except Exception as e:
            logger.exception("Ошибка при декодировании токена")
            return JsonResponse({"error": "Ошибка при обработке токена"}, status=400)

        return view_func(request, *args, **kwargs)

    return wrapper

@csrf_exempt
def validate_token(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
    except json.JSONDecodeError:
        return JsonResponse({"valid": False, "error": "Неверный формат запроса"}, status=400)

    if not token:
        return JsonResponse({"valid": False, "error": "Токен не предоставлен"}, status=400)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return JsonResponse({"valid": True, "payload": payload})
    except jwt.ExpiredSignatureError:
        return JsonResponse({"valid": False, "error": "Токен истек"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"valid": False, "error": "Неверный токен"}, status=401)
    
@csrf_exempt
def registration(request):
    if profiles is None:
        logger.error("Ошибка подключения к БД")
        return JsonResponse({"error": "Ошибка подключения к БД"}, status=503)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('mail')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат запроса"}, status=400)

        if not username or not password or not email:
            return JsonResponse(
                {"error": "Необходимо передать username, password и email"},
                status=400
            )

        # Проверка, существует ли пользователь с таким username или email
        if profiles.find_one({"$or": [{"username": username}, {"mail": email}]}):
            return JsonResponse(
                {"error": "Пользователь с таким username или email уже существует"},
                status=409
            )

        # Хеширование пароля
        hashed_password = make_password(password)

        # Создание нового пользователя
        new_user = {
            "username": username,
            "password": hashed_password,
            "mail": email
        }

        # Вставка пользователя в БД
        user_id = profiles.insert_one(new_user).inserted_id

        # Генераци JWT
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'user_id': str(user_id),
            'exp': expiration_time
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return JsonResponse(
            {"message": "Регистрация успешно выполнена", "token": jwt_token},
            status=201
        )
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)
    
@csrf_exempt
@token_required
def user_data(request):
    try:
        user_id = request.user_id
        user = profiles.find_one({"_id": ObjectId(user_id)})
        if user:
            user_data = {
                "username": user.get("username"),
                "mail": user.get("mail")
            }
            return JsonResponse(user_data, status=200)
        else:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)
    except Exception as e:
        logger.exception("Ошибка при получении данных пользователя")
        return JsonResponse({"error": "Ошибка сервера"}, status=500)