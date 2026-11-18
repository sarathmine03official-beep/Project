
import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    help = "Create Render admin account"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = os.environ.get(
            "DJANGO_SUPERUSER_USERNAME"
        )
        email = os.environ.get(
            "DJANGO_SUPERUSER_EMAIL", ""
        )
        password = os.environ.get(
            "DJANGO_SUPERUSER_PASSWORD"
        )

        if not username or not password:
            raise Exception(
                "Admin environment variables are missing"
            )

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Render admin account created/updated successfully"
            )
        )
