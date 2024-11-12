from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlayerProfile

@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        PlayerProfile.objects.create(user=instance)