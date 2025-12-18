from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery

from .models import Song
from .serializers import SongSerializer
from user.models import LikedSong, RecentlyPlayedSong


class SongListView(generics.ListAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}

class SongDetailView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_serializer_context(self):
        return {"request": self.request}

class ToggleLikeSongView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id):
        user = request.user

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"detail": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        liked = LikedSong.objects.filter(user=user, song=song)

        if liked.exists():
            liked.delete()
            return Response({"is_liked": False}, status=status.HTTP_200_OK)

        LikedSong.objects.create(user=user, song=song)
        return Response({"is_liked": True}, status=status.HTTP_201_CREATED)


class TrackRecentlyPlayedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id):
        user = request.user

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"detail": "Song not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        RecentlyPlayedSong.objects.create(
            user=user,
            song=song
        )

        return Response(
            {"detail": "Song play recorded"},
            status=status.HTTP_201_CREATED
        )

class LikedSongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Song.objects.filter(
            liked_by_users=self.request.user
        ).distinct()

    def get_serializer_context(self):
        return {"request": self.request}



class RecentlyPlayedSongsView(generics.ListAPIView):
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        latest_play = RecentlyPlayedSong.objects.filter(
            user=user,
            song=OuterRef("pk")
        ).order_by("-played_at")

        return (
            Song.objects
            .filter(play_history__user=user)
            .annotate(last_played_at=Subquery(latest_play.values("played_at")[:1]))
            .order_by("-last_played_at")
            .distinct()
        )

    def get_serializer_context(self):
        return {"request": self.request}
