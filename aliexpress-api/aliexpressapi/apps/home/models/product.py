# apps/home/models/section_product.py
import uuid
from django.db import models

# from apps.home.models.section import HomepageSection
from apps.products.models.product import Product


class HomepageProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # section = models.ForeignKey(HomepageSection, related_name="products", on_delete=models.CASCADE)
    featured_rank = models.PositiveIntegerField(default=0)  # ✅ add this
    product = models.ForeignKey(Product, related_name="+", on_delete=models.CASCADE)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        db_table = "home_section_product"

    def __str__(self):
        return f"SectionProduct: {self.product.slug} -> {self.product_id}"
