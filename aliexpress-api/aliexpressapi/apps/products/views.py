from rest_framework.viewsets import ViewSet
from .models import Products
from rest_framework.response import Response
from .serializers import ProductSerializer


class productsViewSet(ViewSet):
    def list(self, request):
        queryset = Products.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
