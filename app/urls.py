from django.urls import path

from .views import (
    HomeView,
    LoginView,
    RegisterView,
    SettingsView,
    HotQuestionsView,
    QuestionsByTagView,
    QuestionView,
    AskView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('hot', HotQuestionsView.as_view(), name='hot'),
    path('tag/<str:tag>', QuestionsByTagView.as_view(), name='by-tag'),
    path('question/<int:question_id>', QuestionView.as_view(), name='question'),
    path('ask', AskView.as_view(), name='ask'),
]