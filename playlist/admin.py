from django.contrib import admin
from .models import Playlist

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_hero_slide', 'is_featured', 'is_profile', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_hero_slide', 'is_featured', 'is_profile')
    ordering = ('name',)
