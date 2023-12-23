from django import forms

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
