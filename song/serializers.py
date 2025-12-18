from rest_framework import serializers
from .models import Song
from artist.serializers import ArtistSerializer
from genre.serializers import GenreSerializer
from playlist.serializers import PlaylistSerializer
from user.models import LikedSong, RecentlyPlayedSong


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    playlist = PlaylistSerializer(read_only=True)

    # User-specific fields
    is_liked = serializers.SerializerMethodField()
    is_recently_played = serializers.SerializerMethodField()
    last_played_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Song
        fields = [
            "id",
            "title",
            "album",
            "duration",
            "cover",
            "audio",
            "artist",
            "genre",
            "playlist",
            "is_trending",
            "is_new_release",
            "is_top_chart",
            "is_liked",
            "is_recently_played",
            "last_played_at",
        ]

    # -----------------------------
    # User-specific logic
    # -----------------------------
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return LikedSong.objects.filter(
            user=request.user,
            song=obj
        ).exists()

    def get_is_recently_played(self, obj):
        """
        True if the user has ANY play history for this song
        """
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return RecentlyPlayedSong.objects.filter(
            user=request.user,
            song=obj
        ).exists()
