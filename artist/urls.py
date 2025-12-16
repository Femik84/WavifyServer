from django.urls import path
from .views import (
    ArtistListView,
    ArtistDetailView,
    FavoriteArtistView,
)

urlpatterns = [
    path('', ArtistListView.as_view(), name='artist-list'),
    path('<int:pk>/', ArtistDetailView.as_view(), name='artist-detail'),

    # favorite / unfavorite
    path('<int:pk>/favorite/', FavoriteArtistView.as_view(), name='artist-favorite'),
]
