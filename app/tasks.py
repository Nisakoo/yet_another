from celery import shared_task

import requests

from django.db import transaction
from django.db.models import F

from django.core.cache import cache

from django.conf import settings

from app.models import (
    Question, Answer, Tag, Profile
)

from app.search_index import SearchIndex


@shared_task
def update_ratings_and_answers_count():
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

@shared_task
def update_best_tags():
    best_tags = [
        {"name": tag.name, "url": tag.url}
        for tag in Tag.objects.get_best_tags()
    ]

    # TODO: пересчитывать каждые пять минут
    cache.set("best-tags", best_tags, timeout=20)


@shared_task
def update_best_members():
    best_members = [
        profile.user.username
        for profile in Profile.objects.get_best_members()
    ]

    # TODO: пересчитывать каждые пять минут
    cache.set("best-members", best_members, timeout=20)

@shared_task
def update_search_index():
    index = SearchIndex()
    index.build_index(Question.objects.all(), fields=["title", "text"])


@shared_task
def publish_new_answer(channel, data):
    url = f'{settings.CENTRIFUGO_HOST}/api'
    
    payload = {
        'method': 'publish',
        'params': {
            'channel': channel,
            'data': data
        }
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'apikey {settings.CENTRIFUGO_API_KEY}'
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f'Error publishing to Centrifugo: {e}')
        return False