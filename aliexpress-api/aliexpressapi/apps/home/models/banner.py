# apps/home/models/banner.py
import uuid
from django.db import models
# from apps.home.models.section import HomepageSection

class HomepageBanner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # section = models.ForeignKey(HomepageSection, related_name="banners", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="home/banners/")
    link_url = models.CharField(max_length=512, null=True, blank=True)
    alt_text = models.CharField(max_length=255, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order"]
        db_table = "home_banner"

    def __str__(self):
        return f"Banner {self.id} ({self.title})"
