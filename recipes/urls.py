from django.urls import path
from .views import welcome, recipe_list, recipe_detail, user_login, user_logout, recipe_search, add_recipe



app_name = 'recipes'

urlpatterns = [
   path('', welcome, name='welcome'),
   path('recipes/', recipe_list, name='recipe_list'),
   path('recipes/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
   path('login/', user_login, name='user_login'),
   path('logout/', user_logout, name='user_logout'),
   path('recipes/search/', recipe_search, name='recipe_search'),
   path('recipes/add/', add_recipe, name='add_recipe'),
]
