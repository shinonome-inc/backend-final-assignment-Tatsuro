from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView
from .models import Tweet, Like
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import TweetForm


class TweetCreateView(LoginRequiredMixin, CreateView):
    form_class = TweetForm
    template_name = "tweets/tweet_create.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    template_name = "tweets/tweet_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_for_tweet_count = self.object.like_set.count()
        context["like_number"] = like_for_tweet_count
        # ログイン中のユーザーがいいねしているか否か
        if self.object.like_set.filter(user=self.request.user).exists():
            context["is_user_like_for_tweet"] = True
        else:
            context["is_user_like_for_tweet"] = False

        return context


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "tweets/tweet_delete.html"
    model = Tweet
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user


class LikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        Like.objects.get_or_create(tweet=tweet, user=user)
        context = {"like_number": tweet.like_set.count(), "tweet_pk": tweet.pk}

        return JsonResponse(context)


class UnlikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        tweet = get_object_or_404(Tweet, pk=kwargs["pk"])
        Like.objects.filter(user=user, tweet=tweet).delete()
        context = {"like_number": tweet.like_set.count(), "tweet_pk": tweet.pk}

        return JsonResponse(context)
