from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import FriendShip

CustomUser = get_user_model()

admin.site.register(CustomUser, UserAdmin)

admin.site.register(FriendShip)
