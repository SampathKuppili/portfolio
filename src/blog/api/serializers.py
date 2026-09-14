"""Blog API serializers."""

from rest_framework import serializers

from blog.models import BlogPost, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogPostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'category', 'tags', 'published_at', 'reading_time',
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'category', 'tags', 'published_at', 'reading_time', 'views_count',
        ]
