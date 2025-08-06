from requests import get

from apps.core.models import (
    AutoUpdate,
)  # Adjust the import based on your project structure
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(AutoUpdate):
    # user = models.ForeignKey('api.User', on_delete=models.CASCADE)  # Use 'api.User'
    user = models.ForeignKey(
        User,  # Refers to the custom User model
        on_delete=models.CASCADE,
        related_name="posts",  # Reverse relationship (user.posts.all())
    )
    text = models.TextField()
    video = models.FileField(upload_to="videos/", null=True, blank=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.text}"

    class Meta:
        ordering = ["-created_at"]  # Latest posts appear first
