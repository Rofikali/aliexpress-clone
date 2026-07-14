import logging

from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.views import exception_handler

from components.responses.response_factory import ResponseFactory


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get("request")

    if response is not None:
        status_code = response.status_code

        if isinstance(exc, ValidationError):
            errors = []
            for field, messages in exc.detail.items():
                for message in messages:
                    errors.append({"code": field.upper(), "message": str(message)})
            return ResponseFactory.error(
                message="Validation failed",
                errors=errors,
                status=status_code,
                request=request,
            )

        if isinstance(exc, (AuthenticationFailed, NotAuthenticated, PermissionDenied)):
            return ResponseFactory.error(
                message=str(exc),
                errors=[{"code": "AUTH_ERROR", "message": str(exc)}],
                status=status_code,
                request=request,
            )

        return ResponseFactory.error(
            message=str(exc),
            errors=[{"code": "ERROR", "message": str(exc)}],
            status=status_code,
            request=request,
        )

    logger.exception("Unhandled API exception", exc_info=exc)
    return ResponseFactory.error(
        message="Internal server error",
        errors=[{"code": "SERVER_ERROR", "message": "Internal server error"}],
        status=500,
        request=request,
    )
