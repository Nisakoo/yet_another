import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.base import TemplateResponseMixin

from .mixins import PaginatorMixin, StatisticsMixin
from .models import (
    Question
)


logger = logging.getLogger(__name__)


class HomeView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'home.html'

    def get_object_list(self):
        return Question.objects.get_newest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["page_obj"] = self.get_page_object(self.get_object_list())

        return context


class LoginView(StatisticsMixin, TemplateView):
    template_name = 'login.html'


class RegisterView(StatisticsMixin, TemplateView):
    template_name = 'register.html'


class SettingsView(StatisticsMixin, TemplateView):
    template_name = 'settings.html'


class HotQuestionsView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'hot.html'

    def get_object_list(self):
        return Question.objects.get_hottest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["page_obj"] = self.get_page_object(self.get_object_list())

        return context
    

class QuestionsByTagView(PaginatorMixin, StatisticsMixin, TemplateView):
    objects_per_page = 10
    template_name = 'by_tag.html'

    def get_object_list(self):
        return Question.objects.get_by_tags([self.kwargs["tag"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["page_obj"] = self.get_page_object(self.get_object_list())
        context["tag"] = self.kwargs["tag"]

        return context


class QuestionView(StatisticsMixin, TemplateView):
    template_name = 'questions/single.html'

    def get_object(self):
        return get_object_or_404(
            Question.objects.with_rating(),
            pk=self.kwargs["question_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context["question"] = self.get_object()

        return context


class AskView(StatisticsMixin, TemplateView):
    template_name = 'ask.html'