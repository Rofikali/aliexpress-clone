# # module4/urls.py
# from inspect import getmembers, isclass

# from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from rest_framework.viewsets import ViewSet

# from . import views

# router = DefaultRouter()

# # Automatically find all ViewSets in views.py and register them
# for name, cls in getmembers(views, isclass):
#     if issubclass(cls, ViewSet) and cls.__module__ == views.__name__:
#         router.register(
#             rf"{name.lower().replace('viewset', '')}", cls, basename=name.lower()
#         )

# urlpatterns = [
#     path("", include(router.urls)),  # Register the routes under '/api/products/'
# ]


from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as views_pkg

from components.router.routers import auto_register_viewsets

router = DefaultRouter()
auto_register_viewsets(router, views_pkg)

urlpatterns = [
    path("", include(router.urls)),
]
