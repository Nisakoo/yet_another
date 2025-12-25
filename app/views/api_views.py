import json
from functools import wraps

from django.views import View
from django.core.cache import cache

from app.models import QuestionsLikes, AnswersLikes, Question, Answer, Profile, Tag

from marshmallow import Schema, ValidationError

from .responses.responses import OkResponse, ErrorResponse
from .schemes.schemes import QuestionLikeSchema, AnswerLikeSchema, AnswerCorrectSchema, SearchQuery
from app.search_index import SearchIndex


def json_login_required(func):
    @wraps(func)
    def inner(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(self, request, *args, **kwargs)
        
        return ErrorResponse(status_code=401, message="Unauthorized")
    
    return inner


def validate_data_with(requestSchema: Schema):
    
    def decorator(func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            try:
                data = json.loads(request.body)

                schema = requestSchema()
                validated_data = schema.load(data)

                request.validated_data = validated_data
            except json.JSONDecodeError:
                return ErrorResponse(status_code=400, message="Invalid json")
            except ValidationError as err:
                return ErrorResponse(status_code=400, message=str(err.messages))
            
            return func(self, request, *args, **kwargs)

        return inner
    
    return decorator


# Решил, что не буду добавлять миксин LoginRequired
# Буду отправлять ошибки на фронт - там разберутся
# Также отключил CSRF токен - думаю, что поставить лайк за другого не так страшно
class QuestionLikeView(View):
    http_method_names = ["post"]

    @json_login_required
    @validate_data_with(QuestionLikeSchema)
    def post(self, request):
        question_id = request.validated_data.get("question_id")
        is_like = request.validated_data.get("is_like")
        
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return ErrorResponse(status_code=404, message="Question does not exists")
        
        like, created = QuestionsLikes.objects.get_or_create(
            profile=request.user.profile,
            question=question,
            defaults={"is_like": is_like}
        )

        if created:
            return OkResponse(
                status_code=201,
                message="Like set",
                data=dict(rating=Question.objects.get(id=question_id).rating_cache))

        if like.is_like == is_like:
            like.delete()

            return OkResponse(
                status_code=200,
                message="Like unset",
                data=dict(rating=Question.objects.get(id=question_id).rating_cache))
        
        like.is_like = is_like
        like.save()

        return OkResponse(
            status_code=200,
            message="Like updated",
            data=dict(rating=Question.objects.get(id=question_id).rating_cache)) # Ужас
    

class AnswerLikeView(View):
    http_method_names = ["post"]

    @json_login_required
    @validate_data_with(AnswerLikeSchema)
    def post(self, request):
        answer_id = request.validated_data.get("answer_id")
        is_like = request.validated_data.get("is_like")
        
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return ErrorResponse(status_code=404, message="Answer does not exists")
        
        like, created = AnswersLikes.objects.get_or_create(
            profile=request.user.profile,
            answer=answer,
            defaults={"is_like": is_like}
        )

        # TODO: сделать денормализацию
        if created:
            return OkResponse(
                status_code=201,
                message="Like set",
                data=dict(rating=Answer.objects.with_rating().get(id=answer_id).rating))

        if like.is_like == is_like:
            like.delete()

            return OkResponse(
                status_code=200,
                message="Like unset",
                data=dict(rating=Answer.objects.with_rating().get(id=answer_id).rating))
        
        like.is_like = is_like
        like.save()

        return OkResponse(
            status_code=200,
            message="Like updated",
            data=dict(rating=Answer.objects.with_rating().get(id=answer_id).rating)) # УЖАС
    

class AnswerCorrectView(View):
    http_method_names = ["post"]

    @json_login_required
    @validate_data_with(AnswerCorrectSchema)
    def post(self, request):
        answer_id = request.validated_data.get("answer_id")
        is_correct = request.validated_data.get("is_correct")
        
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return ErrorResponse(status_code=404, message="Answer does not exists")
        
        if request.user.profile == answer.question.profile:
            answer.is_correct = is_correct
            answer.save()

            return OkResponse(
                status_code=200,
                message="Correct status changed",
                data=dict(is_correct=answer.is_correct))
        else:
            return OkResponse(
                status_code=403,
                message="It is not your question",
                data=dict(is_correct=answer.is_correct)
            )
        

class GetBestMembers(View):
    http_method_names = ["get"]

    def get(self, request):
        best_members = cache.get("best-members")

        if best_members is None:
            best_members = []

        return OkResponse(
            status_code=200,
            data=dict(
                members=best_members
            )
        )
    

class GetBestTags(View):
    http_method_names = ["get"]

    def get(self, request):
        best_tags = cache.get("best-tags")

        if best_tags is None:
            best_tags = []

        return OkResponse(
            status_code=200,
            data=dict(
                tags=best_tags
            )
        )
    

class GetSearchHint(View):
    http_method_names = ["get"]

    def get(self, request):
        query = request.GET.get("query")

        index = SearchIndex()
        result = index.search(query)

        questions = Question.objects.filter(id__in=result).only("id", "title")[:5]

        response = [
            {"id": q.id, "title": q.title, "url": q.url}
            for q in questions
        ]

        return OkResponse(
            status_code=200,
            data=dict(
                result=response
            )
        )