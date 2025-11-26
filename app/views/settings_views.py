import logging

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from app.mixins import StatisticsMixin

from app.forms.settings_forms import UserSettingsForm, ProfileSettingsForm


logger = logging.getLogger(__name__)


class SettingsView(LoginRequiredMixin, StatisticsMixin, TemplateView):
    template_name = 'settings.html'

    login_url = reverse_lazy("login")
    redirect_field_name = "continue"

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user_form"] = UserSettingsForm(instance=request.user)
        context["profile_form"] = ProfileSettingsForm(instance=request.user.profile)

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        user_form = UserSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("settings")
        
        context = super().get_context_data(**kwargs)

        context["user_form"] = user_form
        context["profile_form"] = profile_form

        return self.render_to_response(context)