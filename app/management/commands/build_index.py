from django.core.management.base import BaseCommand

from django.core.cache import cache

from app.models import (
    Question
)

from app.search_index import SearchIndex


class Command(BaseCommand):
    def handle(self, *args, **options):
        index = SearchIndex()
        index.build_index(Question.objects.all(), fields=["title", "text"])