from django.contrib import admin
from django.urls import path
from .views import get_recipes

urlpatterns = [
    path('', get_recipes, name='test'),
]