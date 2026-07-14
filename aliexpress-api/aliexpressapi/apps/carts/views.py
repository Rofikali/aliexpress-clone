# from rest_framework.viewsets import ViewSet
# from rest_framework.permissions import AllowAny
# from rest_framework import status
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# from apps.carts.services.cart_service import CartService
# from apps.carts.repositories.cart_repository import CartRepository
# from apps.carts.serializers.cart import CartSerializer
# from components.responses.response_factory import ResponseFactory
# from components.caching.cache_factory import get_cache
# from apps.carts.utils.session import get_or_create_cart_session_id
# from rest_framework.decorators import action

# class CartViewSet(ViewSet):
#     permission_classes = [AllowAny]
#     cache = get_cache("cart")

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.service = CartService(CartRepository())

#     def get_cart(self, request):
#         session_id = None

#         if not request.user.is_authenticated:
#             session_id = get_or_create_cart_session_id(request)

#         return self.service.get_cart(
#             user=request.user,
#             session_id=session_id,
#         )

#     @extend_schema(tags=["Cart"], responses={200: CartSerializer})
#     def list(self, request):
#         cart = self.get_cart(request)
#         serializer = CartSerializer(cart, context={"request": request})
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Active cart fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     @extend_schema(
#         parameters=[
#             OpenApiParameter("product_variant_id", OpenApiTypes.UUID),
#             OpenApiParameter("quantity", OpenApiTypes.INT, required=False),
#         ],
#         responses={201: CartSerializer},
#         tags=["Cart"],
#     )

#     @action(detail=False, methods=["post"])
#     def add_item(self, request):
#         cart = self.get_cart(request)
#         self.service.add_item(
#             cart=cart,
#             variant_id=request.data["product_variant_id"],
#             quantity=int(request.data.get("quantity", 1)),
#         )
#         serializer = CartSerializer(cart, context={"request": request})
#         return ResponseFactory.success_resource(
#             item=serializer.data,
#             message="Item added to cart successfully",
#             status=status.HTTP_201_CREATED,
#             request=request,
#         )


# carts/views/cart_viewset.py

from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.carts.services.cart_service import CartService
from apps.carts.repositories.cart_repository import CartRepository
from apps.carts.serializers.cart import CartSerializer
from components.responses.response_factory import ResponseFactory
from apps.carts.utils.session import get_or_create_cart_session_id


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CartService(CartRepository())

    def get_cart(self, request):
        session_id = None
        if not request.user.is_authenticated:
            session_id = get_or_create_cart_session_id(request)

        return self.service.get_cart(
            user=request.user,
            session_id=session_id,
        )

    @extend_schema(tags=["Cart"], responses={200: CartSerializer})
    def list(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Active cart fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    @extend_schema(
        tags=["Cart"],
        parameters=[
            OpenApiParameter("product_variant_id", OpenApiTypes.UUID),
            OpenApiParameter("quantity", OpenApiTypes.INT),
        ],
        responses={201: CartSerializer},
    )
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        if "product_variant_id" not in request.data:
            return ResponseFactory.error(
                message="product_variant_id is required",
                status=status.HTTP_400_BAD_REQUEST,
                request=request,
            )

        cart = self.get_cart(request)

        self.service.add_item(
            cart=cart,
            variant_id=request.data["product_variant_id"],
            quantity=int(request.data.get("quantity", 1)),
        )

        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Item added to cart successfully",
            status=status.HTTP_201_CREATED,
            request=request,
        )
