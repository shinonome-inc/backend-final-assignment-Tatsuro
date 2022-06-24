from django.contrib import admin
from django.urls import include, path
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
     #path('tweets/', include('tweets.urls')),
    path('', include('welcome.urls')),
]
