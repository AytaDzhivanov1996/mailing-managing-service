import datetime

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from base.services import count_mailing_all, count_mailing_active, count_unique_clients
from coursach.forms import ClientForm, MailingForm, LetterForm
from coursach.models import MailingTry, Client, Mailing, Letter
from blog.models import Article


def stats(request):
    context = {
        'object_list': MailingTry.objects.all()
    }
    return render(request, 'coursach/stats.html', context)


class HomePageView(TemplateView):
    template_name = 'coursach/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = Article.objects.all().order_by('?')[:3]
        context_data['count_mailing_all'] = count_mailing_all()
        context_data['count_mailing_active'] = count_mailing_active()
        context_data['count_unique_clients'] = count_unique_clients()
        return context_data


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(created_user=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('coursach:client_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('coursach:client_list')

    def get_queryset(self):
        return Client.objects.filter(created_user=self.request.user)


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('coursach:client_list')

    def get_queryset(self):
        return Client.objects.filter(created_user=self.request.user)


class ClientDetailView(DetailView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(user_create=self.request.user)


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('coursach.view_mailing'):
            return queryset

        return queryset.filter(created_user=self.request.user)


class MailingCreateView(CreateView):
    model = Mailing
    fields = '__all__'
    success_url = reverse_lazy('coursach:mailing')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('coursach:mailing')

    def get_queryset(self):
        return Mailing.objects.filter(created_user=self.request.user)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('coursach:mailing')

    def get_queryset(self):
        return Mailing.objects.filter(created_user=self.request.user)


class MailingDetailView(DetailView):
    model = Mailing

    def get_queryset(self):
        return Mailing.objects.filter(created_user=self.request.user)


class LetterListView(ListView):
    model = Letter

    def get_queryset(self):
        return Letter.objects.filter(created_user=self.request.user)


class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('coursach:letter')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.created_user = self.request.user
            self.object.save()
        return super().form_valid(form)


class LetterUpdateView(UpdateView):
    model = Letter
    form_class = LetterForm
    success_url = reverse_lazy('coursach:letter')

    def get_queryset(self):
        return Letter.objects.filter(created_user=self.request.user)


class LetterDeleteView(DeleteView):
    model = Letter
    success_url = reverse_lazy('coursach:letter')

    def get_queryset(self):
        return Letter.objects.filter(created_user=self.request.user)


class LetterDetailView(DetailView):
    model = Letter

    def get_queryset(self):
        return Letter.objects.filter(created_user=self.request.user)


def client_mailing(request):
    mailing_items = Mailing.objects.all()
    for item in mailing_items:
        if (
                item.mailing_status == Mailing.STATUS_CREATED or item.mailing_status == Mailing.STATUS_LAUNCHED) and item.start_date == datetime.date.today() and item.end_date >= datetime.date.today() and item.time_of_mailing >= datetime.datetime.now().time():
            item.mailing_status = Mailing.STATUS_LAUNCHED
            item.save()
            try:
                result = send_mail(
                    subject=item.message.letter_topic,
                    message=item.message.letter_body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[item.client.email],
                    fail_silently=False
                )

                if result:
                    item.mailing_status = Mailing.STATUS_COMPLETED
                    item.save()
                MailingTry.objects.create(
                    status=item.mailing_status,
                    answer=200
                )
            except Exception as e:
                MailingTry.objects.create(
                    status=item.mailing_status,
                    answer=e
                )
    return redirect(reverse('coursach:mailing'))


@permission_required('coursach.turn_off')
def turn_off_mailing(request, pk):
    current_mailing = get_object_or_404(Mailing, pk=pk)
    if current_mailing:
        current_mailing.state_mail = Mailing.STATUS_DEACTIVATED
        current_mailing.save()
    return redirect(request.META.get('HTTP_REFERER'))


def mail_customer_confirm(request):
    id = request.user.id
    client_mailing(id)
    return redirect(reverse('coursach:mailing'))
