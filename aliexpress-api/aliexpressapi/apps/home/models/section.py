# apps/home/models/section.py
import uuid
from django.db import models


class HomepageSection(models.Model):
    SECTION_TYPE_CHOICES = [
        ("banner", "Banner"),
        ("product_carousel", "Product Carousel"),
        ("category_links", "Category Links"),
        ("promo", "Promotional"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    type = models.CharField(max_length=32, choices=SECTION_TYPE_CHOICES, db_index=True)
    position = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    metadata = models.JSONField(null=True, blank=True)  # arbitrary config for section
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["position", "-created_at"]
        db_table = "home_section"

    def __str__(self):
        return f"{self.title} ({self.type})"
