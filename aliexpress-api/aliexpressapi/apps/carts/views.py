# # apps.cart_wishlist/viewsets.py
# from rest_framework.viewsets import ViewSet
# from rest_framework import status, permissions
# from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

# from .models import Cart, CartItem, Wishlist, WishlistItem
# from .serializers import (
#     CartSerializer,
#     CartItemSerializer,
#     WishlistSerializer,
#     WishlistItemSerializer,
# )

# from components.paginations.base_pagination import BaseCursorPagination
# # from components.responses.success import ResponseFactory
# # from components.responses.error import ErrorResponse
# from components.responses.response_factory import ResponseFactory
# from components.caching.cache_factory import get_cache


# # -------------------- CART --------------------
# class CartViewSet(ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     cache = get_cache("cart")

#     @extend_schema(
#         request=None,
#         responses={200: CartSerializer(many=True)},
#         tags=["Cart"],
#         summary="List carts of logged-in user",
#         description="Retrieve all carts belonging to the logged-in user (usually only one active).",
#     )
#     def list(self, request):
#         try:
#             user = request.user
#             cache_key = f"cart:user:{user.id}:list"

#             cached_data = self.cache.get(cache_key)
#             if cached_data:
#                 return ResponseFactory.success(
#                     body=cached_data,
#                     message="Carts fetched successfully",
#                     request=request,
#                     extra={"from_cache": True},
#                     status_code=status.HTTP_200_OK,
#                 )

#             queryset = Cart.objects.filter(user=user).order_by("-created_at")
#             serializer = CartSerializer(
#                 queryset, many=True, context={"request": request}
#             )

#             self.cache.set(cache_key, serializer.data, timeout=300)  # 5 min TTL

#             return ResponseFactory.success(
#                 body=serializer.data,
#                 message="Carts fetched successfully",
#                 request=request,
#                 status_code=status.HTTP_200_OK
#             )
#         except Exception as e:
#             return ResponseFactory.error(
#                 message="Failed to fetch carts",
#                 errors={"detail": str(e)},
#                 request=request,
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#     @extend_schema(
#         request=None,
#         responses={200: CartSerializer},
#         tags=["Cart"],
#         summary="Retrieve a single cart",
#         description="Retrieve cart details (with items) for logged-in user.",
#     )
#     def retrieve(self, request, pk=None):
#         try:
#             cache_key = f"cart:{pk}:user:{request.user.id}"
#             cached_data = self.cache.get(cache_key)
#             if cached_data:
#                 return ResponseFactory.send(
#                     body=cached_data,
#                     message="Cart fetched successfully",
#                     request=request,
#                     extra={"from_cache": True},
#                 )

#             cart = get_object_or_404(Cart, id=pk, user=request.user)
#             serializer = CartSerializer(cart, context={"request": request})

#             self.cache.set(cache_key, serializer.data, timeout=300)
#             return ResponseFactory.success(
#                 body=serializer.data,
#                 message="Cart fetched successfully",
#                 request=request,
#             )
#         except Exception as e:
#             return ResponseFactory.error(
#                 message="Cart not found", errors=str(e), request=request
#             )


# # -------------------- CART ITEMS --------------------
# class CartItemViewSet(ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional).",
#                 required=False,
#             ),
#         ],
#         responses={200: CartItemSerializer(many=True)},
#         tags=["Cart Items"],
#         summary="List cart items",
#         description="Retrieve all items inside the user's active cart with infinite scroll pagination.",
#     )
#     def list(self, request):
#         try:
#             cart = get_object_or_404(Cart, user=request.user, status="active")
#             queryset = CartItem.objects.filter(cart=cart).order_by("-added_at")

#             paginator = BaseCursorPagination()
#             page = paginator.paginate_queryset(queryset, request)
#             serializer = CartItemSerializer(
#                 page, many=True, context={"request": request}
#             )
#             response_data = paginator.get_paginated_response(serializer.data).data

#             return ResponseFactory.send(
#                 body=response_data,
#                 message="Cart items fetched successfully",
#                 request=request,
#             )
#         except Exception as e:
#             return ErrorResponse.send(
#                 message="Failed to fetch cart items", errors=str(e), request=request
#             )


# # -------------------- WISHLIST --------------------
# class WishlistViewSet(ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     cache = get_cache("wishlist")

#     @extend_schema(
#         responses={200: WishlistSerializer(many=True)},
#         tags=["Wishlist"],
#         summary="List wishlists of logged-in user",
#         description="Retrieve all wishlists belonging to the logged-in user.",
#     )
#     def list(self, request):
#         try:
#             user = request.user
#             cache_key = f"wishlist:user:{user.id}:list"
#             cached_data = self.cache.get(cache_key)

#             if cached_data:
#                 return ResponseFactory.send(
#                     body=cached_data,
#                     message="Wishlists fetched successfully",
#                     request=request,
#                     extra={"from_cache": True},
#                 )

#             queryset = Wishlist.objects.filter(user=user).order_by("-created_at")
#             serializer = WishlistSerializer(
#                 queryset, many=True, context={"request": request}
#             )

#             self.cache.set(cache_key, serializer.data, timeout=600)  # 10 min TTL

#             return ResponseFactory.send(
#                 body=serializer.data,
#                 message="Wishlists fetched successfully",
#                 request=request,
#             )
#         except Exception as e:
#             return ErrorResponse.send(
#                 message="Failed to fetch wishlists", errors=str(e), request=request
#             )


# # -------------------- WISHLIST ITEMS --------------------
# class WishlistItemViewSet(ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     @extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 name="cursor",
#                 type=OpenApiTypes.STR,
#                 location=OpenApiParameter.QUERY,
#                 description="Cursor for pagination (optional).",
#                 required=False,
#             ),
#         ],
#         responses={200: WishlistItemSerializer(many=True)},
#         tags=["Wishlist Items"],
#         summary="List wishlist items",
#         description="Retrieve all items inside a user's wishlist with infinite scroll pagination.",
#     )
#     def list(self, request):
#         try:
#             wishlist = get_object_or_404(Wishlist, user=request.user)
#             queryset = WishlistItem.objects.filter(wishlist=wishlist).order_by(
#                 "-added_at"
#             )

#             paginator = InfiniteScrollPagination()
#             page = paginator.paginate_queryset(queryset, request)
#             serializer = WishlistItemSerializer(
#                 page, many=True, context={"request": request}
#             )
#             response_data = paginator.get_paginated_response(serializer.data).data

#             return ResponseFactory.send(
#                 body=response_data,
#                 message="Wishlist items fetched successfully",
#                 request=request,
#             )
#         except Exception as e:
#             return ErrorResponse.send(
#                 message="Failed to fetch wishlist items", errors=str(e), request=request
#             )


# apps/cart/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.products.models import ProductVariant


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user, is_active=True)

    def get_object(self):
        """Ensure user always gets their active cart."""
        cart, created = Cart.objects.get_or_create(
            user=self.request.user, is_active=True
        )
        return cart

    def list(self, request):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    # 🛒 Add item to cart
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_object()
        product_variant_id = request.data.get("product_variant_id")
        quantity = int(request.data.get("quantity", 1))

        variant = get_object_or_404(ProductVariant, id=product_variant_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={
                "price": variant.price,
                "discount_price": variant.discount_price or None,
            },
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 🧮 Update item quantity
    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        cart = self.get_object()
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # 🗑️ Remove item
    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        cart = self.get_object()
        item_id = request.data.get("item_id")

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data)
