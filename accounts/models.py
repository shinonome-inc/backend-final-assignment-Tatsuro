from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = "custom_user"

    age = models.IntegerField("age", blank=True, null=True)
    email = models.EmailField(unique=True)


# class FriendShip(models.Model):
#     pass
