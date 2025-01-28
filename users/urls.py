from django.urls import include, path

from users.views import (
    ActivationUserView,
    CustomUserCreationView,
    LogoutView,
    complete_profile,
    login_view,
    profile_view,
    reset_password,
)

app_name = "auth"

urlpatterns = [
    path("profile", profile_view, name="profile_user"),
    path("login/", login_view, name="login"),
    path("create/", CustomUserCreationView.as_view(), name="register"),
    path("activation/<uid>/<token>", ActivationUserView.as_view(), name="confirm_user_activation"),
    path("activation/<uid>/<token>", reset_password, name="reset_password"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("complete-profile/<uid>/", complete_profile, name="complete_profile"),
    path("", include("django.contrib.auth.urls")),
]
