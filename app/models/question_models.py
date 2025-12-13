import logging

from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef, Count, IntegerField
from django.db import models
from django.urls import reverse

from .likes_models import AnswersLikes, QuestionsLikes
    

logger = logging.getLogger(__name__)


class AnswerQuerySet(models.QuerySet):
    @staticmethod
    def _get_likes_sq():
        return AnswersLikes.objects.filter(
            answer=OuterRef("pk"),
            is_like=True
        ).values("answer").annotate(cnt=Count("id")).values("cnt")
    
    @staticmethod
    def _get_total_likes_sq():
        return AnswersLikes.objects.filter(
            answer=OuterRef("pk")
        ).values("answer").annotate(cnt=Count("id")).values("cnt")

    def with_rating(self):
        return self.alias(
            _likes=Coalesce(Subquery(self._get_likes_sq(), output_field=IntegerField()), 0),
            _total=Coalesce(Subquery(self._get_total_likes_sq(), output_field=IntegerField()), 0),
        ).annotate(
            rating=2 * models.F("_likes") - models.F("_total")
        )
    
    def with_related(self):
        return self.select_related("profile")


class Answer(models.Model):
    objects = AnswerQuerySet.as_manager()

    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")
    profile = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)

    rating_cache = models.IntegerField(default=0)

    def __str__(self):
        return self.text[:50]


class QuestionQuerySet(models.QuerySet):
    @staticmethod
    def _get_likes_sq():
        return QuestionsLikes.objects.filter(
            question=OuterRef("pk"),
            is_like=True
        ).values("question").annotate(cnt=Count("id")).values("cnt")
    
    @staticmethod
    def _get_total_likes_sq():
        return QuestionsLikes.objects.filter(
            question=OuterRef("pk")
        ).values("question").annotate(cnt=Count("id")).values("cnt")
    
    @staticmethod
    def _get_answers_sq():
        return Answer.objects.filter(
            question=OuterRef("pk")
        ).values("question").annotate(cnt=Count("id")).values("cnt")
    
    def with_related(self):
        return self.select_related("profile") \
                    .prefetch_related("tags") \

    def with_rating(self):
        return self.alias(
            _likes=Coalesce(Subquery(self._get_likes_sq(), output_field=IntegerField()), 0),
            _total=Coalesce(Subquery(self._get_total_likes_sq(), output_field=IntegerField()), 0),
        ).annotate(
            rating=2 * models.F("_likes") - models.F("_total")
        )
    
    def with_answers_count(self):
        return self.annotate(
            answers_count=Coalesce(Subquery(self._get_answers_sq(), output_field=IntegerField()), 0)
        )
    
    def get_by_tags(self, tags):
        return self.with_related() \
                    .filter(tags__name__in=tags)
    
    def get_hottest(self):
        return self.with_related() \
                    .order_by("-rating_cache")

    def get_newest(self):
        return self.with_related() \
                    .order_by("-created_at")


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()

    title = models.CharField(max_length=255)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField("Tag", blank=True)

    profile = models.ForeignKey("Profile", on_delete=models.SET_NULL, null=True)

    rating_cache = models.IntegerField(default=0)
    answer_count_cache = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("question", kwargs={"question_id": self.pk})
    
    @property
    def url(self):
        return self.get_absolute_url()
    

class TagQuerySet(models.QuerySet):
    @staticmethod
    def _get_question_sq():
        return Question.objects.filter(
            profile=OuterRef("pk")
        ).values("profile").annotate(cnt=Count("id")).values("cnt")

    def with_rating(self):
        return self.annotate(
            rating=Coalesce(Subquery(self._get_question_sq(), output_field=IntegerField()), 0)
        )
    
    def get_best_tags(self, limit=5):
        return self.with_rating().order_by("-rating")[:limit]


class Tag(models.Model):
    objects = TagQuerySet.as_manager()

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name