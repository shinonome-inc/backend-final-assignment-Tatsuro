from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, DeleteView
from .models import Tweet
from django.urls import reverse_lazy

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


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    template_name = "tweets/tweet_delete.html"
    model = Tweet
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        self.object = self.get_object()
        return self.object.user == self.request.user
