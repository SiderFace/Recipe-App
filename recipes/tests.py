from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe
from .forms import RecipeSearchForm
from django.contrib.auth.models import User



class RecipeModelTest(TestCase):
   def test_recipe_creation(self):
      recipe = Recipe.objects.create(
         recipe_name='Spaghetti Bolognese',
         ingredients='ingredient1, ingredient2, ingredient3, ingredient4',
         cooking_time=5,
         difficulty_rating='Easy',
         description_details='...'
      )
      self.assertEqual(recipe.recipe_name, 'Spaghetti Bolognese')
      self.assertEqual(recipe.ingredients, 'ingredient1, ingredient2, ingredient3, ingredient4')
      self.assertEqual(recipe.cooking_time, 5)
      self.assertEqual(recipe.difficulty_rating, 'Easy')
      self.assertEqual(Recipe.objects.count(), 1)

   def test_calculate_difficulty_easy(self):
      recipe = Recipe.objects.create(
         recipe_name='Easy Recipe',
         ingredients='Ingredient 1, Ingredient 2',
         cooking_time=5,
         description_details='Test Description'
      )
      self.assertEqual(recipe.difficulty_rating, 'Easy')

   def test_calculate_difficulty_medium(self):
      recipe = Recipe.objects.create(
         recipe_name='Medium Recipe',
         ingredients='Ingredient 1, Ingredient 2, Ingredient 3, Ingredient 4, Ingredient 5',
         cooking_time=5,
         description_details='Test Description'
      )
      self.assertEqual(recipe.difficulty_rating, 'Medium')

   def test_calculate_difficulty_intermediate(self):
      recipe = Recipe.objects.create(
         recipe_name='Intermediate Recipe',
         ingredients='Ingredient 1, Ingredient 2',
         cooking_time=15,
         description_details='Test Description'
      )
      self.assertEqual(recipe.difficulty_rating, 'Intermediate')

   def test_calculate_difficulty_hard(self):
      recipe = Recipe.objects.create(
         recipe_name='Hard Recipe',
         ingredients='Ingredient 1, Ingredient 2, Ingredient 3, Ingredient 4, Ingredient 5',
         cooking_time=15,
         description_details='Test Description'
      )
      self.assertEqual(recipe.difficulty_rating, 'Hard')


class RecipeViewTests(TestCase):
   def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user(username='testuser', password='testpassword')
      self.recipe = Recipe.objects.create(
         recipe_name="Test Recipe",
         ingredients="Ingredient 1, Ingredient 2",
         cooking_time=8,
         difficulty_rating="Easy",
         description_details="Test Description",
      )

   def test_welcome_view(self):
      response = self.client.get(reverse('recipes:welcome'))
      self.assertEqual(response.status_code, 200)

   def test_recipe_list_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)

   def test_recipe_detail_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)


class RecipeFormTest(TestCase):
   def setUp(self):
      self.user = User.objects.create_user(username='testuser', password='testpassword')
      self.recipe = Recipe.objects.create(
         recipe_name="Test Recipe",
         ingredients="Ingredient 1, Ingredient 2",
         cooking_time=8,
         difficulty_rating="Easy",
         description_details="Test Description",
      )

   def test_recipe_search_form(self):
      form_data = {'ingredients': 'Test Ingredient', 'show_all': False}
      form = RecipeSearchForm(data=form_data)
      self.assertTrue(form.is_valid())

   def test_welcome_view(self):
      response = self.client.get(reverse('recipes:welcome'))
      self.assertEqual(response.status_code, 200)

   def test_recipe_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)

   def test_recipe_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)