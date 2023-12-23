from django.db import models



class Recipe(models.Model):
   recipe_name = models.CharField(max_length=255)
   ingredients = models.TextField()
   cooking_time = models.IntegerField()
   difficulty_rating = models.CharField(max_length=50)
   description_details = models.TextField()
   image = models.ImageField(upload_to='recipe_images/', default='No_image_available.jpg')

   def __str__(self):
      return self.recipe_name
   
   def calculate_difficulty(self):
      if self.cooking_time < 10 and len(self.ingredients.split(',')) < 5:
         self.difficulty_rating = 'Easy'
      elif self.cooking_time < 10 and len(self.ingredients.split(',')) >= 5:
         self.difficulty_rating = 'Medium'
      elif self.cooking_time >= 10 and len(self.ingredients.split(',')) < 5:
         self.difficulty_rating = 'Intermediate'
      else:
         self.difficulty_rating = 'Hard'

   def save(self, *args, **kwargs):
      self.calculate_difficulty()
      super().save(*args, **kwargs)
