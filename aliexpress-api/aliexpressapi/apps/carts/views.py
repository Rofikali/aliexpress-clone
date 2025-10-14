# apps/cart/views.py
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from components.caching.cache_factory import get_cache
from apps.carts.serializers.cart import CartSerializer
from apps.products.models.product_variant import ProductVariant
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from components.responses.response_factory import ResponseFactory


# class CartViewSet(viewsets.ModelViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()

#     def get_queryset(self):
#         user = self.request.user
#         return Cart.objects.filter(user=user, is_active=True)

#     def get_object(self):
#         """Ensure user always gets their active cart."""
#         cart, created = Cart.objects.get_or_create(
#             user=self.request.user, is_active=True
#         )

#     def list(self, request):
#         cart = self.get_object()
#         serializer = self.get_serializer(cart)
#         # return Response(serializer.data)
#         return ResponseFactory.success_collection(
#             items=serializer.data,
#             message="all carts fetched successfully",
#             status=status.HTTP_200_OK,
#             request=request,
#         )

#     # 🛒 Add item to cart
#     @action(detail=False, methods=["post"])
#     def add_item(self, request):
#         cart = self.get_object()
#         product_variant_id = request.data.get("product_variant_id")
#         quantity = int(request.data.get("quantity", 1))

#         variant = get_object_or_404(ProductVariant, id=product_variant_id)

#         item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             product_variant=variant,
#             defaults={
#                 "price": variant.price,
#                 "discount_price": variant.discount_price or None,
#             },
#         )

#         if not created:
#             item.quantity += quantity
#             item.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # 🧮 Update item quantity
#     @action(detail=False, methods=["patch"])
#     def update_item(self, request):
#         cart = self.get_object()
#         item_id = request.data.get("item_id")
#         quantity = int(request.data.get("quantity", 1))

#         item = get_object_or_404(CartItem, id=item_id, cart=cart)
#         item.quantity = quantity
#         item.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

#     # 🗑️ Remove item
#     @action(detail=False, methods=["delete"])
#     def remove_item(self, request):
#         cart = self.get_object()
#         item_id = request.data.get("item_id")

#         item = get_object_or_404(CartItem, id=item_id, cart=cart)
#         item.delete()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

# apps/cart/views.py
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny


class CartViewSet(ViewSet):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    cache = get_cache("cart")

    def get_object(self, request):
        """Ensure the user always has an active cart."""
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        return cart

    # 🛍️ List Cart (GET /cart/)
    # @extend_schema(
    #     responses={200: CartSerializer},
    #     tags=["Cart"],
    #     summary="Retrieve Active Cart",
    #     description="Fetch the active cart of the logged-in user.",
    # )
    @extend_schema(
        tags=["Cart"],
        summary="Retrieve Active Cart",
        description="Fetch the active cart of the logged-in or guest user.",
        responses={200: CartSerializer},
        # security=[{"BearerAuth": []}],
    )
    def list(self, request):
        cart = self.get_object(request)
        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Active cart fetched successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    # 🛒 Add Item (POST /cart/add_item/)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "product_variant_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Product variant ID",
            ),
            OpenApiParameter(
                "quantity",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Quantity to add",
                required=False,
            ),
        ],
        responses={201: CartSerializer},
        tags=["Cart"],
        summary="Add Item to Cart",
        description="Add a product variant to the user's active cart.",
    )
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_object(request)
        product_variant_id = request.data.get("product_variant_id")
        quantity = int(request.data.get("quantity", 1))

        variant = get_object_or_404(ProductVariant, id=product_variant_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={
                "price": variant.price,
                "discount_price": variant.discount_price or None,
                "quantity": quantity,
            },
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Item added to cart successfully",
            status=status.HTTP_201_CREATED,
            request=request,
        )

    # 🔁 Update Item Quantity (PATCH /cart/update_item/)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "item_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Cart item ID",
            ),
            OpenApiParameter(
                "quantity",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="New quantity",
            ),
        ],
        responses={200: CartSerializer},
        tags=["Cart"],
        summary="Update Cart Item Quantity",
        description="Change the quantity of a specific item in the cart.",
    )
    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        cart = self.get_object(request)
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.quantity = quantity
        item.save()

        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Cart item updated successfully",
            status=status.HTTP_200_OK,
            request=request,
        )

    # ❌ Remove Item (DELETE /cart/remove_item/)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "item_id",
                OpenApiTypes.INT,
                OpenApiParameter.QUERY,
                description="Cart item ID to remove",
            ),
        ],
        responses={200: CartSerializer},
        tags=["Cart"],
        summary="Remove Cart Item",
        description="Remove a product variant from the user's cart.",
    )
    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        cart = self.get_object(request)
        item_id = request.data.get("item_id")

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        serializer = CartSerializer(cart, context={"request": request})
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Item removed from cart successfully",
            status=status.HTTP_200_OK,
            request=request,
        )
