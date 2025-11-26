import logging

from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout

from app.mixins import StatisticsMixin

from app.forms.auth_forms import LoginForm, RegisterForm


logger = logging.getLogger(__name__)


class LoginView(StatisticsMixin, TemplateView):
    template_name = 'login.html'

    def get(self, request):
        context = super().get_context_data(form=LoginForm())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            logger.debug("Form is valid!")
            cleaned_data = form.cleaned_data

            user = authenticate(
                request,
                username=cleaned_data["login"],
                password=cleaned_data["password"]
            )

            if user is not None:
                if user.is_active:
                    login(request, user)

                    continue_url = request.GET.get("continue")
                    if continue_url:
                        return redirect(continue_url)
                    
                    return redirect('index')
                else:
                    form.add_error(None, "Cannot login")
            else:
                form.add_error(None, "Incorrect login or password")
        
        context = super().get_context_data(form=form)
        return self.render_to_response(context)


class RegisterView(StatisticsMixin, TemplateView):
    template_name = 'register.html'

    def get(self, request):
        context = super().get_context_data(form=RegisterForm())
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            logger.debug("Form is valid!")

            user = form.save()
            login(request, user)
            return redirect("index")
        
        context = super().get_context_data(form=form)
        return self.render_to_response(context)


class LogoutView(View):
    http_method_names = ["post"]

    def post(self, request):
        logout(request)

        continue_url = request.GET.get("continue")
        if continue_url:
            return redirect(continue_url)

        return redirect("index")