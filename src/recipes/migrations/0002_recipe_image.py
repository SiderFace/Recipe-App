# Generated by Django 4.2.8 on 2023-12-15 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='No_image_available.jpg', upload_to='recipe_images/'),
        ),
    ]
