from django.db import models
from django.contrib.auth.models import User

class Artwork(models.Model):
    file_path = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    target_player = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    target_player = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        target = "All" if self.is_global else self.target_player.username
        return f"Message to {target}: {self.content[:50]}"
