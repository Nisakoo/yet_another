import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from app.models import Answer, AnswersLikes


logger = logging.getLogger(__name__)


@receiver(post_save, sender=AnswersLikes)
def update_question_rating_set_like(sender, instance, created, **kwargs):
    logger.debug("Hello")
    if created:
        Answer.objects.filter(pk=instance.answer.id).update(
            rating_cache=F("rating_cache") + (1 if instance.is_like else -1)
        )
    else:
        # +-2 появляется из учета того, что если стоял дизлайн
        # то сначала он снимается, то есть +1 к рейтингу
        # а потом ставится лайк, то есть еще раз +1 к рейтингу
        Answer.objects.filter(pk=instance.answer.id).update(
            rating_cache=F("rating_cache") + (2 if instance.is_like else -2)
        )


@receiver(post_delete, sender=AnswersLikes)
def update_question_rating_unset_like(sender, instance, **kwargs):
    Answer.objects.filter(pk=instance.answer.id).update(
        rating_cache=F("rating_cache") + (-1 if instance.is_like else 1)
    )