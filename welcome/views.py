from django.views.generic import TemplateView


class WelcomeView(TemplateView):
    template_name = "top.html"


class HomeView(TemplateView):
    template_name = "home.html"
