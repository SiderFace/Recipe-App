from django import forms
from .models import Recipe


class RecipeSearchForm(forms.Form):
   ingredients = forms.CharField(
      label='Ingredients',
      required=False
   )
   show_all = forms.BooleanField(
      label='Show All',
      required=False,
      initial=False
   )

class AddRecipeForm(forms.ModelForm):
   class Meta:
      model = Recipe
      fields = ['recipe_name', 'ingredients', 'cooking_time', 'description_details', 'image']