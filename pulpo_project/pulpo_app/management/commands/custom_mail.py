from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, send_mass_mail

class Command(BaseCommand):
    help = 'Custom mail test'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=str, help='Source email address')
        parser.add_argument('--destination', type=str, help='Destination email address')


    def handle(self, *args, **kwargs):
        try:
            correo = (
                "asunto del correo",
                "mensaje del correo",
                kwargs['source'],
                [kwargs['destination']],
            )
            send_mass_mail((correo,), fail_silently=False)
        except Exception as e:
            raise CommandError(f"Error sending custom mail: {e}")
