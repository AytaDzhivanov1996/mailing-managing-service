from django import forms

from blog.models import Article


class BlogListForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_user']
