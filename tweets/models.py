from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tweet(models.Model):
    content = models.TextField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "tweet"],
                name="like_unique",
            ),
        ]

    def __str__(self):
        return f"{self.user}like{self.tweet}"
