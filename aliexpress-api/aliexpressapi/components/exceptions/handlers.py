# # components/exceptions/handlers.py

# from rest_framework.views import exception_handler
# from components.responses.response_factory import ResponseFactory


# def custom_exception_handler(exc, context):
#     """
#     Wrap DRF & Django exceptions in your ResponseFactory format.
#     """
#     # Let DRF build the standard response first
#     response = exception_handler(exc, context)

#     if response is not None:
#         # Standardize error format
#         return ResponseFactory.error(
#             message=str(exc),
#             errors=response.data,
#             request=context.get("request"),
#             status=response.status_code,
#         )

#     # If DRF didn’t handle it (like middleware rejections)
#     return ResponseFactory.error(
#         message="Unhandled error",
#         errors={"detail": str(exc)},
#         request=context.get("request"),
#         status=500,
#     )


# components/exceptions/custom_exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
)
from components.responses.response_factory import ResponseFactory


def custom_exception_handler(exc, context):
    print("🔥 Custom Exception Handler CALLED with:", exc)  # debug log
    """
    Override DRF default exception handler
    so all errors go through ResponseFactory.
    """
    # Let DRF generate the base response
    response = exception_handler(exc, context)

    # Extract request (needed for tracing info)
    request = context.get("request")

    if response is not None:
        status_code = response.status_code

        # Handle ValidationError separately (common in serializers)
        if isinstance(exc, ValidationError):
            errors = []
            for field, messages in exc.detail.items():
                for msg in messages:
                    errors.append({"code": field.upper(), "message": str(msg)})
            return ResponseFactory.error(
                message="Validation failed",
                errors=errors,
                status=status_code,
                request=request,
            )

        # Handle Auth errors
        if isinstance(exc, (AuthenticationFailed, NotAuthenticated, PermissionDenied)):
            return ResponseFactory.error(
                message=str(exc),
                errors=[{"code": "AUTH_ERROR", "message": str(exc)}],
                status=status_code,
                request=request,
            )

        # Fallback: normalize other DRF errors
        return ResponseFactory.error(
            message=str(exc),
            errors=[{"code": "ERROR", "message": str(exc)}],
            status=status_code,
            request=request,
        )

    # If DRF couldn’t handle it (likely 500s)
    return ResponseFactory.error(
        message="Internal server error",
        errors=[{"code": "SERVER_ERROR", "message": str(exc)}],
        status=500,
        request=request,
    )
