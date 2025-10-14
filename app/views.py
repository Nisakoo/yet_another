import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'home.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class RegisterView(TemplateView):
    template_name = 'register.html'


class SettingsView(TemplateView):
    template_name = 'settings.html'


class HotQuestionsView(TemplateView):
    template_name = 'hot.html'


class QuestionsByTagView(TemplateView):
    template_name = 'by_tag.html'


class QuestionView(TemplateView):
    template_name = 'questions/single.html'


class AskView(TemplateView):
    template_name = 'ask.html'