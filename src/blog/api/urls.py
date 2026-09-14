"""Blog API URL configuration."""

from django.urls import path

from . import views

app_name = 'blog_api'

urlpatterns = [
    path('', views.BlogPostListAPIView.as_view(), name='post_list'),
    path('<slug:slug>/', views.BlogPostDetailAPIView.as_view(), name='post_detail'),
]
