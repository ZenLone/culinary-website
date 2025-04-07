from django.contrib import admin
from django.urls import path, include
from recipes.views import recipes_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/data', recipes_api, name='recipes_api'),
]


