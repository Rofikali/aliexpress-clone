from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        from apps.home.models.section import HomepageSection
        from components.caching.invalidation import register_cache_invalidation

        # Register cache invalidation for Product model
        register_cache_invalidation(HomepageSection, "homepage")
