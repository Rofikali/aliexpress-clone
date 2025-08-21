# # components.responses.success
# from rest_framework import status
# from .base_response import BaseResponse


# class SuccessResponse:
#     @staticmethod
#     def send(data=None, message="Success", code=status.HTTP_200_OK, extra=None):
#         return BaseResponse.build(
#             status_label="success", message=message, data=data, code=code, extra=extra
#         )

from rest_framework import status
from .base_response import BaseResponse

class SuccessResponse:
    @staticmethod
    def send(data=None, message="Success", code=status.HTTP_200_OK, extra=None, request=None):
        return BaseResponse.build(
            status_label="success",
            message=message,
            data=data,
            code=code,
            extra=extra,
            request=request,   # ✅ Pass request here
        )
