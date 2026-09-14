"""Blog API views."""

from rest_framework import generics
from rest_framework.permissions import AllowAny

from blog import services
from blog.models import BlogPost

from .serializers import BlogPostDetailSerializer, BlogPostListSerializer


class BlogPostListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        return services.get_published_posts()


class BlogPostDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = BlogPostDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True)
            .select_related('category', 'author')
            .prefetch_related('tags')
        )
