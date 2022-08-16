from django.contrib.auth import get_user_model
from django.db import models


CustomUser = get_user_model()


class Tweet(models.Model):
    content = models.TextField(max_length=140)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
