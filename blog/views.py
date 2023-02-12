from django.views.generic import ListView, DetailView

from blog.models import Article
from blog.services import cache_blog


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('blog.set_publish'):
            return queryset

        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = cache_blog(self)
        return context_data


class ArticleDetailView(DetailView):
    model = Article
