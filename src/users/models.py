from django.db import models

class User(models.Model):
   user_id = models.AutoField(primary_key=True)
   user_name = models.CharField(max_length=255)
   email_address = models.EmailField(unique=True)

   def __str__(self):
      return self.user_name
   
