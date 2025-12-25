import logging

from django.views.generic import TemplateView

from django.core.cache import cache

from app.mixins import PaginatorMixin, StatisticsMixin
from app.models import Question
from app.search_index import SearchIndex


logger = logging.getLogger(__name__)


class HomeView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'home.html'

    def get_object_list(self):
        return Question.objects.get_newest()
    

class HotQuestionsView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'hot.html'

    should_cache = True
    cache_key = "hot_questions"
    page_cache_limit = 3

    def get_object_list(self):
        return Question.objects.get_hottest()
    

class QuestionsByTagView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'by_tag.html'

    def get_object_list(self):
        return Question.objects.get_by_tags([self.kwargs["tag"]]).get_hottest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["tag"] = self.kwargs["tag"]

        return context
    

class SearchView(PaginatorMixin, TemplateView):
    objects_per_page = 10
    template_name = 'search.html'

    def get_object_list(self):
        query = self.request.GET.get("query")

        index = SearchIndex()
        result = index.search(query)

        return Question.objects.filter(id__in=result)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["query"] = self.request.GET.get("query")

        return context