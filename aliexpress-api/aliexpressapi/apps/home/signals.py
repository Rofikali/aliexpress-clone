# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from apps.home.models.section import HomepageSection
# from components.caching.cache_factory import get_cache
# from components.caching.invalidation import register_cache_invalidation

# home = get_cache("homepage")


# @receiver(post_save, sender=HomepageSection)
# @receiver(post_delete, sender=HomepageSection)
# def invalidate_sections_cache(sender, **kwargs):
#     # CACHE.clear_prefix("homepage")  # clears homepage:*
#     register_cache_invalidation("HomepageSection", "homepage")  # clears homepage:*



# #         # Register cache invalidation for Product model
# #         register_cache_invalidation(Product, "product")
