from rest_framework import serializers
from .models import Artist
from user.models import FavoriteArtist  

class ArtistSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = [
            'id',
            'name',
            'image',
            'followers',
            'is_favorite',
        ]

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteArtist.objects.filter(user=request.user, artist=obj).exists()
        return False
