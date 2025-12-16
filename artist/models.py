from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)
    followers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
