"""Portfolio service functions — keeps views thin."""

from .models import (
    Certification,
    Education,
    Experience,
    Profile,
    Project,
    SkillCategory,
)


def get_active_profile():
    """Return the active profile with prefetched social links, or None."""
    return (
        Profile.objects
        .filter(is_active=True)
        .prefetch_related('social_links')
        .first()
    )


def get_skills_by_category():
    """Return active skill categories with their active skills."""
    return (
        SkillCategory.objects
        .filter(is_active=True)
        .prefetch_related('skills')
    )


def get_experiences():
    """Return all experiences ordered with prefetched bullet points."""
    return (
        Experience.objects
        .prefetch_related('points')
        .all()
    )


def get_education():
    """Return all education entries."""
    return Education.objects.all()


def get_certifications():
    """Return all certifications."""
    return Certification.objects.all()


def get_featured_projects():
    """Return featured, active projects with technologies."""
    return (
        Project.objects
        .filter(is_featured=True, is_active=True)
        .prefetch_related('technologies')
    )


def get_all_projects():
    """Return all active projects with technologies."""
    return (
        Project.objects
        .filter(is_active=True)
        .prefetch_related('technologies')
    )


def get_project_by_slug(slug):
    """Return a single project by slug with images and technologies."""
    return (
        Project.objects
        .filter(slug=slug, is_active=True)
        .prefetch_related('technologies', 'images')
        .first()
    )
