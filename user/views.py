from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserUpdateSerializer,
)
from artist.serializers import ArtistSerializer


# ============================
# REGISTER VIEW
# ============================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "full_name": user.full_name,
                "email": user.email,
                "bio": user.bio,
                "image": request.build_absolute_uri(user.image.url) if user.image else None,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


# ============================
# LOGIN VIEW
# ============================
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "full_name": user.full_name,
                "email": user.email,
                "bio": user.bio,
                "image": request.build_absolute_uri(user.image.url) if user.image else None,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


# ============================
# USER PROFILE (GET / UPDATE)
# ============================
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update the logged-in user's profile.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {"request": self.request}

    def update(self, request, *args, **kwargs):
        partial = True  # Allow PATCH-like behavior
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": {
                "full_name": user.full_name,
                "email": user.email,
                "bio": user.bio,
                "image": request.build_absolute_uri(user.image.url) if user.image else None,
            }
        }, status=status.HTTP_200_OK)


# ============================
# FAVORITE ARTISTS
# ============================
class FavoriteArtistsView(generics.ListAPIView):
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.favorite_artists.all()
