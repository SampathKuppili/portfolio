from django.contrib import admin

from .models import (
    Certification,
    Education,
    Experience,
    ExperiencePoint,
    Profile,
    Project,
    ProjectImage,
    Skill,
    SkillCategory,
    SocialLink,
    Technology,
)


# ---------------------------------------------------------------------------
# Inlines
# ---------------------------------------------------------------------------

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('platform', 'url', 'order', 'is_active')


class ExperiencePointInline(admin.TabularInline):
    model = ExperiencePoint
    extra = 2
    fields = ('description', 'order')


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 2
    fields = ('name', 'proficiency', 'order', 'is_active')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'order')


# ---------------------------------------------------------------------------
# Model Admins
# ---------------------------------------------------------------------------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'is_available', 'is_active', 'updated_at')
    list_filter = ('is_active', 'is_available')
    search_fields = ('name', 'designation', 'email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [SocialLinkInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'designation', 'profile_image'),
        }),
        ('Bio', {
            'fields': ('short_bio', 'about'),
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'location'),
        }),
        ('Resume & Status', {
            'fields': ('resume', 'is_available', 'is_active'),
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SkillInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current',)
    search_fields = ('job_title', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ExperiencePointInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'field_of_study', 'start_year', 'end_year', 'order')
    search_fields = ('degree', 'institution', 'field_of_study')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_date', 'credential_id')
    list_filter = ('issuing_organization',)
    search_fields = ('name', 'issuing_organization', 'credential_id')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_class')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'is_active', 'order', 'created_at')
    list_filter = ('is_featured', 'is_active', 'technologies')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('technologies',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProjectImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'short_description', 'description', 'thumbnail'),
        }),
        ('Technologies & Links', {
            'fields': ('technologies', 'github_url', 'live_url'),
        }),
        ('Dates & Status', {
            'fields': ('start_date', 'end_date', 'is_featured', 'is_active', 'order'),
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
