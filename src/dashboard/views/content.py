from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from dashboard.forms import (
    ProjectForm, BlogPostForm, SkillForm, CertificationForm,
    ExperienceForm, EducationForm
)
from dashboard.views.auth import StaffRequiredMixin
from portfolio.models import Project, Skill, Certification, Experience, Education
from blog.models import BlogPost


class ContentHubView(StaffRequiredMixin, View):
    """Central index for all managed portfolio content."""
    template_name = 'dashboard/content/index.html'

    def get(self, request):
        context = {
            'projects_count': Project.objects.count(),
            'skills_count': Skill.objects.count(),
            'posts_count': BlogPost.objects.count(),
            'certs_count': Certification.objects.count(),
            'exp_count': Experience.objects.count(),
            'edu_count': Education.objects.count(),
            'active_nav': 'content',
        }
        return render(request, self.template_name, context)


# ============================================================================
# Projects CRUD
# ============================================================================

class ProjectListView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/projects_list.html'

    def get(self, request):
        projects = Project.objects.all().order_by('order', '-created_at')
        q = request.GET.get('q', '').strip()
        ptype = request.GET.get('type', '')

        if q:
            projects = projects.filter(Q(title__icontains=q) | Q(short_description__icontains=q))
        if ptype:
            projects = projects.filter(project_type=ptype)

        paginator = Paginator(projects, 10)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'projects': page_obj,
            'page_obj': page_obj,
            'search_query': q,
            'current_type': ptype,
            'active_nav': 'content_projects',
        })


