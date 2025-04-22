from io import BytesIO
from tkinter import Image
from django.shortcuts import render
from backend import settings
from db_config import profiles , fs
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import logging
import jwt
from PIL import Image as PILImage
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.http import require_http_methods
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
        registrationDate = datetime.utcnow()

        # Создание нового пользователя
        new_user = {
        "username": username,
        "password": hashed_password,
        "mail": email,
        "registrationDate": datetime.utcnow(),
        "role": "user",
        "image_id": None
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
        # Извлечение user_id из токена
        user_id = request.user_id

        # Преобразование user_id в ObjectId
        try:
            user_id = ObjectId(user_id)
        except Exception:
            return JsonResponse({"error": "Неверный формат user_id"}, status=400)

        # Поиск пользователя по ID
        user = profiles.find_one({"_id": user_id})
        if not user:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)

        # Формирование данных пользователя
        user_data = {
            "username": user.get("username"),
            "mail": user.get("mail"),
            "registrationDate": user.get("registrationDate"),
            "_id": str(user.get("_id")),
            "role": "user",
            "image_id": str(user.get("image_id")) if user.get("image_id") else None
        }

        # Обработка GET-запросов
        if request.method == 'GET':
            return JsonResponse(user_data, status=200)
        else:
            return JsonResponse({"error": "Метод не разрешен"}, status=405)

    except Exception as e:
        logger.exception("Ошибка при получении данных пользователя")
        return JsonResponse({"error": "Ошибка сервера"}, status=500)
@csrf_exempt
def upload_photo(request, id):
    if request.method == "POST":
        try:
            # Проверка наличия файла в запросе
            if "image" not in request.FILES:
                logger.error("Файл не найден в запросе")
                return JsonResponse({"error": "Файл не найден в запросе"}, status=400)

            file = request.FILES["image"]
            logger.info(f"Получен файл: {file.name}, размер: {file.size} байт")

            # Открытие изображения с помощью Pillow
            try:
                img = PILImage.open(file)  # Явное использование PILImage
            except Exception as e:
                logger.error(f"Ошибка при открытии изображения: {str(e)}")
                return JsonResponse({"error": f"Ошибка при открытии изображения: {str(e)}"}, status=500)

            max_size = (500, 500)  # Максимальный размер изображения
            img.thumbnail(max_size)

            # Сохранение измененного изображения во временный буфер
            buffer = BytesIO()
            try:
                img.save(buffer, format=img.format)
            except Exception as e:
                logger.error(f"Ошибка при сохранении изображения: {str(e)}")
                return JsonResponse({"error": f"Ошибка при сохранении изображения: {str(e)}"}, status=500)

            buffer.seek(0)

            # Загрузка файла в GridFS
            try:
                file_id = fs.put(
                    buffer,
                    user_id=id,
                    filename=file.name,
                    content_type=file.content_type
                )
            except Exception as e:
                logger.error(f"Ошибка при загрузке файла в GridFS: {str(e)}")
                return JsonResponse({"error": f"Ошибка при загрузке файла в GridFS: {str(e)}"}, status=500)

            # Обновление поля image_id в профиле пользователя
            try:
                profiles.update_one(
                    {"_id": ObjectId(id)},
                    {"$set": {"image_id": str(file_id)}}
                )
            except Exception as e:
                logger.error(f"Ошибка при обновлении профиля пользователя: {str(e)}")
                return JsonResponse({"error": f"Ошибка при обновлении профиля пользователя: {str(e)}"}, status=500)

            return JsonResponse({
                "message": "Файл успешно загружен",
                "file_id": str(file_id),
            }, status=200)

        except Exception as e:
            logger.error(f"Неожиданная ошибка: {str(e)}")
            return JsonResponse({"error": f"Неожиданная ошибка: {str(e)}"}, status=500)
        
@csrf_exempt
def load_photo(request, id):
    try:
        # Преобразование строки в ObjectId
        user_oid = ObjectId(id)

        # Поиск пользователя по _id
        user = profiles.find_one({"_id": user_oid})
        if not user:
            return JsonResponse({"error": "Пользователь не найден"}, status=404)

        # Получение image_id из документа пользователя
        image_id = user.get("image_id")
        if not image_id:
            return JsonResponse({"error": "У пользователя нет аватара"}, status=404)

        # Получение файла из GridFS
        image = fs.get(ObjectId(image_id))

        # Отправка файла клиенту
        response = HttpResponse(image.read(), content_type=image.content_type)
        response['Content-Disposition'] = f'inline; filename="{image.filename}"'
        return response

    except Exception as e:
        return JsonResponse({"error": f"Ошибка сервера: {str(e)}"}, status=500)
@csrf_exempt
def get_image(request, image_id):
    try:
        # Преобразование строки в ObjectId
        image_oid = ObjectId(image_id)

        # Проверка наличия файла в GridFS
        if not fs.exists({"_id": image_oid}):
            logger.error(f"Файл с _id {image_oid} не найден в GridFS")
            return HttpResponse("Image not found", status=404)

        # Получение файла из GridFS
        image = fs.get(image_oid)

        # Отправка файла клиенту
        response = HttpResponse(image.read(), content_type=image.content_type)
        response['Content-Disposition'] = f'inline; filename="{image.filename}"'
        return response

    except Exception as e:
        logger.error(f"Ошибка сервера: {str(e)}")
        return HttpResponse("Internal Server Error", status=500)

