from django.http import JsonResponse
from django.shortcuts import render
from .models import Recipe

def get_recipes(request):
    recipes = Recipe.get_all_recipes()
    data = [
        {
            "id": str(recipe.get('_id', '')),
            "title": recipe.get('title', 'Без названия'),
            "ingredients": recipe.get('ingredients', []),
            "instructions": recipe.get('instructions', []),
            "created_at": recipe.get('created_at', '').isoformat() if 'created_at' in recipe else ''
        }
        for recipe in recipes
    ]
    return JsonResponse(data, safe=False)

def recipes(request):
    return render(request, 'recipes/recipes.html')