from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import SignupForm

class SignupView(CreateView):

    form_class = SignupForm
    success_url = reverse_lazy('welcome:home')
    template_name = 'registration/signup.html'

    def form_valid(self, form): 
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
