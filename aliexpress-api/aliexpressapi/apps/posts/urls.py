from inspect import getmembers, isclass

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ViewSet

from . import views

router = DefaultRouter()

# Automatically find all ViewSets in views.py and register them
for name, cls in getmembers(views, isclass):
    if issubclass(cls, ViewSet) and cls.__module__ == views.__name__:
        router.register(
            rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
        )

# router.register(r"productlist", views.ProductListViewSet, basename="productlist")

urlpatterns = [
    # Register the routes under '/api/mod5/'
    path("", include(router.urls)),
    # Manually add the custom path for DynamicCategoryURLFilterViewSet
]
