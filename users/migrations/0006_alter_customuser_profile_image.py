# Generated by Django 5.0.6 on 2024-05-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='default.png', upload_to='profile_images/'),
        ),
    ]
