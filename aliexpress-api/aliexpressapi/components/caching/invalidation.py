from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from components.caching.cache_factory import get_cache


def register_cache_invalidation(model, namespace: str):
    """
    Auto-registers cache invalidation for a given model + cache namespace.

    Example:
        register_cache_invalidation(Product, "product")
    """

    cache = get_cache(namespace)

    @receiver(post_save, sender=model, weak=False)
    @receiver(post_delete, sender=model, weak=False)
    def clear_model_cache(sender, instance, **kwargs):
        """
        On create/update/delete → clear namespace cache.
        """
        cache.clear()
