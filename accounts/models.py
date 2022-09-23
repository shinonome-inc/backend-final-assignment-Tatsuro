from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"

    age = models.IntegerField("age", blank=True, null=True)
    email = models.EmailField(unique=True)


class FriendShip(models.Model):
    following = models.ForeignKey(
        CustomUser,
        related_name="following",
        on_delete=models.CASCADE,
    )
    follower = models.ForeignKey(
        CustomUser,
        related_name="follower",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["following", "follower"], name="follow_unique"
            ),
        ]

    def __str__(self):
        return f"{self.follower}follow{self.following}"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    introduction = models.CharField("Self introduction", max_length=255, blank=True)

    def __str__(self):
        return str(self.user)
