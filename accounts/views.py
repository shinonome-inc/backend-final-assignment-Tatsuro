from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import FriendShip
from .forms import SignupForm
from tweets.models import Tweet

User = get_user_model()


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


class HomeView(ListView):
    model = Tweet
    template_name = "home.html"
    ordering = ["-created_at"]
    queryset = Tweet.objects.select_related("user")
    context_object_name = "tweet_list"


class LoginView(LoginView):
    template_name = "registration/login.html"


class LogoutView(LogoutView):
    template_name = "registration/login.html"


class FollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/follow.html"
    model = FriendShip

    def post(self, request, *args, **kwargs):
        try:
            follower = self.request.user
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.error(request, "You can't follow yourself.")
                return render(request, "accounts/follow.html")

            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                messages.error(request, "You have already followed.")
                return render(request, "accounts/follow.html")
            else:
                FriendShip.objects.get_or_create(follower=follower, following=following)
                messages.success(request, "You've just followed.")
                return HttpResponseRedirect(reverse_lazy("accounts:home"))

        except User.DoesNotExist:
            messages.error(request, "This user does not exist.")
            raise Http404


class UnFollowView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/unfollow.html"
    model = FriendShip

    def post(self, request, *args, **kwargs):
        try:
            follower = self.request.user
            following = User.objects.get(username=self.kwargs["username"])
            if follower == following:
                messages.error(request, "This is your account.")
                return render(request, "accounts/unfollow.html")
            elif FriendShip.objects.filter(
                follower=follower, following=following
            ).exists():
                FriendShip.objects.filter(
                    following=following, follower=follower
                ).delete()
                messages.success(request, "You've just unfollowed.")
                return HttpResponseRedirect(reverse_lazy("accounts:home"))
            else:
                messages.error(request, "You haven't follow the user.")
                return render(request, "accounts/unfollow.html")
        except User.DoesNotExist:
            messages.error(request, "This user does not exist.")
            raise Http404


class FollowingListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/following_list.html"

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context["following_number"] = FriendShip.objects.filter(follower=user).count()
        context["following_list"] = FriendShip.objects.select_related(
            "following"
        ).filter(follower=user)

        return context


class FollowerListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/follower_list.html"

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context["follower_number"] = FriendShip.objects.filter(following=user).count()
        context["follower_list"] = FriendShip.objects.select_related("follower").filter(
            following=user
        )

        return context
