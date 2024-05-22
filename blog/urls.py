from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/new/', views.create_blog, name='blog_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('blog/<int:blog_id>/post/new/', views.create_post, name='post_create'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.SignUpView.as_view(), name='signup')
]

