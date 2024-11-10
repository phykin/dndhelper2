from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create dummy users.'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        dummy_users = [
            {
                "username": "Dummy",
                "password": "Dummy"
            }
        ]
        for dummy_user in dummy_users:
            if not User.objects.filter(username=dummy_user["username"]).exists():
                user = User.objects.create(
                    username=dummy_user["username"]
                )
                user.set_password(dummy_user["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Dummy user "{dummy_user["username"]}" created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Dummy user "{dummy_user["username"]}" already exists'))
