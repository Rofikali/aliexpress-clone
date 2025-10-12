from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as views_pkg

from components.router.routers import auto_register_viewsets

router = DefaultRouter()
auto_register_viewsets(router, views_pkg)

urlpatterns = [
    path("", include(router.urls)),
]
