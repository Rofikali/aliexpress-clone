# components/exceptions/handlers.py

from rest_framework.views import exception_handler
from components.responses.response_factory import ResponseFactory


def custom_exception_handler(exc, context):
    """
    Wrap DRF & Django exceptions in your ResponseFactory format.
    """
    # Let DRF build the standard response first
    response = exception_handler(exc, context)

    if response is not None:
        # Standardize error format
        return ResponseFactory.error(
            message=str(exc),
            errors=response.data,
            request=context.get("request"),
            status=response.status_code,
        )

    # If DRF didn’t handle it (like middleware rejections)
    return ResponseFactory.error(
        message="Unhandled error",
        errors={"detail": str(exc)},
        request=context.get("request"),
        status=500,
    )
