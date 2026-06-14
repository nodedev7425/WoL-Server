from django.core.management.base import BaseCommand, CommandError

from core.services import WakeService

class Command(BaseCommand):

    help = "Send Wake-on-LAN magic packet to target network card (MAC)"

    def add_arguments(self, parser):
        parser.add_argument("mac_address", type=str)

    def handle(self, *args, **options):

        mac_address = options['mac_address']

        try:
            WakeService.wake_device(mac_address)
        except ValueError:
            raise CommandError(f"Incorrect MAC address format: '{mac_address}'")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully send magic packet to '{mac_address}'")
        )