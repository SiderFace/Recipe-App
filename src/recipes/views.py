from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from .models import Recipe
from .forms import RecipeSearchForm

from django.http import JsonResponse
import pandas as pd
from django.core.serializers import serialize

import matplotlib.pyplot as plt
from io import BytesIO
import base64 
import matplotlib
matplotlib.use('agg')



def welcome(request):
   recipes = Recipe.objects.all() 
   return render(request, 'recipes/recipes_home.html', {'recipes': recipes}) 

@login_required
def recipe_detail(request, recipe_id):
   if request.user.is_authenticated:
      recipe = get_object_or_404(Recipe, pk=recipe_id)
      return render(request, 'recipes/recipe_details.html', {'recipe': recipe})
   else:
      # Redirect to login page for non-authenticated users
      return redirect('recipes:user_login')

def user_login(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user:
         login(request, user)
         return redirect('recipes:recipe_list') 
      else:
         messages.error(request, "Invalid username or password. Please try again.")
   return render(request, 'recipes/user_login.html')

def user_logout(request):
   logout(request)
   messages.success(request, "You've successfully logged out.")
   return render(
      request, 
      'recipes/success.html', 
      {'message': "You've successfully logged out."})

def recipe_search(request):
   form = RecipeSearchForm(request.GET)
   recipes = Recipe.objects.all()

   if form.is_valid():
      ingredients = form.cleaned_data.get('ingredients')
      if ingredients:
         recipes = recipes.filter(
            Q(ingredients__icontains=ingredients)
         )

   bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64 = generate_charts_data(recipes)

   return render(
      request, 
      'recipes/search_results.html', 
      {
         'search_results': recipes, 
         'form': form,
         'bar_chart_img': bar_chart_img_base64,
         'pie_chart_img': pie_chart_img_base64,
         'line_chart_img': line_chart_img_base64,
      }
   )


def generate_charts_data(recipes):
    # Create a DataFrame from the recipes
    data = {
        'Recipe Name': [recipe.recipe_name for recipe in recipes],
        'Cooking Time': [recipe.cooking_time for recipe in recipes],
    }
    df = pd.DataFrame(data)

    # Process data and generate charts
    # (You can customize this part based on your specific requirements)
    # For demonstration purposes, let's assume you want to return base64-encoded images
    bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64 = generate_charts(df)

    return bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64

def generate_charts(df):
   plt.switch_backend('agg')

   # Data for data visualization
   recipe_names = df['Recipe Name']
   cooking_times = df['Cooking Time']

   # Bar Chart
   plt.figure(figsize=(10, 6))
   plt.bar(recipe_names, cooking_times, color='blue')
   plt.xlabel('Recipe Names')
   plt.ylabel('Cooking Time (minutes)')
   plt.title('Cooking Time Comparison for Recipes')
   plt.xticks(rotation=45, ha='right')
   bar_chart_img = BytesIO()
   plt.savefig(bar_chart_img, format='png')
   plt.close()

   # Pie Chart
   plt.figure(figsize=(8, 8))
   plt.pie(cooking_times, labels=recipe_names, autopct='%1.1f%%', startangle=140)
   plt.axis('equal')
   plt.title('Percentage of Cooking Time for Each Recipe')
   pie_chart_img = BytesIO()
   plt.savefig(pie_chart_img, format='png')
   plt.close()

   # Line Chart
   plt.figure(figsize=(10, 6))
   plt.plot(recipe_names, cooking_times, marker='o', color='green', linestyle='-', linewidth=2, markersize=8)
   plt.xlabel('Recipe Names')
   plt.ylabel('Cooking Time (minutes)')
   plt.title('Trends in Cooking Time Across Recipes')
   plt.xticks(rotation=45, ha='right')
   line_chart_img = BytesIO()
   plt.savefig(line_chart_img, format='png')
   plt.close()

   # Convert images to base64
   bar_chart_img_base64 = base64.b64encode(bar_chart_img.getvalue()).decode('utf-8')
   pie_chart_img_base64 = base64.b64encode(pie_chart_img.getvalue()).decode('utf-8')
   line_chart_img_base64 = base64.b64encode(line_chart_img.getvalue()).decode('utf-8')

   return bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64


@login_required
def recipe_list(request):
   if request.user.is_authenticated:
      form = RecipeSearchForm(request.GET)
      recipes = Recipe.objects.all()

      if form.is_valid():
         search_query = form.cleaned_data.get('ingredients')
         show_all = form.cleaned_data.get('show_all')

         if show_all:
               recipes = Recipe.objects.all()
         elif search_query:
               recipes = Recipe.objects.filter(
                  Q(ingredients__icontains=search_query) | Q(recipe_name__icontains=search_query)
               )

         # Generate charts data
         bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64 = generate_charts_data(recipes)

         # Render the entire HTML including both recipe list, search results, and charts
         return render(
               request,
               'recipes/recipe_list.html',
               {
                  'recipes': recipes,
                  'bar_chart_img': bar_chart_img_base64,
                  'pie_chart_img': pie_chart_img_base64,
                  'line_chart_img': line_chart_img_base64,
                  'form': form,
               }
         )

      # If the form is not valid, show all recipes and charts
      bar_chart_img_base64, pie_chart_img_base64, line_chart_img_base64 = generate_charts_data(recipes)

      return render(
         request,
         'recipes/recipe_list.html',
         {
               'recipes': recipes,
               'bar_chart_img': bar_chart_img_base64,
               'pie_chart_img': pie_chart_img_base64,
               'line_chart_img': line_chart_img_base64,
               'form': form,
         }
      )
   else:
      # Redirect to login page for non-authenticated users
      return redirect('recipes:user_login')