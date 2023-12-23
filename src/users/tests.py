from django.test import TestCase
from .models import User

class UserModelTest(TestCase):

   def test_user_creation(self):
      user = User.objects.create(
         user_name='John Doe',
         email_address='john@example.com',
      )
      self.assertEqual(user.user_name, 'John Doe')
      self.assertEqual(user.email_address, 'john@example.com')
      self.assertEqual(User.objects.count(), 1)

