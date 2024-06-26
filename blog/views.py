from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Post, Comment
from .forms import BlogForm, PostForm, CommentForm


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'all_blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            followed_blogs = Blog.objects.filter(followers=self.request.user)
            user_blogs = Blog.objects.filter(author=self.request.user)
        else:
            followed_blogs = []
            user_blogs = []
        context['followed_blogs'] = followed_blogs
        context['user_blogs'] = user_blogs
        return context

    def get_queryset(self):
        return Blog.objects.all()


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.total_likes()
        data['post_is_liked'] = liked
        data['form'] = CommentForm()
        return data


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})


@login_required
def create_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.blog = blog
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'blog': blog})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'form': form, 'post': post})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


@login_required
def follow_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.followers.filter(id=request.user.id).exists():
        blog.followers.remove(request.user)
    else:
        blog.followers.add(request.user)
    return HttpResponseRedirect(reverse('blog_detail', args=[str(pk)]))


@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if blog.author != request.user:
        return HttpResponseForbidden()
    blog.delete()
    return redirect('blog_list')


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden()
    post.delete()
    return redirect('blog_detail', pk=post.blog.pk)


@login_required
def delete_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author != request.user and post.author != request.user:
        return HttpResponseForbidden()
    comment.delete()
    return redirect('post_detail', pk=post_pk)
