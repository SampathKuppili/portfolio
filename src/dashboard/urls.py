from django.urls import path
from dashboard.views import auth, overview, users, content, contacts, analytics

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', auth.DashboardLoginView.as_view(), name='login'),
    path('logout/', auth.DashboardLogoutView.as_view(), name='logout'),

    # Overview
    path('', overview.OverviewDashboardView.as_view(), name='overview'),

    # Analytics
    path('analytics/', analytics.AnalyticsDashboardView.as_view(), name='analytics'),

    # User Management
    path('users/', users.UserListView.as_view(), name='user_list'),
    path('users/add/', users.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', users.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', users.UserDeleteView.as_view(), name='user_delete'),

    # Content Hub
    path('content/', content.ContentHubView.as_view(), name='content_hub'),

    # Projects CRUD
    path('content/projects/', content.ProjectListView.as_view(), name='project_list'),
    path('content/projects/add/', content.ProjectCreateView.as_view(), name='project_create'),
    path('content/projects/<int:pk>/edit/', content.ProjectUpdateView.as_view(), name='project_edit'),
    path('content/projects/<int:pk>/delete/', content.ProjectDeleteView.as_view(), name='project_delete'),

    # Blog Posts CRUD
    path('content/blog/', content.BlogListView.as_view(), name='blog_list'),
    path('content/blog/add/', content.BlogCreateView.as_view(), name='blog_create'),
    path('content/blog/<int:pk>/edit/', content.BlogUpdateView.as_view(), name='blog_edit'),
    path('content/blog/<int:pk>/delete/', content.BlogDeleteView.as_view(), name='blog_delete'),

    # Skills CRUD
    path('content/skills/', content.SkillListView.as_view(), name='skill_list'),
    path('content/skills/add/', content.SkillCreateView.as_view(), name='skill_create'),
    path('content/skills/<int:pk>/edit/', content.SkillUpdateView.as_view(), name='skill_edit'),
    path('content/skills/<int:pk>/delete/', content.SkillDeleteView.as_view(), name='skill_delete'),

    # Certifications CRUD
    path('content/certifications/', content.CertListView.as_view(), name='cert_list'),
    path('content/certifications/add/', content.CertCreateView.as_view(), name='cert_create'),
    path('content/certifications/<int:pk>/edit/', content.CertUpdateView.as_view(), name='cert_edit'),
    path('content/certifications/<int:pk>/delete/', content.CertDeleteView.as_view(), name='cert_delete'),

    # Experience & Education CRUD
    path('content/experience/', content.ExperienceListView.as_view(), name='experience_list'),
    path('content/experience/add/', content.ExperienceCreateView.as_view(), name='experience_create'),
    path('content/experience/<int:pk>/edit/', content.ExperienceUpdateView.as_view(), name='experience_edit'),
    path('content/experience/<int:pk>/delete/', content.ExperienceDeleteView.as_view(), name='experience_delete'),
    path('content/education/add/', content.EducationCreateView.as_view(), name='education_create'),
    path('content/education/<int:pk>/edit/', content.EducationUpdateView.as_view(), name='education_edit'),
    path('content/education/<int:pk>/delete/', content.EducationDeleteView.as_view(), name='education_delete'),

    # Contact Submissions
    path('contacts/', contacts.ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:pk>/', contacts.ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/<int:pk>/toggle-read/', contacts.ContactToggleReadView.as_view(), name='contact_toggle_read'),
    path('contacts/<int:pk>/delete/', contacts.ContactDeleteView.as_view(), name='contact_delete'),
]
