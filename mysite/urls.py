from django.contrib import admin
from django.urls import include, path

# from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("tweets/", include("tweets.urls")),
    path("", include("welcome.urls")),
]

""" if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
       path("__debug__/", include(debug_toolbar.urls)),
      ]
"""
