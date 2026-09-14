from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    """Blog post category."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Blog post tag for cross-cutting topics."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Technical blog post."""

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    excerpt = models.TextField(
        max_length=500,
        help_text="Short summary shown on listing pages.",
    )
    content = models.TextField(
        help_text="Full blog post content (HTML).",
    )
    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    views_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_published']),
        ]

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    def __str__(self):
        return self.title
