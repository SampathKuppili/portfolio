"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from common.sitemaps import sitemaps

# Customise admin header
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio CMS"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom Admin Dashboard
    path('dashboard/', include('dashboard.urls')),

    # App URLs
    path('', include('portfolio.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),

    # API
    path('api/', include('portfolio.api.urls')),
    path('api/blog/', include('blog.api.urls')),
    path('api/contact/', include('contact.api.urls')),

    # SEO
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),
]

# Error handlers
handler404 = 'common.views.handler404'
handler403 = 'common.views.handler403'
handler500 = 'common.views.handler500'

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
