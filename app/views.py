import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.base import TemplateResponseMixin

from .mixins import PaginatorMixin


logger = logging.getLogger(__name__)


QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "description": "Default description",
        "answers_count": i * 10 % 9,
        "tags": ["Rust", "Blazing", "Fast"]
    } for i in range(30)
]


class HomeView(PaginatorMixin, TemplateView):
    objects_per_page = 10
    template_name = 'home.html'

    def get_object_list(self):
        return QUESTIONS

    def get_context_data(self, **kwargs):
        context = {}
        context['page_obj'] = self.get_page_object(self.get_object_list())
        return context


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


class SettingsView(TemplateView):
    template_name = 'settings.html'


class HotQuestionsView(PaginatorMixin, TemplateView):
    objects_per_page = 10
    template_name = 'hot.html'

    def get_object_list(self):
        return QUESTIONS

    def get_context_data(self, **kwargs):
        context = {}
        context['page_obj'] = self.get_page_object(self.get_object_list())
        return context


class QuestionsByTagView(PaginatorMixin, TemplateView):
    objects_per_page = 10
    template_name = 'by_tag.html'

    def get_object_list(self):
        return QUESTIONS

    def get_context_data(self, **kwargs):
        context = {}
        context['page_obj'] = self.get_page_object(self.get_object_list())
        context['tag'] = 'Idris'
        return context


class QuestionView(TemplateView):
    template_name = 'questions/single.html'


class AskView(TemplateView):
    template_name = 'ask.html'