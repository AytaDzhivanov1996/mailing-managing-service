from django.core.management import BaseCommand

from coursach.send_mail import client_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        client_mailing()
