from django import forms
from .models import Blog, Post, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type here...'}),
        }
        labels = {
            'content': '',
        }
