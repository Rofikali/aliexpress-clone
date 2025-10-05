from django.urls import include, path
from rest_framework.routers import DefaultRouter
import apps.home.views as views_pkg

from components.router.routers import auto_register_viewsets
# from apps.home.views.home import HomepageDetailViewSet

router = DefaultRouter()
auto_register_viewsets(router, views_pkg)


urlpatterns = [
    path("", include(router.urls)),
    # path("", include("homepage_router.urls")),
]
