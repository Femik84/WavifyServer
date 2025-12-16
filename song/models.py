from django.db import models
from artist.models import Artist
from genre.models import Genre
from playlist.models import Playlist
from django.core.exceptions import ValidationError
from mutagen import File as MutagenFile

# -----------------------------
# Validator for audio files
# -----------------------------
def validate_audio_file(value):
    valid_extensions = ['.mp3', '.m4a']
    import os
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: .mp3, .m4a')


# -----------------------------
# Song model
# -----------------------------
class Song(models.Model):
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds",
        blank=True,
        null=True
    )
    cover = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    audio = models.FileField(
        upload_to='songs/',
        validators=[validate_audio_file]
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='songs')
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, related_name='songs')

    # Global flags
    is_trending = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    is_top_chart = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    # -----------------------------
    # Auto-set duration when saving
    # -----------------------------
    def save(self, *args, **kwargs):
        if self.audio:
            try:
                audio_file = MutagenFile(self.audio)
                if audio_file is not None and hasattr(audio_file.info, 'length'):
                    # Duration in seconds (rounded to int)
                    self.duration = int(audio_file.info.length)
            except Exception as e:
                print("Error reading audio duration:", e)
        super().save(*args, **kwargs)
