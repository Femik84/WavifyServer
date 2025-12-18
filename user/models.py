from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from artist.models import Artist
from song.models import Song


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, bio=None, image=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not full_name:
            raise ValueError("Users must have a full name")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, bio=bio, image=image)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password, bio=None, image=None):
        user = self.create_user(email, full_name, password, bio, image)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    favorite_artists = models.ManyToManyField(
        Artist,
        through="FavoriteArtist",
        related_name="favorited_by_users",
        blank=True
    )

    liked_songs = models.ManyToManyField(
        Song,
        through="LikedSong",
        related_name="liked_by_users",
        blank=True
    )

    recently_played_songs = models.ManyToManyField(
        Song,
        through="RecentlyPlayedSong",
        related_name="recently_played_by_users",
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

class FavoriteArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "artist")
        indexes = [
            models.Index(fields=["user", "artist"]),
        ]


class LikedSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "song")
        indexes = [
            models.Index(fields=["user", "song"]),
        ]


class RecentlyPlayedSong(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recently_played_entries"
    )
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="play_history"
    )
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-played_at"]
        indexes = [
            models.Index(fields=["user", "-played_at"]),
            models.Index(fields=["song"]),
        ]
