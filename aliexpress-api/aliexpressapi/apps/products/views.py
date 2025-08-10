from rest_framework.viewsets import ViewSet
from .models import Products
from rest_framework.response import Response
from .serializers import ProductSerializer

# paginations are here
# from components.paginations.cursor_pagination import CustomCursorPagination
from components.paginations.infinite_scroll import InfiniteScrollPagination


class productsViewSet(ViewSet):
    # pagination_class = CustomCursorPagination

    def list(self, request):
        queryset = Products.objects.all()
        paginator = InfiniteScrollPagination()
        paginator_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(
            paginator_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)
