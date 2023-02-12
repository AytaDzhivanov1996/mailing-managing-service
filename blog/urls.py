from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', ArticleListView.as_view(), name='blog_list'),
    path('read/<int:pk>/', ArticleDetailView.as_view(), name='blog_read'),
]
