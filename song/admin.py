from django.contrib import admin
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'album', 'artist', 'genre', 'playlist',
        'duration_display', 'is_trending', 'is_new_release', 'is_top_chart'
    )
    search_fields = ('title', 'album', 'artist__name', 'playlist__name')
    list_filter = ('is_trending', 'is_new_release', 'is_top_chart', 'genre', 'playlist')
    ordering = ('title',)
    readonly_fields = ('duration', 'audio_preview')  # show audio preview and duration in form

    # -----------------------------
    # Display duration in MM:SS
    # -----------------------------
    def duration_display(self, obj):
        if obj.duration:
            minutes, seconds = divmod(obj.duration, 60)
            return f"{minutes}:{seconds:02d}"
        return "-"
    duration_display.short_description = 'Duration'

    # -----------------------------
    # Optional: audio preview in admin
    # -----------------------------
    def audio_preview(self, obj):
        if obj.audio:
            return f'<audio controls><source src="{obj.audio.url}" type="audio/mpeg"></audio>'
        return "-"
    audio_preview.allow_tags = True
    audio_preview.short_description = "Audio Preview"
