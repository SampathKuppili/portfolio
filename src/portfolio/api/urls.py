"""Portfolio API URL configuration."""

from django.urls import path

from . import views

app_name = 'portfolio_api'

urlpatterns = [
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('skills/', views.SkillListAPIView.as_view(), name='skills'),
    path('experience/', views.ExperienceListAPIView.as_view(), name='experience'),
    path('education/', views.EducationListAPIView.as_view(), name='education'),
    path('certifications/', views.CertificationListAPIView.as_view(), name='certifications'),
    path('projects/', views.ProjectListAPIView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailAPIView.as_view(), name='project_detail'),
]
