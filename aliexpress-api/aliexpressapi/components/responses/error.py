# # components.responses.error
from rest_framework import status
from .base_response import BaseResponse


class ErrorResponse:
    @staticmethod
    def send(
        message="Error",
        errors=None,
        status=status.HTTP_400_BAD_REQUEST,
        extra=None,
        request=None,
    ):
        return BaseResponse.build(
            status_label="error",
            message=message,
            errors=errors,
            status=status,
            extra=extra,
            request=request,  # ✅ Pass request here
        )
