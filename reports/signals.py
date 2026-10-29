from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Goal

@receiver (post_save, sender=User)
def create_user_goal(sender, instance, created, **kwargs):
    if created:
        Goal.objects.create(user=instance)
