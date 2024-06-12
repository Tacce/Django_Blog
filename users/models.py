from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')
    email = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)

            width, height = img.size
            if width > height:
                left = (width - height) / 2
                upper = 0
                right = (width + height) / 2
                lower = height
            else:
                left = 0
                upper = (height - width) / 2
                right = width
                lower = (height + width) / 2

            img = img.crop((left, upper, right, lower))
            img.save(self.profile_image.path)

    def remove_profile_image(self):
        if self.profile_image and self.profile_image.url != 'default.png':
            self.profile_image.delete(save=False)
        self.profile_image = 'default.png'
        self.save()
