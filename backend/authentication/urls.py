from django.contrib import admin
from django.urls import path, include
from .views import user_login_GET

urlpatterns = [
    path('api/login/', user_login_GET)
]