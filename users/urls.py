from django.urls import path, include
from users.views import login_view
from users.views import reset_password

from users.views import CustomUserCreationView
from users.views import ActivationUserView
from users.views import profile_view
from users.views import LogoutView
from users.views import complete_profile


app_name="auth"

urlpatterns = [
    path('profile', profile_view, name='profile_user'),
    path('login/', login_view, name='login'),
    path('create/', CustomUserCreationView.as_view(), name='register'),
    path('activation/<uid>/<token>', ActivationUserView.as_view(), name='confirm_user_activation'),
    path('activation/<uid>/<token>', reset_password, name='reset_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('complete-profile/<uid>/', complete_profile, name='complete_profile'),
    path('', include('django.contrib.auth.urls')),
]

