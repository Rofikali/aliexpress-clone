from .models import Post
from django.contrib import admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display = ('id', 'text', 'video', 'created_at', 'updated_at')
    list_display = ("id", "user", "text", "video", "created_at", "updated_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "text",'user__name')
    ordering = ("-created_at",)
