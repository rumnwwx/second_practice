from django.urls import path
from .views import index, custom_logout, UserProfileListView, DesignRequestCreateView, DesignRequestListView, DesignRequestDelete, ProfileUpdate
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('catalog/', index, name='index'),
    path('catalog/register/', views.Register.as_view(), name='register'),
    path('catalog/register/agreement/', views.user_agree, name='agreement'),
    path('catalog/login/', views.Login.as_view(), name='login'),
    path('catalog/logout/', custom_logout, name='logout'),
    path('catalog/profile/', UserProfileListView.as_view(), name='profile'),
    path('catalog/profile/update', ProfileUpdate.as_view(), name='profile_update'),
    path('catalog/design_request/', DesignRequestCreateView.as_view(), name='design_request'),
    path('catalog/profile/view/', DesignRequestListView.as_view(), name='design_request_view'),
    path('view/<int:pk>/delete/', DesignRequestDelete.as_view(), name='design_request_delete'),
]
