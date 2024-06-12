from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from blog.models import Blog
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View

from .forms import CustomUserChangeForm
from .models import CustomUser


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('profile', username=user.username)
        return render(request, 'registration/signup.html', {'form': form})


'''
class CustomLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog_list')
        return render(request, 'users/login.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog_list')
'''


def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    blogs = Blog.objects.filter(author=user)
    context = {
        'user_profile': user,
        'blogs': blogs,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def remove_profile_image(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user.remove_profile_image()
    return redirect('profile', username=user.username)

