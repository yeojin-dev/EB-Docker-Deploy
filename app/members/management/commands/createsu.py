from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from config.settings.production import json_object

User = get_user_model()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('username', nargs=1, type=str)
        # parser.add_argument('password', nargs=1, type=str)
        # parser.add_argument('email', nargs=1, type=str)

    def handle(self, *args, **options):
        if not User.objects.filter(username=json_object['SUPERUSER']['username']).exists():
            User.objects.create_superuser(**json_object['SUPERUSER'])

        self.stdout.write(self.style.SUCCESS('Successfully created superuser "%s"' % json_object['SUPERUSER']['username']))
