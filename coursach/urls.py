from django.urls import path

from coursach.apps import CoursachConfig
from coursach.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, ClientDetailView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, MailingDetailView, LetterListView, \
    LetterCreateView, LetterUpdateView, LetterDeleteView, LetterDetailView, client_mailing, stats

app_name = CoursachConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='coursach'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('detail_client/<int:pk>/', ClientDetailView.as_view(), name='detail_client'),
    path('mailing/', MailingListView.as_view(), name='mailing'),
    path('create_mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('update_mailing/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('detail_mailing/<int:pk>/', MailingDetailView.as_view(), name='detail_mailing'),
    path('letter/', LetterListView.as_view(), name='letter'),
    path('create_letter/', LetterCreateView.as_view(), name='create_letter'),
    path('update_letter/<int:pk>/', LetterUpdateView.as_view(), name='update_letter'),
    path('delete_letter/<int:pk>/', LetterDeleteView.as_view(), name='delete_letter'),
    path('detail_letter/<int:pk>/', LetterDetailView.as_view(), name='detail_letter'),
    path('client_mailing/', client_mailing, name='status'),
    path('stats/', stats, name='stats')
]
