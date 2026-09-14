"""Contact API URL configuration."""

from django.urls import path

from . import views

app_name = 'contact_api'

urlpatterns = [
    path('', views.ContactMessageCreateAPIView.as_view(), name='contact_create'),
]
