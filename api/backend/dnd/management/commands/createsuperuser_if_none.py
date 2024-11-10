from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser if one does not already exist'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.environ['DJANGO_SUPERUSER_USERNAME'],
                email=os.environ['DJANGO_SUPERUSER_EMAIL'],
                password=os.environ['DJANGO_SUPERUSER_PASSWORD']
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
