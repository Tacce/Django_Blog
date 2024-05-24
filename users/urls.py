from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile_view, name='profile'),
]
