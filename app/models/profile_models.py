import logging

from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef, Count, IntegerField
from django.db import models
from django.templatetags.static import static

from .question_models import Question
    

logger = logging.getLogger(__name__)


class ProfileQuerySet(models.QuerySet):
    @staticmethod
    def _get_question_sq():
        return Question.objects.filter(
            profile=OuterRef("pk")
        ).values("profile").annotate(cnt=Count("id")).values("cnt")

    def with_rating(self):
        return self.annotate(
            rating=Coalesce(Subquery(self._get_question_sq(), output_field=IntegerField()), 0)
        )
    
    def get_best_members(self, limit=5):
        return self.select_related("user") \
                    .only("user__username") \
                    .with_rating() \
                    .order_by("-rating")[:limit]


class Profile(models.Model):
    objects = ProfileQuerySet.as_manager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=25)
    avatar = models.ImageField(upload_to="uploads", blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, "url"):
            return self.avatar.url
        
        return static("images/image.png")

    def __str__(self):
        return self.user.username