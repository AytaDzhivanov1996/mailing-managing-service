from coursach.models import Client, Mailing


def count_mailing_all(*args, **kwargs):
    return Mailing.objects.all().count()


def count_mailing_active(*args, **kwargs):
    return Mailing.objects.filter(mailing_status='created').count()


def count_unique_clients(*args, **kwargs):
    return Client.objects.all().count()
