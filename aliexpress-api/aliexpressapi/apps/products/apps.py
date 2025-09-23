from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"

    # from django.apps import AppConfig

    # class ProductsConfig(AppConfig):
    #     default_auto_field = "django.db.models.BigAutoField"
    #     name = "apps.products"

    def ready(self):
        from apps.products.models.product import Product
        from components.caching.invalidation import register_cache_invalidation

        # Register cache invalidation for Product model
        register_cache_invalidation(Product, "product")
