# # from dataclasses import dataclass
# # from contextlib import contextmanager

# # # from apps.products.models import ProductVariant
# # from apps.products.models.product_variant import ProductVariant
# # from apps.products.utils.attributes import (
# #     build_available_attributes,
# #     build_combination_map,
# # )


# # @dataclass
# # class VariantDataBundle:
# #     variants: list
# #     available_attributes: dict
# #     combination_map: dict


# # class VariantService:
# #     """Business logic separated from Django layers."""

# #     @staticmethod
# #     @contextmanager
# #     def fetch_variants(product_id: str):
# #         """
# #         Context manager ensures clean DB query scope.
# #         Good for logging, measuring, error catching.
# #         """
# #         try:
# #             qs = (
# #                 ProductVariant.objects.filter(product_id=product_id, is_active=True)
# #                 .select_related("image")
# #                 .prefetch_related(
# #                     "attributes",
# #                     "attributes__attribute",
# #                     "attributes__value",
# #                 )
# #             )
# #             yield qs
# #         except Exception as e:
# #             raise e

# #     @staticmethod
# #     def build_response_data(variants):
# #         """Builds UI-ready structured data."""
# #         return VariantDataBundle(
# #             variants=variants,
# #             available_attributes=build_available_attributes(variants),
# #             combination_map=build_combination_map(variants),
# #         )


# from __future__ import annotations
# from dataclasses import dataclass
# from contextlib import contextmanager
# from typing import Iterable, List, Dict, Any, Optional
# from decimal import Decimal, InvalidOperation

# from django.db.models.query import QuerySet

# from apps.products.models.product_variant import ProductVariant, ProductVariantValue
# from apps.products.models.product_attribute import ProductAttributeValue
# from components.caching.cache_factory import get_cache


# @dataclass
# class VariantDataBundle:
#     """
#     DTO returned by VariantService.build_response_data
#     - variants: list[ProductVariant] (model instances)
#     - available_attributes: dict mapping attribute_id -> { attribute_id, attribute_name, values: [{value_id, value}] }
#     - combination_map: dict (canonical_key -> variant_id)
#     """

#     variants: List[ProductVariant]
#     available_attributes: Dict[str, Any]
#     combination_map: Dict[str, str]


# class VariantService:
#     """
#     Business logic for product variants.
#     Responsibilities:
#       - provide a safe DB query scope (context manager)
#       - build UI-friendly data structures:
#          available_attributes (unique values per attribute)
#          combination_map (deterministic sorted key -> variant id)
#       - normalize numeric fields to Python primitives for safe comparisons
#       - small cache helpers (uses your get_cache factory)
#     """

#     CACHE_NAMESPACE = (
#         "product_variants"  # used with get_cache(CACHE_NAMESPACE, product_pk)
#     )

#     # -------------------------
#     # Context manager: fetch variants queryset with required prefetches
#     # -------------------------
#     @staticmethod
#     @contextmanager
#     def fetch_variants(product_id: str) -> Iterable[QuerySet]:
#         """
#         Yields a queryset of ProductVariant objects prefetching related attributes and values.
#         Use like:
#             with VariantService.fetch_variants(product_id) as qs:
#                 page = paginator.paginate_queryset(qs, request)
#         """
#         try:
#             qs = (
#                 ProductVariant.objects.filter(product_id=product_id)
#                 .select_related("image")  # image is FK to ProductImages
#                 .prefetch_related(
#                     # prefetch ProductVariantValue objects and their attribute & value FKs
#                     "attributes",  # uses related_name="attributes"
#                     "attributes__attribute",
#                     "attributes__value",
#                 )
#             )
#             yield qs
#         except Exception:
#             # allow outer handlers to catch; keep context manager minimal
#             raise

#     # -------------------------
#     # Normalization helpers
#     # -------------------------
#     @staticmethod
#     def _safe_decimal_to_float(value: Optional[Decimal]) -> Optional[float]:
#         """Convert Decimal to float or return None safely."""
#         if value is None:
#             return None
#         if isinstance(value, (float, int)):
#             return float(value)
#         try:
#             return float(value)
#         except (InvalidOperation, ValueError, TypeError):
#             try:
#                 return float(str(value))
#             except Exception:
#                 return None

