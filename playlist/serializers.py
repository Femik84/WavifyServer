from rest_framework import serializers
from .models import Playlist

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            'id',
            'name',
            'description',
            'image',
            'is_hero_slide',
            'is_featured',
            'is_profile',
        ]
