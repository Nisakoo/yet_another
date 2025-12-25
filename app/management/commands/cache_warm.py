from django.core.management.base import BaseCommand

from django.core.cache import cache

from app.models import (
    Profile, Tag
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        best_members = [
            profile.user.username
            for profile in Profile.objects.get_best_members()
        ]

        # TODO: пересчитывать каждые пять минут
        cache.set("best-members", best_members, timeout=20)

        best_tags = [
            {"name": tag.name, "url": tag.url}
            for tag in Tag.objects.get_best_tags()
        ]

        # TODO: пересчитывать каждые пять минут
        cache.set("best-tags", best_tags, timeout=20)