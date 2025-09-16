# # apps.products.urls.py
# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# import apps.products.views as views_pkg

# from components.router.routers import auto_register_viewsets

# router = DefaultRouter()
# auto_register_viewsets(router, views_pkg)

# urlpatterns = [
#     path("", include(router.urls)),
# ]


# # apps/products/urls.py
# from django.urls import include, path
# from rest_framework_nested.routers import NestedDefaultRouter
# from rest_framework.routers import DefaultRouter

# import apps.products.views as views_pkg
# from components.router.routers import auto_register_viewsets

# # main router
# router = DefaultRouter()
# auto_register_viewsets(router, views_pkg)

# # nested router for variants under products
# # from apps.products.views.products_variants_view import ProductVariantViewSet
# from apps.products.views.products_variants_view import ProductVariantViewSet

# products_router = NestedDefaultRouter(router, "products", lookup="product")
# products_router.register("variants", ProductVariantViewSet, basename="product-variants")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("", include(products_router.urls)),
# ]

# # apps/products/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

import apps.products.views as views_pkg
from components.router.routers import auto_register_viewsets

# ---------------- Base router ----------------
router = DefaultRouter()
auto_register_viewsets(router, views_pkg)

# ---------------- Nested: Variants under Products ----------------
# from apps.products.viewsets.product_variants_view import ProductVariantViewSet
from apps.products.views.products_variants_view import ProductVariantViewSet

products_router = NestedDefaultRouter(router, "products", lookup="product")
products_router.register("variants", ProductVariantViewSet, basename="product-variants")

# ---------------- Nested: Attributes under Variants ----------------
from apps.products.views.product_attribute_view import ProductAttributeViewSet

variants_router = NestedDefaultRouter(products_router, "variants", lookup="variant")
variants_router.register(
    "attributes", ProductAttributeViewSet, basename="product-attributes"
)

# ---------------- URL patterns ----------------
urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
    path("", include(variants_router.urls)),
]
