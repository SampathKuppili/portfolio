from django.db import models
from django.utils.text import slugify


class Profile(models.Model):
    """Main portfolio profile — typically one active profile."""

    name = models.CharField(max_length=100)
    designation = models.CharField(
        max_length=200,
        help_text="e.g. Senior Python/Django Developer",
    )
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
    )
    short_bio = models.TextField(
        max_length=500,
        help_text="Brief introduction shown in the hero section.",
    )
    about = models.TextField(
        help_text="Detailed about section content.",
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=150, blank=True)
    resume = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True,
        help_text="Upload your resume/CV (PDF recommended).",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Show 'Available for hire' badge.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only one active profile should exist.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """Social media links associated with a profile."""

    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('stackoverflow', 'Stack Overflow'),
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter / X'),
        ('other', 'Other'),
    ]

    PLATFORM_ICONS = {
        'github': 'fa-brands fa-github',
        'linkedin': 'fa-brands fa-linkedin',
        'stackoverflow': 'fa-brands fa-stack-overflow',
        'youtube': 'fa-brands fa-youtube',
        'instagram': 'fa-brands fa-instagram',
        'twitter': 'fa-brands fa-x-twitter',
        'other': 'fa-solid fa-link',
    }

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='social_links',
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'platform']
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'platform'],
                name='unique_profile_platform',
                violation_error_message="This platform is already linked to this profile.",
            ),
        ]

    @property
    def icon_class(self):
        return self.PLATFORM_ICONS.get(self.platform, 'fa-solid fa-link')

    def __str__(self):
        return f"{self.profile.name} — {self.get_platform_display()}"


class SkillCategory(models.Model):
    """Grouping for skills (e.g. Backend, Frontend, DevOps)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual technical skill with proficiency level."""

    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
    )
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        default=50,
        help_text="Proficiency level (1–100).",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Experience(models.Model):
    """Professional work experience entry."""

    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,
        help_text="Brief overview of the role.",
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    @property
    def duration(self):
        end = self.end_date or __import__('datetime').date.today()
        months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
        years, remaining_months = divmod(months, 12)
        parts = []
        if years:
            parts.append(f"{years} yr{'s' if years > 1 else ''}")
        if remaining_months:
            parts.append(f"{remaining_months} mo{'s' if remaining_months > 1 else ''}")
        return ' '.join(parts) or 'Less than a month'

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class ExperiencePoint(models.Model):
    """Bullet-point responsibility under an experience."""

    experience = models.ForeignKey(
        Experience,
        on_delete=models.CASCADE,
        related_name='points',
    )
    description = models.CharField(max_length=500)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Experience Point'
        verbose_name_plural = 'Experience Points'

    def __str__(self):
        return self.description[:80]


class Education(models.Model):
    """Education / academic qualification."""

    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_year']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Certification(models.Model):
    """Professional certification or credential."""

    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    credential_id = models.CharField(max_length=200, blank=True)
    credential_url = models.URLField(blank=True)
    certificate_image = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'

    def __str__(self):
        return f"{self.name} — {self.issuing_organization}"


class Technology(models.Model):
    """Reusable technology tag (used across projects)."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional CSS icon class (e.g. fa-brands fa-python).",
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Technology'
        verbose_name_plural = 'Technologies'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio project showcase."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(
        max_length=300,
        help_text="Brief summary shown on project cards.",
    )
    description = models.TextField(
        help_text="Full project description.",
    )
    thumbnail = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
    )
    technologies = models.ManyToManyField(
        Technology,
        blank=True,
        related_name='projects',
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Screenshot / gallery image for a project."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return f"{self.project.title} — Image {self.order}"
