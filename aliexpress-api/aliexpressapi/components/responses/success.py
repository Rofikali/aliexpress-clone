# # components.responses.success

from rest_framework import status
from .base_response import BaseResponse

class SuccessResponse:
    @staticmethod
    def send(data=None, message="Success", status=status.HTTP_200_OK, extra=None, request=None):
        return BaseResponse.build(
            status_label="success",
            message=message,
            data=data,
            status=status,
            extra=extra,
            request=request,   # ✅ Pass request here
        )
