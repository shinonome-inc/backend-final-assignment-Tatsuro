from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy

from .forms import SignupForm


class SignupView(CreateView):

    form_class = SignupForm
    success_url = reverse_lazy("accounts:home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return response


class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(LoginView):
    template_name = "registration/login.html"


class LogoutView(LogoutView):
    template_name = "registration/login.html"
