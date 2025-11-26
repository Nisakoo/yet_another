import logging

from django.db import models
    

logger = logging.getLogger(__name__)


class QuestionsLikes(models.Model):
    is_like = models.BooleanField()

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["profile", "question"]


class AnswersLikes(models.Model):
    is_like = models.BooleanField()

    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["profile", "answer"]
