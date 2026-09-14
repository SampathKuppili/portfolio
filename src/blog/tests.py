"""Tests for blog models and views."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import BlogPost, Category, Tag

User = get_user_model()


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.category = Category.objects.create(name='Django', slug='django')
        cls.tag = Tag.objects.create(name='python', slug='python')
        cls.post = BlogPost.objects.create(
            title='Test Post', slug='test-post',
            excerpt='A test excerpt.', content='Full content here.',
            author=cls.user, category=cls.category,
            is_published=True, published_at=timezone.now(),
        )
        cls.post.tags.add(cls.tag)

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Django')

    def test_category_auto_slug(self):
        cat = Category.objects.create(name='API Dev')
        self.assertEqual(cat.slug, 'api-dev')

    def test_tag_str(self):
        self.assertEqual(str(self.tag), 'python')

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_reading_time(self):
        self.assertGreaterEqual(self.post.reading_time, 1)

    def test_post_auto_publish_date(self):
        post = BlogPost.objects.create(
            title='Auto Date', slug='auto-date',
            excerpt='Test', content='Content',
            author=self.user, is_published=True,
        )
        self.assertIsNotNone(post.published_at)

    def test_post_tags_relationship(self):
        self.assertEqual(self.post.tags.count(), 1)
        self.assertIn(self.tag, self.post.tags.all())


class BlogViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.category = Category.objects.create(name='Django', slug='django', is_active=True)
        cls.tag = Tag.objects.create(name='python', slug='python')
        cls.post = BlogPost.objects.create(
            title='Test Post', slug='test-post',
            excerpt='A test excerpt.', content='Full content for search.',
            author=cls.user, category=cls.category,
            is_published=True, published_at=timezone.now(),
        )
        cls.post.tags.add(cls.tag)

    def setUp(self):
        self.client = Client()

    def test_blog_list(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_detail(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_blog_category(self):
        response = self.client.get(reverse('blog:category', kwargs={'slug': 'django'}))
        self.assertEqual(response.status_code, 200)

    def test_blog_tag(self):
        response = self.client.get(reverse('blog:tag', kwargs={'slug': 'python'}))
        self.assertEqual(response.status_code, 200)

    def test_blog_search(self):
        response = self.client.get(reverse('blog:search') + '?q=content')
        self.assertEqual(response.status_code, 200)

    def test_blog_search_empty(self):
        response = self.client.get(reverse('blog:search') + '?q=nonexistent12345')
        self.assertEqual(response.status_code, 200)

    def test_unpublished_post_404(self):
        BlogPost.objects.create(
            title='Draft', slug='draft-post',
            excerpt='Draft', content='Draft content',
            author=self.user, is_published=False,
        )
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'draft-post'}))
        self.assertEqual(response.status_code, 404)
