"""Blog views — listing, detail, category, tag, and search."""

from django.views.generic import DetailView, ListView, TemplateView

from . import services
from .models import BlogPost


class BlogListView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return services.get_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = services.get_active_categories()
        context['tags'] = services.get_all_tags()
        return context


class BlogDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            BlogPost.objects
            .filter(is_published=True)
            .select_related('category', 'author')
            .prefetch_related('tags')
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        BlogPost.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = services.get_related_posts(self.object)
        return context


class BlogCategoryView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return services.get_posts_by_category(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Category
        context['current_category'] = Category.objects.filter(slug=self.kwargs['slug']).first()
        context['categories'] = services.get_active_categories()
        context['tags'] = services.get_all_tags()
        return context


class BlogTagView(ListView):
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return services.get_posts_by_tag(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Tag
        context['current_tag'] = Tag.objects.filter(slug=self.kwargs['slug']).first()
        context['categories'] = services.get_active_categories()
        context['tags'] = services.get_all_tags()
        return context


class BlogSearchView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return services.search_posts(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
