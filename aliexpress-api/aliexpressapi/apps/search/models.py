from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class SearchIndex(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        "products.Category", on_delete=models.SET_NULL, null=True
    )
    brand = models.ForeignKey("products.Brand", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RecommendationRule(models.Model):
    RULE_TYPE_CHOICES = [
        ("also_bought", "Also Bought"),
        ("trending", "Trending"),
        ("personalized", "Personalized"),
    ]
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    parameters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RecommendationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="logged_product"
    )
    recommended_product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="recommended_product"
    )
    rule = models.ForeignKey(RecommendationRule, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