#     @staticmethod
#     def _normalize_variant_numeric_fields(variant: ProductVariant) -> Dict[str, Any]:
#         """
#         Return a dict with stabilized numeric types for a variant.
#         We do *not* mutate the model instance.
#         """
#         return {
#             "id": str(variant.id),
#             "sku": variant.sku,
#             "price": VariantService._safe_decimal_to_float(variant.price),
#             "discount_price": VariantService._safe_decimal_to_float(
#                 variant.discount_price
#             ),
#             "currency": variant.currency,
#             "stock": int(variant.stock) if variant.stock is not None else None,
#             "is_active": bool(variant.is_active),
#         }

#     # -------------------------
#     # Attribute builders
#     # -------------------------
#     @staticmethod
#     def build_available_attributes(
#         variants: Iterable[ProductVariant],
#     ) -> Dict[str, Any]:
#         """
#         Build available_attributes map:
#         {
#           attribute_id: {
#             "attribute_id": str,
#             "attribute_name": str,
#             "values": [ {"value_id": str, "value": str}, ... ]
#           },
#           ...
#         }

#         Implementation uses sets to deduplicate and converts to lists deterministically.
#         """
#         result: Dict[str, Dict[str, Any]] = {}

#         for v in variants:
#             # attributes are ProductVariantValue instances prefetched via "attributes"
#             for av in getattr(v, "attributes", []) or []:
#                 attr = getattr(av, "attribute", None)
#                 val = getattr(av, "value", None)
#                 if not attr or not val:
#                     continue
#                 aid = str(attr.id)
#                 vid = str(val.id)
#                 vstr = str(val.value)

#                 entry = result.setdefault(
#                     aid,
#                     {"attribute_id": aid, "attribute_name": attr.name, "values": set()},
#                 )
#                 entry["values"].add((vid, vstr))

#         # convert sets to sorted lists (deterministic order)
#         out: Dict[str, Any] = {}
#         for aid, meta in result.items():
#             values_list = sorted(
#                 list(meta["values"]), key=lambda t: (t[1].lower(), t[0])
#             )  # sort by value string, fallback id
#             out[aid] = {
#                 "attribute_id": aid,
#                 "attribute_name": meta["attribute_name"],
#                 "values": [{"id": vid, "value": vstr} for (vid, vstr) in values_list],
#             }
#         return out

#     @staticmethod
#     def build_combination_map(variants: Iterable[ProductVariant]) -> Dict[str, str]:
#         """
#         Build deterministic combination_map:
#           "attrId:valId|attrId:valId" (attributes sorted by attribute id) -> variant_id

#         Always return string keys (no mixing types).
#         """
#         combo: Dict[str, str] = {}

#         for v in variants:
#             pairs: List[str] = []
#             for av in getattr(v, "attributes", []) or []:
#                 # attribute_id and value_id may be UUID, cast to str
#                 pairs.append(f"{str(av.attribute_id)}:{str(av.value_id)}")

#             # sort pairs by attribute id string to guarantee canonical key order
#             key = "|".join(sorted(pairs, key=lambda x: x.split(":", 1)[0]))
#             # store mapping
#             combo[key] = str(v.id)

#         return combo

#     # -------------------------
#     # High level builder: build response DTO
#     # -------------------------
#     @staticmethod
#     def build_response_data(variants: Iterable[ProductVariant]) -> VariantDataBundle:
#         """
#         Build VariantDataBundle with:
#           - variants: list(model instances) (we keep instances to let serializer handle full fields)
#           - available_attributes: dict as described
#           - combination_map: dict mapping canonical key -> variant_id
#         """
#         # ensure we have a list to iterate multiple times
#         variant_list = list(variants)

#         available_attributes = VariantService.build_available_attributes(variant_list)
#         combination_map = VariantService.build_combination_map(variant_list)

#         return VariantDataBundle(
#             variants=variant_list,
#             available_attributes=available_attributes,
#             combination_map=combination_map,
#         )

#     # -------------------------
#     # Cache helpers (best-effort, uses your get_cache factory)
#     # -------------------------
#     @staticmethod
#     def cache_key(product_id: str, cursor: str = "first") -> str:
#         return f"product:{product_id}:variants:{cursor}"

