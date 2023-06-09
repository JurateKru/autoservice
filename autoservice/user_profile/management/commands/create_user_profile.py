from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from user_profile.models import Profile

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        user_without_profile = User.objects.filter(profile__isnull=True)
        created_profile_count = 0
        try:
            for user in user_without_profile:
                profile = Profile(user=user)
                profile.save()
                created_profile_count += 1
        except Exception as e:
            raise CommandError(e)
        else:
            self.stdout.write(
                self.style.SUCCESS('%d user profiles created' % created_profile_count)
            )