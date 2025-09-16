
# components/router/routers.py
import inspect
import pkgutil
import importlib
import re

from rest_framework.viewsets import ViewSetMixin, ViewSet
from rest_framework.routers import DefaultRouter


def auto_register_viewsets(
    router: DefaultRouter, module, prefix: str = None, case_style: str = "kebab"
) -> None:
    """
    Auto-discover and register all DRF ViewSets in a module or package.

    ✅ Production grade improvements:
    - Skips DRF's base ViewSet classes (ViewSet, GenericViewSet).
    - Respects __all__ if defined (explicit exports).
    - Works with both single `views.py` or `views/` package.
    - Allows optional `route_name` override in each ViewSet.
    - Supports kebab-case (default) or snake_case routes.
    - Prevents duplicate basename registration.

    Parameters
    ----------
    router : DefaultRouter
        DRF router instance.
    module : module
        The views module or package to scan.
    prefix : str, optional
        Prefix string for route names (e.g., "accounts").
    case_style : {"kebab", "snake"}, default "kebab"
        Naming style for routes.

    Example
    -------
        class ProductViewSet(ViewSet):
            pass
        # → /products/

        class AuthViewSet(ViewSet):
            route_name = "auth"
        # → /auth/
    """

    if hasattr(module, "__path__"):  # Package: views/
        for _, modname, _ in pkgutil.iter_modules(module.__path__):
            submodule = importlib.import_module(f"{module.__name__}.{modname}")
            _register_from_module(router, submodule, prefix, case_style)

    else:  # Single file: views.py
        _register_from_module(router, module, prefix, case_style)


def _register_from_module(
    router: DefaultRouter, module, prefix: str = None, case_style: str = "kebab"
) -> None:
    """
    Register eligible ViewSets from a single module.
    """

    # Only include explicitly exported names (if __all__ exists)
    names = getattr(module, "__all__", None) or [
        n for n in dir(module) if not n.startswith("_")
    ]

    for name in names:
        obj = getattr(module, name, None)

        if not inspect.isclass(obj):
            continue

        # Must be subclass of DRF ViewSet
        if not issubclass(obj, ViewSetMixin):
            continue

        # Skip DRF's abstract base classes
        if obj in (ViewSet, ViewSetMixin):
            continue

        # Use explicit route_name if defined
        route_name = getattr(obj, "route_name", None)
        if not route_name:
            base = _to_snake_case(name.replace("ViewSet", ""))
            route_name = _apply_case(base, case_style)

        # Apply global prefix if provided
        if prefix:
            prefix_case = _apply_case(prefix, case_style)
            route_name = f"{prefix_case}-{route_name}"

        # Prevent duplicate registrations
        if route_name in router.registry:
            raise RuntimeError(
                f"Duplicate ViewSet registration: '{route_name}' already exists. "
                f"Check your imports in {module.__name__}."
            )

        router.register(route_name, obj, basename=route_name)


def _to_snake_case(name: str) -> str:
    """Convert CamelCase → snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _apply_case(word: str, case_style: str) -> str:
    """Apply kebab-case or snake_case."""
    if case_style == "kebab":
        return word.replace("_", "-")
    return word
