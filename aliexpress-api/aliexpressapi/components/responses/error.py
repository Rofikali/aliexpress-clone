# # components.responses.error
# from rest_framework import status
# from .base_response import BaseResponse


# class ErrorResponse:
#     @staticmethod
#     def send(
#         message="Error", errors=None, code=status.HTTP_400_BAD_REQUEST, extra=None
#     ):
#         return BaseResponse.build(
#             status_label="error", message=message, errors=errors, code=code, extra=extra
#         )

from rest_framework import status
from .base_response import BaseResponse


class ErrorResponse:
    @staticmethod
    def send(
        message="Error",
        errors=None,
        code=status.HTTP_400_BAD_REQUEST,
        extra=None,
        request=None,
    ):
        return BaseResponse.build(
            status_label="error",
            message=message,
            errors=errors,
            code=code,
            extra=extra,
            request=request,  # ✅ Pass request here
        )
