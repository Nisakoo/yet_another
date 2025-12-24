from django.core.management.base import BaseCommand, CommandError

from django.db import transaction
from django.db.models import F

from app.models import (
    Question, Answer
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            Question.objects.with_rating().update(
                rating_cache=F("rating")
            )

            Question.objects.with_answers_count().update(
                answer_count_cache=F("answers_count")
            )

            Answer.objects.with_rating().update(
                rating_cache=F("rating")
            )