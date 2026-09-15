import json
import os
import sys
import django
from pathlib import Path
from django.conf import settings
from django.db.models import Avg, Count, Sum
from django.shortcuts import render
from django.views import View
from dashboard.views.auth import StaffRequiredMixin
from portfolio.models import Project, Skill, SkillCategory, Certification, Experience
from blog.models import BlogPost
from contact.models import ContactMessage
from django.contrib.auth.models import User


class AnalyticsDashboardView(StaffRequiredMixin, View):
    """Deep-dive analytics dashboard with interactive Chart.js visualizations."""
    template_name = 'dashboard/analytics/index.html'

    def get(self, request):
        # 1. Project Type Distribution
        project_types = Project.objects.values('project_type').annotate(count=Count('id'))
        type_labels_map = {
            'company': 'Company Projects',
            'personal': 'Personal Projects',
            'wordpress': 'WordPress Sites'
        }
        p_labels = [type_labels_map.get(pt['project_type'], pt['project_type']) for pt in project_types]
        p_values = [pt['count'] for pt in project_types]

        # 2. Skills Distribution & Average Proficiency by Category
        skills_by_cat = (
            SkillCategory.objects
            .annotate(
                skill_count=Count('skills'),
                avg_proficiency=Avg('skills__proficiency')
            )
            .filter(skill_count__gt=0)
            .order_by('order')
        )
        cat_labels = [c.name for c in skills_by_cat]
        cat_counts = [c.skill_count for c in skills_by_cat]
        cat_avg_prof = [round(c.avg_proficiency or 0, 1) for c in skills_by_cat]

        # 3. Blog Views & Publication Stats
        total_posts = BlogPost.objects.count()
        published_posts = BlogPost.objects.filter(is_published=True).count()
        draft_posts = total_posts - published_posts
        total_views = BlogPost.objects.aggregate(total=Sum('views_count'))['total'] or 0

        posts_by_views = BlogPost.objects.all().order_by('-views_count')[:5]
        post_titles = [p.title[:25] + ('...' if len(p.title) > 25 else '') for p in posts_by_views]
        post_views = [p.views_count for p in posts_by_views]

        # 4. Contact Inquiries Stats
        total_inquiries = ContactMessage.objects.count()
        read_inquiries = ContactMessage.objects.filter(is_read=True).count()
        unread_inquiries = ContactMessage.objects.filter(is_read=False).count()

        # Group inquiries by date (last 7 days or recent months)
        from django.db.models.functions import TruncDate
        inquiries_by_date = (
            ContactMessage.objects
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')[:10]
        )
        inquiry_dates = [i['date'].strftime('%b %d') for i in inquiries_by_date] if inquiries_by_date else ['Recent']
        inquiry_counts = [i['count'] for i in inquiries_by_date] if inquiries_by_date else [total_inquiries]

        # 5. System & Database Health
        db_path = settings.DATABASES['default']['NAME']
        try:
            db_size_kb = round(os.path.getsize(db_path) / 1024, 1)
        except Exception:
            db_size_kb = 0

        system_info = {
            'python_version': sys.version.split()[0],
            'django_version': django.__version__,
            'debug_mode': settings.DEBUG,
            'db_size_kb': db_size_kb,
            'user_count': User.objects.count(),
            'server_tz': str(settings.TIME_ZONE),
        }

        context = {
            # Data metrics
            'total_projects': Project.objects.count(),
            'total_skills': Skill.objects.count(),
            'total_certs': Certification.objects.count(),
            'total_experience': Experience.objects.count(),
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_views': total_views,
            'total_inquiries': total_inquiries,
            'read_inquiries': read_inquiries,
            'unread_inquiries': unread_inquiries,
            'system_info': system_info,

            # Charts JSON
            'project_chart_labels': json.dumps(p_labels),
            'project_chart_values': json.dumps(p_values),
            'cat_labels': json.dumps(cat_labels),
            'cat_counts': json.dumps(cat_counts),
            'cat_avg_prof': json.dumps(cat_avg_prof),
            'post_titles': json.dumps(post_titles),
            'post_views': json.dumps(post_views),
            'inquiry_dates': json.dumps(inquiry_dates),
            'inquiry_counts': json.dumps(inquiry_counts),
            'active_nav': 'analytics',
        }
        return render(request, self.template_name, context)
