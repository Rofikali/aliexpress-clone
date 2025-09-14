from rest_framework import serializers
from apps.products.models import (
    Inventory,
)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "product", "quantity", "location"]
