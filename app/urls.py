from django.urls import path

from app.views import *


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('settings', SettingsView.as_view(), name='settings'),
    path('hot', HotQuestionsView.as_view(), name='hot'),
    path('tag/<str:tag>', QuestionsByTagView.as_view(), name='tag'),
    path('question/<int:question_id>', QuestionView.as_view(), name='question'),
    path('ask', AskView.as_view(), name='ask'),
]