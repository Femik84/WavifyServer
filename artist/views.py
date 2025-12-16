from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Artist
from .serializers import ArtistSerializer
from user.models import FavoriteArtist
class ArtistListView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_context(self):
        return {"request": self.request}
class ArtistDetailView(generics.RetrieveAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get_serializer_context(self):
        return {"request": self.request}
class FavoriteArtistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        Favorite an artist
        """
        artist = generics.get_object_or_404(Artist, pk=pk)

        FavoriteArtist.objects.get_or_create(
            user=request.user,
            artist=artist
        )

        return Response(
            {"detail": "Artist added to favorites"},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        """
        Unfavorite an artist
        """
        artist = generics.get_object_or_404(Artist, pk=pk)

        FavoriteArtist.objects.filter(
            user=request.user,
            artist=artist
        ).delete()

        return Response(
            {"detail": "Artist removed from favorites"},
            status=status.HTTP_204_NO_CONTENT
        )
