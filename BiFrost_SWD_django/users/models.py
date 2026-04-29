from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Extended profile for the built-in Django User model.
    Stores BiFrost-specific user preferences and metadata.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, help_text="Short bio or travel interests.")
    home_city = models.CharField(max_length=100, blank=True)
    preferred_currency = models.CharField(max_length=10, default="USD")
    avatar_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"