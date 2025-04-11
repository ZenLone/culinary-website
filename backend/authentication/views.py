from django.shortcuts import render
from db_config import profiles
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
import logging
from django.contrib.auth.models import User
import jwt
from datetime import datetime, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)

def recipes_api(request):
    if profiles is None:
        logger.error("Ошибка подключение к Бд")
        return JsonResponse({"Ошбика подключения к БД"}, status=503, ensure_ascii=False)
    if request.method == 'GET':
        return user_login_GET(request)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
def user_login_GET(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    mail = request.Get.get("mail")
    user = authenticate(username=username, password=password, mail=mail)
    if user is not None:
        login(request, user)
        # Generate JWT token
        expiration_time = datetime.utcnow() + timedelta(hours=1)
        payload = {
            'user_id': user.id,
            'exp': expiration_time
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({"message": "Login successful", "token": jwt_token}, status=200)
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=401)