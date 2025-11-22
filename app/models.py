from django.contrib.auth.models import User
from django.db import models
    

class ProfileQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(
            rating=models.Count("question")
        )
    
    def get_best_members(self, limit=5):
        return self.with_rating().order_by("-rating")[:limit]


class Profile(models.Model):
    objects = ProfileQuerySet.as_manager()

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to="uploads", blank=True)

    def __repr__(self):
        return self.user.username
    

class TagQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(
            rating=models.Count("question")
        )
    
    def get_best_tags(self, limit=5):
        return self.with_rating().order_by("-rating")[:limit]


class Tag(models.Model):
    objects = TagQuerySet.as_manager()

    name = models.CharField(max_length=50, unique=True)

    def __repr__(self):
        return self.name


class QuestionQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(
            total=models.Count("questionslikes"),
            likes=models.Count("questionslikes", filter=models.Q(questionslikes__is_like=True))
        ).annotate(
            rating=2 * models.F("likes") - models.F("total")
        )
    
    def get_by_tags(self, tags):
        return self.filter(tags__name__in=tags)
    
    def get_hottest(self):
        return self.with_rating().order_by("-rating")

    def get_newest(self):
        return self.order_by("-created_at").with_rating()


class Question(models.Model):
    objects = QuestionQuerySet.as_manager()

    title = models.CharField(max_length=255)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, blank=True)

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __repr__(self):
        return self.title


class AnswerQuerySet(models.QuerySet):
    def with_rating(self):
        return self.annotate(
            total=models.Count("answerslikes"),
            likes=models.Count("answerslikes", filter=models.Q(answerslikes__is_like=True))
        ).annotate(
            rating=2 * models.F("likes") - models.F("total")
        )


class Answer(models.Model):
    objects = AnswerQuerySet.as_manager()

    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __repr__(self):
        return self.text[:50]


class QuestionsLikes(models.Model):
    is_like = models.BooleanField()

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    class Meta:
        unique_together = ["profile", "question"]


class AnswersLikes(models.Model):
    is_like = models.BooleanField()

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)

    class Meta:
        unique_together = ["profile", "answer"]