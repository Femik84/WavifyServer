from django.urls import path
from .views import (
    SongListView,
    SongDetailView,
    ToggleLikeSongView,
    TrackRecentlyPlayedView,
    LikedSongsView,
    RecentlyPlayedSongsView,
)

urlpatterns = [
    path("", SongListView.as_view(), name="song-list"),
    path("<int:pk>/", SongDetailView.as_view(), name="song-detail"),

    path("<int:song_id>/like/", ToggleLikeSongView.as_view(), name="song-like"),
    path("<int:song_id>/play/", TrackRecentlyPlayedView.as_view(), name="song-play"),

    path("liked/", LikedSongsView.as_view(), name="liked-songs"),
    path("recently-played/", RecentlyPlayedSongsView.as_view(), name="recently-played-songs"),
]
