from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe
import json


@csrf_exempt
def get_recipes(request):
    """
    Simple view to test GET request.
    Returns a text response.
    """
    if request.method == 'GET':
        # In the future, this will fetch recipes from the database
        # For now, just return a simple text response for testing
        return HttpResponse("GET request to get_recipes worked successfully!")
    else:
        # Handle other methods (POST, PUT, etc.) if needed
        return HttpResponse(status=405)  # Method Not Allowed


@csrf_exempt
def recipesApi(request):
    if request.method == 'GET':
        recipes = Recipe.get_all_recipes()
        for recipe in recipes:
            if '_id' in recipe:
                recipe['_id'] = str(recipe['_id'])
        return JsonResponse(recipes, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process the data (implementation depends on your model)
            return JsonResponse({"message": "Data received successfully", "received_data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
