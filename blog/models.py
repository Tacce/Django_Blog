from django.db import models
from django.utils import timezone
from users.models import CustomUser


# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    followers = models.ManyToManyField(CustomUser, related_name='followed_blogs', blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

