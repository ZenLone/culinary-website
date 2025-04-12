from django.contrib import admin
from django.urls import path, include
from recipes.views import recipes_api, recipe_id
from authentication.views import login_api ,validate_token, registration, user_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data', recipes_api, name='recipes_api'),
    path('api/data/<str:id>/', recipe_id, name='recipe_detail'),
    path('api/login/', login_api, name='login_api'),
    path('api/validate-token/', validate_token),
    path('api/user-data/',user_data, name='user-data'),
    path('api/register/' , registration, name='reg'),
]