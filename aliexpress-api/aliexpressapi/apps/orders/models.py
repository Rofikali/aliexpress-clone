from django.db import models
from django.conf import settings


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    seller = models.ForeignKey("users.Seller", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    warehouse = models.ForeignKey("inventory.Warehouse", on_delete=models.CASCADE)
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    estimated_delivery = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Return(models.Model):
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("processed", "Processed"),
        ("rejected", "Rejected"),
    ]
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="requested"
    )
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