class ProjectCreateView(StaffRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/content/project_form.html'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, f"Project '{form.cleaned_data['title']}' created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add New Project'
        ctx['active_nav'] = 'content_projects'
        return ctx


class ProjectUpdateView(StaffRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/content/project_form.html'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, f"Project '{self.object.title}' updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Project: {self.object.title}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_projects'
        return ctx


class ProjectDeleteView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/confirm_delete.html'

    def get(self, request, pk):
        item = get_object_or_404(Project, pk=pk)
        return render(request, self.template_name, {
            'item': item,
            'item_type': 'Project',
            'cancel_url': reverse_lazy('dashboard:project_list'),
            'active_nav': 'content_projects',
        })

    def post(self, request, pk):
        item = get_object_or_404(Project, pk=pk)
        title = item.title
        item.delete()
        messages.success(request, f"Project '{title}' was deleted.")
        return redirect('dashboard:project_list')


# ============================================================================
# Blog Posts CRUD
# ============================================================================

class BlogListView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/blog_list.html'

    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        q = request.GET.get('q', '').strip()
        status = request.GET.get('status', '')

        if q:
            posts = posts.filter(Q(title__icontains=q) | Q(excerpt__icontains=q))
        if status == 'published':
            posts = posts.filter(is_published=True)
        elif status == 'draft':
            posts = posts.filter(is_published=False)

        paginator = Paginator(posts, 10)
        page_obj = paginator.get_page(request.GET.get('page'))

        return render(request, self.template_name, {
            'posts': page_obj,
            'page_obj': page_obj,
            'search_query': q,
            'current_status': status,
            'active_nav': 'content_blog',
        })


class BlogCreateView(StaffRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/content/blog_form.html'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f"Article '{form.cleaned_data['title']}' created successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Write New Article'
        ctx['active_nav'] = 'content_blog'
        return ctx


class BlogUpdateView(StaffRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'dashboard/content/blog_form.html'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        messages.success(self.request, f"Article '{self.object.title}' updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Article: {self.object.title}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_blog'
        return ctx


class BlogDeleteView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/confirm_delete.html'

    def get(self, request, pk):
        item = get_object_or_404(BlogPost, pk=pk)
        return render(request, self.template_name, {
            'item': item,
            'item_type': 'Blog Post',
            'cancel_url': reverse_lazy('dashboard:blog_list'),
            'active_nav': 'content_blog',
        })

    def post(self, request, pk):
        item = get_object_or_404(BlogPost, pk=pk)
        title = item.title
        item.delete()
        messages.success(request, f"Article '{title}' was deleted.")
        return redirect('dashboard:blog_list')


# ============================================================================
# Skills CRUD
# ============================================================================

class SkillListView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/skills_list.html'

    def get(self, request):
        skills = Skill.objects.select_related('category').all().order_by('category__order', 'order', 'name')
        q = request.GET.get('q', '').strip()
        cat = request.GET.get('category', '')

        if q:
            skills = skills.filter(name__icontains=q)
        if cat:
            skills = skills.filter(category_id=cat)

        from portfolio.models import SkillCategory
        categories = SkillCategory.objects.all()

        return render(request, self.template_name, {
            'skills': skills,
            'categories': categories,
            'search_query': q,
            'current_cat': cat,
            'active_nav': 'content_skills',
        })


class SkillCreateView(StaffRequiredMixin, CreateView):
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/content/skill_form.html'
    success_url = reverse_lazy('dashboard:skill_list')

    def form_valid(self, form):
        messages.success(self.request, f"Skill '{form.cleaned_data['name']}' added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add New Skill'
        ctx['active_nav'] = 'content_skills'
        return ctx


class SkillUpdateView(StaffRequiredMixin, UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'dashboard/content/skill_form.html'
    success_url = reverse_lazy('dashboard:skill_list')

    def form_valid(self, form):
        messages.success(self.request, f"Skill '{self.object.name}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Skill: {self.object.name}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_skills'
        return ctx


class SkillDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        skill = get_object_or_404(Skill, pk=pk)
        name = skill.name
        skill.delete()
        messages.success(request, f"Skill '{name}' deleted.")
        return redirect('dashboard:skill_list')


# ============================================================================
# Certifications CRUD
# ============================================================================

class CertListView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/certs_list.html'

    def get(self, request):
        certs = Certification.objects.all().order_by('-issue_date')
        return render(request, self.template_name, {
            'certs': certs,
            'active_nav': 'content_certs',
        })


class CertCreateView(StaffRequiredMixin, CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/content/cert_form.html'
    success_url = reverse_lazy('dashboard:cert_list')

    def form_valid(self, form):
        messages.success(self.request, f"Certification '{form.cleaned_data['name']}' saved.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add New Certification'
        ctx['active_nav'] = 'content_certs'
        return ctx


class CertUpdateView(StaffRequiredMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'dashboard/content/cert_form.html'
    success_url = reverse_lazy('dashboard:cert_list')

    def form_valid(self, form):
        messages.success(self.request, f"Certification '{self.object.name}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Certification: {self.object.name}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_certs'
        return ctx


class CertDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        cert = get_object_or_404(Certification, pk=pk)
        name = cert.name
        cert.delete()
        messages.success(request, f"Certification '{name}' deleted.")
        return redirect('dashboard:cert_list')


# ============================================================================
# Experience & Education CRUD
# ============================================================================

class ExperienceListView(StaffRequiredMixin, View):
    template_name = 'dashboard/content/experience_list.html'

    def get(self, request):
        experiences = Experience.objects.all().order_by('order', '-start_date')
        educations = Education.objects.all().order_by('order', '-start_year')
        return render(request, self.template_name, {
            'experiences': experiences,
            'educations': educations,
            'active_nav': 'content_experience',
        })


class ExperienceCreateView(StaffRequiredMixin, CreateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'dashboard/content/experience_form.html'
    success_url = reverse_lazy('dashboard:experience_list')

    def form_valid(self, form):
        messages.success(self.request, f"Experience at '{form.cleaned_data['company_name']}' added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add Work Experience'
        ctx['active_nav'] = 'content_experience'
        return ctx


class ExperienceUpdateView(StaffRequiredMixin, UpdateView):
    model = Experience
    form_class = ExperienceForm
    template_name = 'dashboard/content/experience_form.html'
    success_url = reverse_lazy('dashboard:experience_list')

    def form_valid(self, form):
        messages.success(self.request, f"Experience '{self.object.job_title}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Experience: {self.object.company_name}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_experience'
        return ctx


class ExperienceDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        exp = get_object_or_404(Experience, pk=pk)
        name = exp.company_name
        exp.delete()
        messages.success(request, f"Experience at '{name}' deleted.")
        return redirect('dashboard:experience_list')


class EducationCreateView(StaffRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'dashboard/content/education_form.html'
    success_url = reverse_lazy('dashboard:experience_list')

    def form_valid(self, form):
        messages.success(self.request, f"Education entry for '{form.cleaned_data['institution']}' added.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = 'Add Education Qualification'
        ctx['active_nav'] = 'content_experience'
        return ctx


class EducationUpdateView(StaffRequiredMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'dashboard/content/education_form.html'
    success_url = reverse_lazy('dashboard:experience_list')

    def form_valid(self, form):
        messages.success(self.request, f"Education '{self.object.degree}' updated.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action_title'] = f"Edit Education: {self.object.institution}"
        ctx['is_edit'] = True
        ctx['active_nav'] = 'content_experience'
        return ctx


class EducationDeleteView(StaffRequiredMixin, View):
    def post(self, request, pk):
        edu = get_object_or_404(Education, pk=pk)
        name = edu.institution
        edu.delete()
        messages.success(request, f"Education at '{name}' deleted.")
        return redirect('dashboard:experience_list')
