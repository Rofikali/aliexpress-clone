# apps/home/models/section_category.py
import uuid
from django.db import models
# from apps.home.models.section import HomepageSection
from apps.products.models.category import Category


class HomepageCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name="+", on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        db_table = "home_section_category"

    def __str__(self):
        return f"{self.section.slug} -> {self.category.name}"
