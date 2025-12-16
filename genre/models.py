from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='genres/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
