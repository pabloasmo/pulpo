from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

import os
from dotenv import load_dotenv
load_dotenv()

class Command(BaseCommand):
    help = 'Custom mail test'
    source_mail = os.getenv("EMAIL_HOST_USER")

    def add_arguments(self, parser):
        parser.add_argument('-a', type=str, help='Asunto del correo', required=True)
        parser.add_argument('-u', type=str, help='Nombre de usuario', required=True)
        parser.add_argument('-m', type=str, help='Mensaje del correo', required=True)
        parser.add_argument('-d', type=str, help='Destinatario del correo', required=True)

    def handle(self, *args, **kwargs):
        try:
            send_mail(subject=kwargs['a'], message=kwargs['m'], from_email=self.source_mail, recipient_list=[kwargs['d']], fail_silently=False)
        except Exception as e:
            raise CommandError(f"Error sending custom mail: {e}")
