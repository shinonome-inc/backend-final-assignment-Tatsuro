from django.urls import path

from . import views

app_name = "welcome"
urlpatterns = [
    # path("accounts/home/", views.HomeView.as_view(), name="home"),
    path("", views.WelcomeView.as_view(), name="welcome"),
]
