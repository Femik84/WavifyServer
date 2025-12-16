from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='playlists/', blank=True, null=True)
    is_hero_slide = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    is_profile = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
