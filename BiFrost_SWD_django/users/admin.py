from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "home_city", "preferred_currency", "created_at"]
    search_fields = ["user__username", "user__email", "home_city"]
    list_filter = ["preferred_currency"]