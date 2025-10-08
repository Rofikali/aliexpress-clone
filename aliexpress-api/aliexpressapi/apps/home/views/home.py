# apps/home/views/home_viewset.py
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema

from components.caching.cache_factory import get_cache
from components.responses.response_factory import ResponseFactory

CACHE = get_cache("homepage")  # use your existing cache factory


# class HomepageViewSet(viewsets.ViewSet):
#     """
#     Return a list of active homepage sections (cached).
#     """

#     @extend_schema(
#         responses={200: HomepageSectionSerializer(many=True)},
#         tags=["Homepage"],
#         summary="Get homepage sections",
#     )
#     def list(self, request):
#         qs = HomepageSection.objects.filter(is_active=True).prefetch_related(
#             "banners",
#             "products__product",
#             "categories__category",
#             "promotions",  # ✅ added
#         )

#         serializer = HomepageSectionSerializer(
#             qs, many=True, context={"request": request}
#         )
#         data = serializer.data
#         return ResponseFactory.success_collection(
#             items=data,
#             pagination={},
#             message="Homepage sections",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         responses={200: HomepageSectionSerializer},
#         tags=["Homepage"],
#         summary="Retrieve single homepage section",
#     )
#     def retrieve(self, request, pk=None):
#         section = get_object_or_404(
#             HomepageSection.objects.prefetch_related(
#                 "banners",
#                 "products__product",
#                 "categories__category",
#                 "promotions",  # ✅ added
#             ),
#             pk=pk,
#             is_active=True,
#         )
#         serializer = HomepageSectionSerializer(section, context={"request": request})
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Homepage section retrieved",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         responses={200: HomepageSectionSerializer},
#         tags=["Homepage"],
#         summary="Retrieve homepage Banner, Products and Promotions section",
#     )
#     @action(
#         detail=False,
#         methods=["get"],
#         url_path="featured",
#     )
#     def featured(self, request):
#         sections = (
#             HomepageSection.objects.filter(
#                 is_active=True,
#                 type__in=["banner", "product_carousel", "promo"],  # ✅ include promo
#             ).prefetch_related("banners", "products__product", "promotions")  # ✅ added
#         )

#         serializer = HomepageSectionSerializer(
#             sections, many=True, context={"request": request}
#         )
#         data = serializer.data
#         return ResponseFactory.success_collection(
#             items=data,
#             pagination={},
#             message="Featured homepage content",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

from drf_spectacular.utils import OpenApiResponse
from apps.home.serializers.banner_serializer import HomepageBannerSerializer

# from apps.home.serializers.category_serializer import HomepageCategorySerializer
from apps.home.serializers.product_serializer import HomepageProductSerializer
from apps.home.serializers.promotion_serializer import HomepagePromotionSerializer

from apps.home.models.banner import HomepageBanner

# from apps.home.models.category import HomepageCategory
# from apps.home.models.product import HomepageProduct

from apps.home.models.promotion import HomepagePromotion


from apps.products.models.category import Category
from apps.products.models.product import Product
from apps.products.serializers.category import CategorySerializer
from apps.products.serializers.product import ProductSerializer


class HomepageViewSet(viewsets.ViewSet):
    """
    Aggregated homepage data for frontend (like Amazon/Flipkart).
    """

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Aggregated homepage data",
            )
        },
        tags=["Homepage"],
        summary="Get homepage aggregated content",
    )
    def list(self, request):
        # Fetch active items
        banners = HomepageBanner.objects.filter(is_active=True).order_by("sort_order")
        # categories = HomepageCategory.objects.select_related("category").order_by(
        #     "sort_order"
        # )
        categories = Category.objects.all().order_by("name")[:5]
        featured_products = Product.objects.all().order_by("-created_at")[:7]
        promotions = HomepagePromotion.objects.filter(is_active=True).order_by(
            "sort_order"
        )

        # Serialize
        data = {
            "banners": HomepageBannerSerializer(
                banners, many=True, context={"request": request}
            ).data,
            "categories": CategorySerializer(
                categories, many=True, context={"request": request}
            ).data,
            "featured_products": ProductSerializer(
                featured_products, many=True, context={"request": request}
            ).data,
            "promotions": HomepagePromotionSerializer(
                promotions, many=True, context={"request": request}
            ).data,
        }

        return ResponseFactory.success_resource(
            item=data,
            message="Homepage aggregated content",
            status=status.HTTP_200_OK,
            request=request,
        )
