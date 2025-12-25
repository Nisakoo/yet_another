import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F

from app.models import Answer, Question, QuestionsLikes

from app.tasks import publish_new_answer


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Answer)
def update_answer_count(sender, instance, created, **kwargs):
    if created:
        Question.objects.filter(pk=instance.question.id).update(
            answer_count_cache=F("answer_count_cache") + 1
        )

        channel = f'answers:question_{instance.question_id}'
        
        data = {
            'type': 'new_answer',
            'answer_id': instance.id,
            'text': instance.text,
            'author': instance.profile.user.username,
            'created_at': instance.created_at.isoformat()
        }
        
        publish_new_answer(channel, data)


@receiver(post_save, sender=QuestionsLikes)
def update_question_rating_set_like(sender, instance, created, **kwargs):
    logger.debug("Hello")
    if created:
        Question.objects.filter(pk=instance.question.id).update(
            rating_cache=F("rating_cache") + (1 if instance.is_like else -1)
        )
    else:
        # +-2 появляется из учета того, что если стоял дизлайн
        # то сначала он снимается, то есть +1 к рейтингу
        # а потом ставится лайк, то есть еще раз +1 к рейтингу
        Question.objects.filter(pk=instance.question.id).update(
            rating_cache=F("rating_cache") + (2 if instance.is_like else -2)
        )


@receiver(post_delete, sender=QuestionsLikes)
def update_question_rating_unset_like(sender, instance, **kwargs):
    Question.objects.filter(pk=instance.question.id).update(
        rating_cache=F("rating_cache") + (-1 if instance.is_like else 1)
    )