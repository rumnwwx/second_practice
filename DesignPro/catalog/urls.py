from django.urls import path
from .views import index, custom_logout, UserProfileListView, user_agree
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('catalog/', index, name='index'),
    path('catalog/register/', views.Register.as_view(), name='register'),
    path('catalog/register/agreement/', views.user_agree, name='agreement'),
    path('catalog/login/', views.Login.as_view(), name='login'),
    path('catalog/logout/', custom_logout, name='logout'),
    path('catalog/profile/', UserProfileListView.as_view(), name='profile'),
]