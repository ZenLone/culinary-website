from django.contrib import admin
from django.urls import path, include
from .views import login_api , protected_view

urlpatterns = [
    # path('api/login/', login_api),
    # path('api/validate-token/', protected_view),
]