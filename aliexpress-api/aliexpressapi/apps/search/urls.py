# from django.urls import path
# from .views import SearchUserAPIView

# urlpatterns = [
#     path('search-users', SearchUserAPIView.as_view(), name='search-users'),
# ]
# from rest_framework.routers import DefaultRouter
# from django.urls import path, include

# Create and register router for the PostViewSet
# router = DefaultRouter()
# router.register(r'search', SearchUserAPIView, basename='search-users')

# # # Combine the manual URLs and router-generated URLs
# # urlpatterns += router.urls


# # Define your URL patterns
# urlpatterns = [
#     #     path('user/logged-in/', LoggedInUser.as_view(), name='logged_in_user'),
#     # pass
#     path('search/', include(router.urls)),
# ]
# # urlpatterns += router.urls


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

# # router.register(r"productlist", views.ProductListViewSet, basename="productlist")

# urlpatterns = [
#     # Register the routes under '/api/mod5/'
#     path("", include(router.urls)),
#     # Manually add the custom path for DynamicCategoryURLFilterViewSet
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
