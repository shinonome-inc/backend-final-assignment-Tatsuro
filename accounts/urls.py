from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    # path('', views.WelcomeView.as_view(), name='welcome'),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('home/', views.HomeView.as_view(), name='home'),
    # path('', include('django.contrib.auth.urls')),
    # path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    # path('profile/edit/', views.UserProfileEditView.as_view(), name='user_profile_edit'),
    # path('<str:username>/following_list/', views.FollowingListView.as_view(), name='following_list'),
    # path('<str:username>/follower_list/', views.FollowerListView.as_view(), name='follower_list'),
    # path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    # path('<str:username>/unfollow/', views.UnFollowView, name='unfollow'),
]
