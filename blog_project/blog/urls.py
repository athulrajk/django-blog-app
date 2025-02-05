from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.blog_list, name='blog_list'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('post/new/', views.blog_create, name='blog_create'),
    path('post/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('post/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]
