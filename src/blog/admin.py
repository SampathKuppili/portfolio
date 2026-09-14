from django.contrib import admin

from .models import BlogPost, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'published_at', 'views_count')
    list_filter = ('is_published', 'category', 'tags', 'created_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags'),
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image'),
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at'),
        }),
        ('Stats & Timestamps', {
            'classes': ('collapse',),
            'fields': ('views_count', 'created_at', 'updated_at'),
        }),
    )
