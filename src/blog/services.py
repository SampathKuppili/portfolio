"""Blog service functions."""

from django.db.models import Q

from .models import BlogPost, Category, Tag


def get_published_posts():
    """Return published blog posts with related objects."""
    return (
        BlogPost.objects
        .filter(is_published=True)
        .select_related('category', 'author')
        .prefetch_related('tags')
    )


def get_post_by_slug(slug):
    """Return a single published post by slug."""
    return (
        BlogPost.objects
        .filter(slug=slug, is_published=True)
        .select_related('category', 'author')
        .prefetch_related('tags')
        .first()
    )


def get_posts_by_category(category_slug):
    """Return published posts filtered by category slug."""
    return get_published_posts().filter(category__slug=category_slug)


def get_posts_by_tag(tag_slug):
    """Return published posts filtered by tag slug."""
    return get_published_posts().filter(tags__slug=tag_slug).distinct()


def get_related_posts(post, limit=3):
    """Return related posts by same category or shared tags."""
    related = (
        BlogPost.objects
        .filter(is_published=True)
        .exclude(pk=post.pk)
    )
    # Try same category first
    if post.category:
        by_category = related.filter(category=post.category)[:limit]
        if by_category.exists():
            return by_category
    # Fallback to shared tags
    tag_ids = post.tags.values_list('id', flat=True)
    if tag_ids:
        return related.filter(tags__in=tag_ids).distinct()[:limit]
    # Fallback to latest
    return related[:limit]


def search_posts(query):
    """Search published posts by title, excerpt, and content."""
    if not query or not query.strip():
        return BlogPost.objects.none()
    return (
        get_published_posts()
        .filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )
        .distinct()
    )


def get_active_categories():
    """Return categories that have at least one published post."""
    return (
        Category.objects
        .filter(is_active=True, posts__is_published=True)
        .distinct()
    )


def get_all_tags():
    """Return tags that are used in at least one published post."""
    return Tag.objects.filter(posts__is_published=True).distinct()
