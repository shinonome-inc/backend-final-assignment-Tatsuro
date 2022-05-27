from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'welcome'
urlpatterns = [
    path('', TemplateView.as_view(template_name='welcome/index.html')),
]
