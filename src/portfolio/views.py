"""Portfolio views — homepage and portfolio content pages."""

from django.http import FileResponse, Http404
from django.views.generic import DetailView, ListView, TemplateView

from blog.services import get_published_posts
from . import services


class HomeView(TemplateView):
    """Homepage with hero, about, skills, experience, featured projects, and latest posts."""
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = services.get_active_profile()
        context.update({
            'profile': profile,
            'skill_categories': services.get_skills_by_category(),
            'experiences': services.get_experiences()[:3],
            'featured_projects': services.get_featured_projects()[:6],
            'latest_posts': get_published_posts()[:3],
            'certifications': services.get_certifications()[:4],
        })
        return context


class AboutView(TemplateView):
    template_name = 'portfolio/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = services.get_active_profile()
        return context


class SkillsView(TemplateView):
    template_name = 'portfolio/skills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_categories'] = services.get_skills_by_category()
        return context


class ExperienceView(TemplateView):
    template_name = 'portfolio/experience.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = services.get_experiences()
        return context


class EducationView(TemplateView):
    template_name = 'portfolio/education.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['education_list'] = services.get_education()
        return context


class CertificationsView(TemplateView):
    template_name = 'portfolio/certifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['certifications'] = services.get_certifications()
        return context


class ProjectListView(ListView):
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        queryset = services.get_all_projects()
        tech = self.request.GET.get('tech')
        if tech:
            queryset = queryset.filter(technologies__slug=tech).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Technology
        context['technologies'] = Technology.objects.all()
        context['current_tech'] = self.request.GET.get('tech', '')
        return context


class ProjectDetailView(DetailView):
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        from .models import Project
        return (
            Project.objects
            .filter(is_active=True)
            .prefetch_related('technologies', 'images')
        )


def resume_download(request):
    """Serve the resume file from the active profile."""
    profile = services.get_active_profile()
    if not profile or not profile.resume:
        raise Http404("Resume not available.")
    return FileResponse(
        profile.resume.open('rb'),
        as_attachment=True,
        filename='resume.pdf',
    )
