"""
URL configuration for limonmental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from limonmentalApp import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('posts/', views.post_list, name='posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/comment/', views.create_comment, name='create_comment'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('psychologists/', views.psychologists, name='psychologists'),
    path('posts/search/', views.post_search, name='post_search'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('paypal/', views.paypal, name='paypal'),
    path('404/', views.error_404, name='error_404'),
    path('create_psychologist/', views.create_psychologist, name='create_psychologist'),
    path('psychologist/<int:pk>/', views.psychologist_detail, name='psychologist_detail'),
    path('delete_psychologist/<int:pk>/', views.delete_psychologist, name='delete_psychologist'),
    #path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    #path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    #path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    #path('blog/', views.blog, name='blog')   
]
