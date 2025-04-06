from django.contrib import admin
from django.urls import path, include
from recipes.views import recipesApi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls')),
    path('api/data', recipesApi, name='recipes_api'),
]


