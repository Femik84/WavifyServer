from rest_framework import generics
from .models import Playlist
from .serializers import PlaylistSerializer

class PlaylistListView(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistDetailView(generics.RetrieveAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
