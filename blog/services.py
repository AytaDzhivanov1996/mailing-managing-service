from django.conf import settings
from django.core.cache import cache

from blog.models import Article


def cache_blog(self):
    queryset = Article.objects.all()
    if settings.CACHE_ENABLED:
        key = 'blog'
        cache_data = cache.get(key)

        if cache_data is None:
            cache_data = queryset
            cache.set(key, cache_data)

        return cache_data

    return queryset
