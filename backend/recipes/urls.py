from django.contrib import admin
from django.urls import path
from .views import recipes_api

urlpatterns = [
    path('', recipes_api, name='test'),
]