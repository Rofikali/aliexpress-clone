from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from components.responses.response_factory import ResponseFactory
from apps.products.models.product_variant import ProductVariant
from apps.products.serializers.product_variants import (
    ProductVariantSerializer,
)

import os
import sys


class ProductVariantViewSet(ViewSet):
    def get_queryset(self, product_id=None):
        qs = ProductVariant.objects.all()
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

    @extend_schema(
        responses={200: ProductVariantSerializer(many=True)},
        tags=["Product Variants"],
        summary="List product variants",
    )
    # def list(self, request, product_pk=None):
    #     queryset = self.get_queryset(product_pk)
    #     serializer = ProductVariantSerializer(queryset, many=True)
    #     return ResponseFactory.success_resource(
    #         item=serializer.data,
    #         message="Product variants retrieved successfully.",
    #         status=status.HTTP_200_OK,
    #     )
    def list(self, request, product_pk=None):
        queryset = self.get_queryset(product_pk)
        serializer = ProductVariantSerializer(
            queryset, many=True, context={"request": request}
        )

        # Build available attributes & combination map
        available_attributes = {}
        combination_map = {}

        for variant in queryset:
            attrs = variant.attributes.all()

            # Build available attribute groups
            for attr_val in attrs:
                attr_id = str(attr_val.attribute.id)
                if attr_id not in available_attributes:
                    available_attributes[attr_id] = {
                        "name": attr_val.attribute.name,
                        "values": [],
                    }

                available_attributes[attr_id]["values"].append(
                    {"id": str(attr_val.value.id), "value": attr_val.value.value}
                )

            # Build combination key → variant id map
            key_parts = []
            for attr_val in attrs:
                key_parts.append(f"{attr_val.attribute.id}:{attr_val.value.id}")
            combination_key = "|".join(sorted(key_parts))
            combination_map[combination_key] = str(variant.id)

        # Remove duplicate values
        for k, attr in available_attributes.items():
            seen = set()
            unique = []
            for v in attr["values"]:
                if v["id"] not in seen:
                    unique.append(v)
                    seen.add(v["id"])
            attr["values"] = unique

        # 👉 final payload (Amazon/AliExpress style)
        final_payload = {
            "variants": serializer.data,
            "available_attributes": available_attributes,
            "combination_map": combination_map,
        }

        return ResponseFactory.success_resource(
            item=final_payload,
            message="Product variants fetched",
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        responses={200: ProductVariantSerializer},
        tags=["Product Variants"],
        summary="Retrieve single product variant",
    )
    def retrieve(self, request, pk=None, product_pk=None):
        variant = get_object_or_404(self.get_queryset(product_pk), id=pk)
        serializer = ProductVariantSerializer(variant)
        return ResponseFactory.success_resource(
            item=serializer.data,
            message="Product variant retrieved successfully.",
            status=status.HTTP_200_OK,
        )
