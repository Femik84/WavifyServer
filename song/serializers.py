from rest_framework import serializers
from .models import Song
from artist.serializers import ArtistSerializer
from genre.serializers import GenreSerializer
from playlist.serializers import PlaylistSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    playlist = PlaylistSerializer(read_only=True)

    # User-specific flags
    is_liked = serializers.SerializerMethodField()
    is_recently_played = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = [
            'id',
            'title',
            'album',
            'duration',
            'cover',
            'audio',
            'artist',
            'genre',
            'playlist',
            'is_trending',
            'is_new_release',
            'is_top_chart',
            'is_liked',
            'is_recently_played',
        ]

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.liked_by_users.filter(id=user.id).exists()
        return False

    def get_is_recently_played(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.recently_played_by_users.filter(id=user.id).exists()
        return False
