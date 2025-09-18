🖥 Views (views.py)
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing Categories and their related Products.
    """

    # GET /api/v1/categories/ → List all categories in tree structure
    def list(self, request):
        queryset = Category.objects.filter(parent__isnull=True, is_active=True)
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET /api/v1/categories/{id}/ → Retrieve a single category with subcategories
    def retrieve(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk, is_active=True)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # GET /api/v1/categories/{id}/products/ → List products under category with filters
    def products(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk, is_active=True)

        # 🔹 Example placeholder: adjust based on your Product model
        products_qs = category.products.filter(is_active=True)

        # Filters
        brand = request.query_params.get("brand")
        if brand:
            products_qs = products_qs.filter(brand__iexact=brand)

        price_min = request.query_params.get("price_min")
        if price_min:
            products_qs = products_qs.filter(price__gte=price_min)

        price_max = request.query_params.get("price_max")
        if price_max:
            products_qs = products_qs.filter(price__lte=price_max)

        color = request.query_params.get("color")
        if color:
            products_qs = products_qs.filter(color__iexact=color)

        size = request.query_params.get("size")
        if size:
            products_qs = products_qs.filter(size__iexact=size)

        # Sorting
        sort = request.query_params.get("sort")
        if sort:
            products_qs = products_qs.order_by(sort)

        # Pagination (simple manual example, or hook into DRF pagination)
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 10))
        start = (page - 1) * page_size
        end = start + page_size
        paginated = products_qs[start:end]

        # 🔹 Replace with your ProductSerializer
        data = [{"id": p.id, "name": p.name, "price": p.price} for p in paginated]

        return Response({
            "count": products_qs.count(),
            "page": page,
            "page_size": page_size,
            "results": data
        }, status=status.HTTP_200_OK)

🔗 Router (urls.py)

Since you’re using ViewSet, you’ll need to register custom routes (DRF doesn’t auto-detect products):

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # custom action for products inside category
    path("categories/<uuid:pk>/products/", CategoryViewSet.as_view({"get": "products"})),
]

urlpatterns += router.urls


👉 Now your endpoints work as:

GET /api/v1/categories/ → top-level categories with children.

GET /api/v1/categories/{id}/ → single category + subcategories.

GET /api/v1/categories/{id}/products/ → products inside category (with filters).

Do you want me to also add a ProductSerializer + model outline for the products endpoint so it’s fully working, or just keep it abstract like now?

ChatGPT can make mistakes. Che