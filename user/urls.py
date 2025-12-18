from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    UserProfileView,
    FavoriteArtistsView,
)

urlpatterns = [
    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # User profile (GET / PATCH)
    path("profile/", UserProfileView.as_view(), name="user_profile"),

    # Favorites
    path("favorites/artists/", FavoriteArtistsView.as_view(), name="favorite_artists"),
]
