"""Django sitemap classes for SEO."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost
from portfolio.models import Project


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'portfolio:home',
            'portfolio:about',
            'portfolio:skills',
            'portfolio:experience',
            'portfolio:education',
            'portfolio:certifications',
            'portfolio:project_list',
            'blog:post_list',
            'contact:contact',
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('portfolio:project_detail', kwargs={'slug': obj.slug})


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:post_detail', kwargs={'slug': obj.slug})


sitemaps = {
    'static': StaticSitemap,
    'projects': ProjectSitemap,
    'blog': BlogPostSitemap,
}
