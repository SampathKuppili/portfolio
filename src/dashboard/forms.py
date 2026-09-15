from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from portfolio.models import (
    Project, Skill, SkillCategory, Certification,
    Experience, Education, Profile, SocialLink
)
from blog.models import BlogPost, Category as BlogCategory, Tag
from contact.models import ContactMessage

COMMON_INPUT_CLASSES = (
    "w-full bg-[#0d161a] border border-white/10 rounded-xl px-4 py-2.5 text-white "
    "placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-1 "
    "focus:ring-red-500 text-sm transition-all duration-200"
)

COMMON_SELECT_CLASSES = (
    "w-full bg-[#0d161a] border border-white/10 rounded-xl px-4 py-2.5 text-white "
    "focus:outline-none focus:border-red-500 focus:ring-1 focus:ring-red-500 "
    "text-sm transition-all duration-200"
)

COMMON_CHECKBOX_CLASSES = (
    "rounded border-white/20 bg-[#0d161a] text-red-500 focus:ring-red-500 h-4 w-4"
)

COMMON_TEXTAREA_CLASSES = (
    "w-full bg-[#0d161a] border border-white/10 rounded-xl px-4 py-2.5 text-white "
    "placeholder-gray-500 focus:outline-none focus:border-red-500 focus:ring-1 "
    "focus:ring-red-500 text-sm transition-all duration-200 resize-y"
)


class DashboardLoginForm(forms.Form):
    """Admin login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': COMMON_INPUT_CLASSES,
            'placeholder': 'Enter username or email',
            'autocomplete': 'username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': COMMON_INPUT_CLASSES,
            'placeholder': 'Enter password',
            'autocomplete': 'current-password',
        })
    )


class DashboardUserCreateForm(forms.ModelForm):
    """Form to create a new user from the dashboard."""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': COMMON_INPUT_CLASSES,
            'placeholder': 'Set user password',
        }),
        help_text="Required. Use a secure password."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': COMMON_INPUT_CLASSES,
            'placeholder': 'Confirm user password',
        }),
        help_text="Enter the same password again for verification."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'e.g. john_doe'}),
            'email': forms.EmailInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'john@example.com'}),
            'first_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Doe'}),
            'is_staff': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'is_superuser': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class DashboardUserEditForm(forms.ModelForm):
    """Form to edit an existing user."""
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': COMMON_INPUT_CLASSES,
            'placeholder': 'Leave blank to keep unchanged',
        }),
        help_text="Leave blank if you don't want to change the password."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'email': forms.EmailInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'first_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'last_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'is_staff': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'is_superuser': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class ProjectForm(forms.ModelForm):
    """Form for portfolio projects."""
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'project_type', 'short_description', 'description',
            'thumbnail', 'technologies', 'github_url', 'live_url',
            'start_date', 'end_date', 'is_featured', 'is_active', 'order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Project title'}),
            'slug': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'unique-slug'}),
            'project_type': forms.Select(attrs={'class': COMMON_SELECT_CLASSES}),
            'short_description': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 2, 'placeholder': 'Short summary for cards...'}),
            'description': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 5, 'placeholder': 'Detailed project description...'}),
            'thumbnail': forms.FileInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'technologies': forms.SelectMultiple(attrs={'class': COMMON_SELECT_CLASSES, 'size': 5}),
            'github_url': forms.URLInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'https://github.com/...'}),
            'live_url': forms.URLInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'https://...'}),
            'start_date': forms.DateInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'date'}),
            'is_featured': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'order': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '0'}),
        }


class BlogPostForm(forms.ModelForm):
    """Form for blog posts."""
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'category', 'tags', 'excerpt', 'content',
            'featured_image', 'is_published', 'published_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Article title'}),
            'slug': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'article-slug'}),
            'category': forms.Select(attrs={'class': COMMON_SELECT_CLASSES}),
            'tags': forms.SelectMultiple(attrs={'class': COMMON_SELECT_CLASSES, 'size': 4}),
            'excerpt': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 2, 'placeholder': 'Catchy excerpt...'}),
            'content': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 10, 'placeholder': 'HTML content...'}),
            'featured_image': forms.FileInput(attrs={'class': COMMON_INPUT_CLASSES}),
            'is_published': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'published_at': forms.DateTimeInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'datetime-local'}),
        }


class SkillForm(forms.ModelForm):
    """Form for technical skills."""
    class Meta:
        model = Skill
        fields = ['name', 'category', 'icon_class', 'proficiency', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'e.g. Python, Docker, React'}),
            'category': forms.Select(attrs={'class': COMMON_SELECT_CLASSES}),
            'icon_class': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'e.g. devicon-python-plain or fa-brands fa-react'}),
            'proficiency': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'min': 1, 'max': 100, 'placeholder': '85'}),
            'order': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
        }


class CertificationForm(forms.ModelForm):
    """Form for certifications."""
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'issue_date', 'credential_id', 'credential_url', 'certificate_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Certification title'}),
            'issuing_organization': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'e.g. AWS, Meta, Microsoft'}),
            'issue_date': forms.DateInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'date'}),
            'credential_id': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'ID-12345'}),
            'credential_url': forms.URLInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'https://...'}),
            'certificate_image': forms.FileInput(attrs={'class': COMMON_INPUT_CLASSES}),
        }


class ExperienceForm(forms.ModelForm):
    """Form for professional work experience."""
    class Meta:
        model = Experience
        fields = ['company_name', 'job_title', 'location', 'start_date', 'end_date', 'is_current', 'description', 'order']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Company Name'}),
            'job_title': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Role / Title'}),
            'location': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'City, Remote / On-site'}),
            'start_date': forms.DateInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': COMMON_INPUT_CLASSES, 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': COMMON_CHECKBOX_CLASSES}),
            'description': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 4, 'placeholder': 'Role description and impact...'}),
            'order': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '0'}),
        }


class EducationForm(forms.ModelForm):
    """Form for academic background."""
    class Meta:
        model = Education
        fields = ['degree', 'institution', 'field_of_study', 'start_year', 'end_year', 'description', 'order']
        widgets = {
            'degree': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'e.g. Bachelor of Technology'}),
            'institution': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'University / College Name'}),
            'field_of_study': forms.TextInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': 'Computer Science'}),
            'start_year': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '2019'}),
            'end_year': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '2023'}),
            'description': forms.Textarea(attrs={'class': COMMON_TEXTAREA_CLASSES, 'rows': 3, 'placeholder': 'Key highlights or CGPA...'}),
            'order': forms.NumberInput(attrs={'class': COMMON_INPUT_CLASSES, 'placeholder': '0'}),
        }
