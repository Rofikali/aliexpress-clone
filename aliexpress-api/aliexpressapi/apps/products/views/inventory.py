
# apps.products/views/inventory_view.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import extend_schema

from apps.products.models.inventory import (
    Inventory,
)
from apps.products.serializers.inventory import (
    InventorySerializer,
) 

# -------------------- INVENTORY --------------------
class InventoryViewSet(ViewSet):
    @extend_schema(
        responses={200: InventorySerializer(many=True)},
        tags=["Inventory"],
    )
    def list(self, request):
        queryset = Inventory.objects.all()
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: InventorySerializer},
        tags=["Inventory"],
    )
    def retrieve(self, request, pk=None):
        stock = get_object_or_404(Inventory, id=pk)
        serializer = InventorySerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
