import logging

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from app.mixins import StatisticsMixin
from app.models import Question

from app.forms.content_forms import AskQuestionForm, AddAnswerForm


logger = logging.getLogger(__name__)


class QuestionView(StatisticsMixin, TemplateView):
    template_name = 'questions/single.html'

    def get_object(self):
        return get_object_or_404(
            Question.objects.with_related(), pk=self.kwargs["question_id"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["question"] = self.get_object()

        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(form=AddAnswerForm())
        return self.render_to_response(context)
    
    @method_decorator(login_required(redirect_field_name="continue", login_url=reverse_lazy("login")))
    def post(self, request, *args, **kwargs):
        form = AddAnswerForm(request.POST)
        context = self.get_context_data()

        if form.is_valid():
            answer = form.save(commit=False)

            answer.profile = request.user.profile
            answer.question = context["question"]
            answer.save()

            return redirect(f"{context["question"].url}#answer-{answer.pk}")

        context["form"] = form
        return self.render_to_response(context)


class AskView(LoginRequiredMixin, StatisticsMixin, TemplateView):
    template_name = 'ask.html'

    login_url = reverse_lazy("login")
    redirect_field_name = "continue"

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(form=AskQuestionForm())
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form = AskQuestionForm(request.POST)

        if form.is_valid():
            question = form.save()
            question.profile = request.user.profile
            question.save()

            return redirect(question)

        context = super().get_context_data(form=form)
        return self.render_to_response(context)