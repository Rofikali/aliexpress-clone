# import apps.products.views as views_pkg
from components.router.routers import auto_register_viewsets
import apps.products.views as views_pkg
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

# from apps.products.views.product import ProductsViewSet
# from apps.products.views.products_variants import ProductVariantViewSet
from apps.products.views.products_variants import ProductVariantViewSet
# from apps.products.views.product_attribute import ProductAttributeViewSet

# Root router
router = DefaultRouter()
auto_register_viewsets(router, views_pkg)

# Nested: product → variants
products_router = NestedDefaultRouter(router, "products", lookup="product")
products_router.register("variants", ProductVariantViewSet, basename="product-variants")

# Nested: variant → attributes
variants_router = NestedDefaultRouter(products_router, "variants", lookup="variant")
# variants_router.register(
#     "attributes", ProductAttributeViewSet, basename="product-variant-attributes"
# )

urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(variants_router.urls)),
]
