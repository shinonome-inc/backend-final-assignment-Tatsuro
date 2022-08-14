from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


CustomUser = get_user_model()


class Tweet(models.Model):
    content = models.TextField(max_length=140)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content
