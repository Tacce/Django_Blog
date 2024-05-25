from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    email = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

