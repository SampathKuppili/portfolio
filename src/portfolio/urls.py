from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    path('education/', views.EducationView.as_view(), name='education'),
    path('certifications/', views.CertificationsView.as_view(), name='certifications'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('resume/', views.resume_download, name='resume_download'),
]