#     @staticmethod
#     def get_cache_for_product(product_id: str):
#         """
#         Returns your cache instance for this product.
#         This assumes components.caching.cache_factory.get_cache(namespace, product_id) signature.
#         """
#         return get_cache(VariantService.CACHE_NAMESPACE, product_id)

#     @staticmethod
#     def read_cache(product_id: str, cursor: str = "first") -> Optional[Dict[str, Any]]:
#         cache = VariantService.get_cache_for_product(product_id)
#         key = VariantService.cache_key(product_id, cursor)
#         try:
#             return cache.get_results(key)
#         except TypeError:
#             # if cache API only accepts single arg etc., call with key
#             return cache.get_results(key)

#     @staticmethod
#     def write_cache(product_id: str, data: Dict[str, Any], cursor: str = "first"):
#         cache = VariantService.get_cache_for_product(product_id)
#         key = VariantService.cache_key(product_id, cursor)
#         try:
#             return cache.cache_results(key, data)
#         except TypeError:
#             return cache.cache_results(key, data)

#     @staticmethod
#     def invalidate_cache(product_id: str):
#         """
#         Best-effort cache invalidation. Your cache class may expose special methods;
#         implement more efficient invalidation if possible.
#         """
#         cache = VariantService.get_cache_for_product(product_id)
#         # try to remove common keys
#         try:
#             if hasattr(cache, "delete"):
#                 # delete typical keys — you might have many cursors; production: implement prefix invalidation
#                 cache.delete(VariantService.cache_key(product_id, "first"))
#             elif hasattr(cache, "invalidate_prefix"):
#                 cache.invalidate_prefix(f"product:{product_id}:variants:")
#             else:
#                 # fallback: overwrite with empty structure
#                 cache.cache_results(VariantService.cache_key(product_id, "first"), None)
#         except Exception:
#             # best-effort only
#             pass

# services/product_variant_service.py

# from dataclasses import dataclass
from typing import List
from django.db import transaction
from apps.products.models.product import Product
from dataclasses import dataclass
# from contextlib import contextmanager
# from typing import Iterable, List, Dict, Any, Optional
# from decimal import Decimal, InvalidOperation

# from django.db.models.query import QuerySet

from apps.products.models.product_variant import ProductVariant, ProductVariantValue
from apps.products.models.product_attribute import ProductAttributeValue
from components.caching.cache_factory import get_cache

@dataclass
class VariantAttributeDTO:
    attribute_id: str
    attribute_name: str
    value_id: str
    value: str


@dataclass
class VariantDTO:
    id: str
    sku: str
    price: float
    discount_price: float | None
    stock: int
    currency: str
    image: str | None
    attributes: List[VariantAttributeDTO]


class SafeDB:
    """Context manager for safe DB execution with rollback."""

    def __enter__(self):
        self.tx = transaction.atomic()
        self.tx.__enter__()
        return self

    def __exit__(self, exc_type, *_):
        return self.tx.__exit__(exc_type, *_)


class ProductVariantService:
    @staticmethod
    def list_product_variants(product_id: str) -> List[VariantDTO]:
        with SafeDB():  # Safe & rollback protected
            product = Product.objects.only("id").get(id=product_id)

            variants = (
                ProductVariant.objects.filter(product=product, is_active=True)
                .select_related("image")
                .prefetch_related("attributes__attribute", "attributes__value")
                .order_by("created_at")
            )

            result = []

            for variant in variants:
                attrs = []
                for pav in variant.attributes.all():  # ✔ No RelatedManager bug
                    attrs.append(
                        VariantAttributeDTO(
                            attribute_id=str(pav.attribute.id),
                            attribute_name=pav.attribute.name,
                            value_id=str(pav.value.id),
                            value=pav.value.value,
                        )
                    )

                result.append(
                    VariantDTO(
                        id=str(variant.id),
                        sku=variant.sku,
                        price=float(variant.price),
                        discount_price=float(variant.discount_price)
                        if variant.discount_price
                        else None,
                        stock=variant.stock,
                        currency=variant.currency,
                        image=variant.image.image.url if variant.image else None,
                        attributes=attrs,
                    )
                )

            return result
