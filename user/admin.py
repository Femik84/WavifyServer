from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FavoriteArtist, LikedSong, RecentlyPlayedSong

# ------------------------
# Inline admin classes
# ------------------------
class FavoriteArtistInline(admin.TabularInline):
    model = FavoriteArtist
    extra = 0
    readonly_fields = ("artist", "created_at")  # show artist details only
    can_delete = False

class LikedSongInline(admin.TabularInline):
    model = LikedSong
    extra = 0
    readonly_fields = ("song", "created_at")
    can_delete = False

class RecentlyPlayedSongInline(admin.TabularInline):
    model = RecentlyPlayedSong
    extra = 0
    readonly_fields = ("song", "played_at")
    can_delete = False

# ------------------------
# User admin
# ------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "bio", "image")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "bio", "image", "is_staff", "is_active"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")

    # ------------------------
    # Include inlines
    # ------------------------
    inlines = [FavoriteArtistInline, LikedSongInline, RecentlyPlayedSongInline]
