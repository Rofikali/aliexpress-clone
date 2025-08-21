# # from components.responses.base_response import BaseResponse
# from rest_framework.response import Response
# import uuid
# import datetime
# from django.conf import settings
# import time


# class BaseResponse:
#     """
#     Standardized API Response
#     Adds request_id, timestamp, cache_status, region, and latency.
#     """

#     @staticmethod
#     def build(
#         status_label,
#         message,
#         data=None,
#         errors=None,
#         code=200,
#         extra=None,
#         cache_status="MISS",
#         request=None,
#     ):
#         now = datetime.datetime.utcnow().isoformat()
#         payload = {
#             "status": status_label,
#             "message": message,
#             "data": data,
#             "errors": errors,
#             "timestamp": now,
#             "request_id": str(uuid.uuid4()),
#             "cache_status": cache_status,  # HIT / MISS
#             "region": getattr(settings, "REGION", "unknown"),  # server region
#             "latency_ms": None,
#         }

#         # Calculate latency if request timing is available
#         if request and hasattr(request, "start_time"):
#             payload["latency_ms"] = round((time.time() - request.start_time) * 1000, 2)

#         if extra:
#             payload.update(extra)

#         return Response(payload, status=code)

from rest_framework.response import Response
import uuid
import datetime
from django.conf import settings
import time


class BaseResponse:
    """
    Standardized API Response
    Adds request_id, timestamp, cache_status, region, and latency.
    """

    @staticmethod
    def build(
        status_label,
        message,
        data=None,
        errors=None,
        code=200,
        extra=None,
        request=None,
    ):
        now = (
            datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        )

        # Default cache status is MISS
        cache_status = "MISS"

        # If extra contains 'from_cache' = True, mark HIT
        if extra and extra.get("from_cache") is True:
            cache_status = "HIT"

        payload = {
            "status": status_label,
            "message": message,
            "data": data,
            "errors": errors,
            "timestamp": now,
            "request_id": str(uuid.uuid4()),
            "cache_status": cache_status,
            "region": getattr(settings, "REGION", "unknown"),
            "latency_ms": None,
        }

        # Calculate latency if request timing is available
        if request and hasattr(request, "start_time"):
            payload["latency_ms"] = round((time.time() - request.start_time) * 1000, 2)

        if extra:
            payload.update(extra)

        return Response(payload, status=code)
