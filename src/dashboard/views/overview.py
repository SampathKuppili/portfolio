import json
from django.shortcuts import render
from django.views import View
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from dashboard.views.auth import StaffRequiredMixin
from portfolio.models import Project, Skill, Certification, Experience, Education
from blog.models import BlogPost
from contact.models import ContactMessage


class OverviewDashboardView(StaffRequiredMixin, View):
    """Main dashboard overview page showing KPI metrics, charts, and recent activity."""
    template_name = 'dashboard/overview.html'

    def get(self, request):
        # Key KPI counts
        total_projects = Project.objects.count()
        featured_projects = Project.objects.filter(is_featured=True).count()
        total_skills = Skill.objects.count()
        total_certs = Certification.objects.count()
        total_experience = Experience.objects.count()
        total_education = Education.objects.count()

        total_posts = BlogPost.objects.count()
        published_posts = BlogPost.objects.filter(is_published=True).count()
        total_views = BlogPost.objects.aggregate(total_views=Sum('views_count'))['total_views'] or 0

        total_contacts = ContactMessage.objects.count()
        unread_contacts = ContactMessage.objects.filter(is_read=False).count()
        total_users = User.objects.count()
        staff_users = User.objects.filter(is_staff=True).count()

        # Recent activities
        recent_contacts = ContactMessage.objects.all().order_by('-created_at')[:5]
        recent_projects = Project.objects.all().order_by('-created_at')[:4]
        recent_posts = BlogPost.objects.all().order_by('-created_at')[:4]

        # Chart Data: Project types
        project_types = Project.objects.values('project_type').annotate(count=Count('id'))
        type_labels_map = {'company': 'Company Projects', 'personal': 'Personal Projects', 'wordpress': 'WordPress Sites'}
        project_chart_labels = [type_labels_map.get(pt['project_type'], pt['project_type']) for pt in project_types]
        project_chart_values = [pt['count'] for pt in project_types]

        # Chart Data: Skills by Category
        skills_by_cat = Skill.objects.values('category__name').annotate(count=Count('id')).order_by('-count')[:6]
        skill_chart_labels = [s['category__name'] or 'Uncategorized' for s in skills_by_cat]
        skill_chart_values = [s['count'] for s in skills_by_cat]

        context = {
            'total_projects': total_projects,
            'featured_projects': featured_projects,
            'total_skills': total_skills,
            'total_certs': total_certs,
            'total_experience': total_experience,
            'total_education': total_education,
            'total_posts': total_posts,
            'published_posts': published_posts,
            'total_views': total_views,
            'total_contacts': total_contacts,
            'unread_contacts': unread_contacts,
            'total_users': total_users,
            'staff_users': staff_users,
            'recent_contacts': recent_contacts,
            'recent_projects': recent_projects,
            'recent_posts': recent_posts,
            # JSON-safe chart data
            'project_chart_labels': json.dumps(project_chart_labels),
            'project_chart_values': json.dumps(project_chart_values),
            'skill_chart_labels': json.dumps(skill_chart_labels),
            'skill_chart_values': json.dumps(skill_chart_values),
            'active_nav': 'overview',
        }
        return render(request, self.template_name, context)
