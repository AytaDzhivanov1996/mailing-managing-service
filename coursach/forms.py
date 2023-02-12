from django import forms

from base.forms import StyleFormMixin
from coursach.models import Client, Mailing, Letter


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['created_user', ]


class MailingForm(StyleFormMixin, forms.ModelForm):
    STATUSES = (
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена'),
    )
    mailing_status = forms.ChoiceField(choices=STATUSES, )

    class Meta:
        model = Mailing
        exclude = ['created_user', ]


class LetterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Letter
        exclude = ['created_user']
