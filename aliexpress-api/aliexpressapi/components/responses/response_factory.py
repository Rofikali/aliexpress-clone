# # # components/responses/response_factory.py
# # from rest_framework.response import Response
# # from uuid import uuid4
# # from datetime import datetime
# # import time


# # class ResponseFactory:
# #     @staticmethod
# #     def _base_response(
# #         status_str,
# #         success,
# #         code,
# #         message,
# #         request,
# #         data=None,
# #         errors=None,
# #         # extra=None,
# #         cache=None,
# #     ):
# #         start_time = getattr(request, "_start_time", time.time())

# #         response = {
# #             "status": status_str,
# #             "success": success,
# #             "code": code,
# #             "message": message,
# #             "request": {
# #                 "id": str(uuid4()),
# #                 "timestamp": datetime.utcnow().isoformat(),
# #                 "latency_ms": round((time.time() - start_time) * 1000, 2),
# #                 "region": "Nepal-01",
# #                 "cache": cache if cache else "MISS",  # ✅ auto defaults to MISS
# #             },
# #             # "meta": extra or {},
# #             **(data or {}),  # ✅ always expand a dict
# #             "errors": errors,
# #         }
# #         return Response(response, status=code)

# #     @classmethod
# #     def success(
# #         cls,
# #         data=None,
# #         message="Success",
# #         status_code=200,
# #         request=None,
# #         # extra=None,
# #         cache=None,
# #     ):
# #         return cls._base_response(
# #             "success",
# #             True,
# #             status_code,
# #             message,
# #             request,
# #             data=data,
# #             # extra=extra,
# #             cache=cache,
# #         )

# #     @classmethod
# #     def error(
# #         cls,
# #         message="Error",
# #         errors=None,
# #         status_code=400,
# #         request=None,
# #         # extra=None,
# #         cache=None,
# #     ):
# #         return cls._base_response(
# #             "error",
# #             False,
# #             status_code,
# #             message,
# #             request,
# #             errors=errors,
# #             # extra=extra,
# #             cache=cache,
# #         )


# # # components/responses/response_factory.py
# # """
# # Centralized API response factory.

# # ✅ Features:
# #  - Consistent JSON response schema across the project
# #  - Latency, request ID, timestamp, region, cache status
# #  - Handles both success + error responses
# #  - Prevents data collisions (keeps "data" namespace clean)
# #  - Extensible: can add meta, pagination, trace IDs later

# # Usage:
# #     return ResponseFactory.success(data={"products": [...]}, request=request)
# #     return ResponseFactory.error(message="Invalid credentials", status_code=401, request=request)
# # """

# # from rest_framework.response import Response
# # from uuid import uuid4
# # from datetime import datetime
# # import time


# # class ResponseFactory:
# #     @staticmethod
# #     def _base_response(
# #         status: str,
# #         success: bool,
# #         code: int,
# #         message: str,
# #         request,
# #         data: dict = None,
# #         errors: dict | list | None = None,
# #         meta: dict | None = None,
# #         cache: str | None = None,
# #     ) -> Response:
# #         """
# #         Private builder for the consistent response payload.
# #         """
# #         start_time = getattr(request, "_start_time", time.time())

# #         response = {
# #             "status": status,  # "success" | "error"
# #             "success": success,
# #             "code": code,
# #             "message": message,
# #             "request": {
# #                 "id": str(uuid4()),  # unique per response
# #                 "timestamp": datetime.utcnow().isoformat() + "Z",
# #                 "latency_ms": round((time.time() - start_time) * 1000, 2),
# #                 "region": "Nepal-01",  # TODO: make configurable via settings
# #                 "cache": cache or "MISS",
# #             },
# #             "meta": meta or {},
# #             "errors": errors or None,
# #             "data": data or {},
# #         }
# #         return Response(response, status=code)

# #     # -----------------------
# #     # Public convenience APIs
# #     # -----------------------

# #     @classmethod
# #     def success(
# #         cls,
# #         data: dict = None,
# #         message: str = "Success",
# #         status: int = 200,
# #         request=None,
# #         meta: dict | None = None,
# #         cache: str | None = None,
# #     ) -> Response:
# #         """
# #         Success response factory.
# #         """
# #         return cls._base_response(
# #             "success",
# #             True,
# #             status,
# #             message,
# #             request,
# #             data=data,
# #             meta=meta,
# #             cache=cache,
# #         )

# #     @classmethod
# #     def error(
# #         cls,
# #         message: str = "Error",
# #         errors: dict | list | None = None,
# #         status: int = 400,
# #         request=None,
# #         meta: dict | None = None,
# #         cache: str | None = None,
# #     ) -> Response:
# #         """
# #         Error response factory.
# #         """
# #         return cls._base_response(
# #             "error",
# #             False,
# #             status,
# #             message,
# #             request,
# #             errors=errors,
# #             meta=meta,
# #             cache=cache,
# #         )

# # components/responses/response_factory.py
# """
# Centralized API response factory.

# ✅ Features:
#  - Consistent JSON response schema across the project
#  - Auto-detects collections (arrays) vs single resources (objects)
#  - JSON:API / REST-friendly: arrays for collections, objects for resources
#  - Adds request metadata (latency, region, cache, trace ID)
#  - Handles success + error in one place
# """

# from rest_framework.response import Response
# from uuid import uuid4
# from datetime import datetime
# import time


# class ResponseFactory:
#     @staticmethod
#     def _base_response(
#         status: str,
#         success: bool,
#         code: int,
#         message: str,
#         request,
#         data=None,
#         errors: dict | list | None = None,
#         meta: dict | None = None,
#         cache: str | None = None,
#     ) -> Response:
#         """
#         Private builder for consistent response payload.
#         """
#         start_time = getattr(request, "_start_time", time.time())

#         # --- Normalize data ---
#         normalized_data = None
#         if data is None:
#             normalized_data = None
#         elif isinstance(data, (list, tuple)):
#             # ✅ Collection response
#             normalized_data = list(data)
#         elif isinstance(data, dict):
#             # ✅ Already object response
#             normalized_data = data
#         else:
#             # ✅ Wrap scalars (id, string, etc.) in object
#             normalized_data = {"value": data}

#         response = {
#             "status": status,  # "success" | "error"
#             "success": success,
#             "code": code,
#             "message": message,
#             "request": {
#                 "id": str(uuid4()),
#                 "timestamp": datetime.utcnow().isoformat() + "Z",
#                 "latency_ms": round((time.time() - start_time) * 1000, 2),
#                 "region": "Nepal-01",  # TODO: configurable
#                 "cache": cache or "MISS",
#             },
#             "meta": meta or {},
#             "errors": errors or None,
#             "data": normalized_data,
#         }
#         return Response(response, status=code)

#     # -----------------------
#     # Public factories
#     # -----------------------

#     @classmethod
#     def success(
#         cls,
#         data=None,
#         message: str = "Success",
#         status: int = 200,
#         request=None,
#         meta: dict | None = None,
#         cache: str | None = None,
#     ) -> Response:
#         return cls._base_response(
#             "success",
#             True,
#             status,
#             message,
#             request,
#             data=data,
#             meta=meta,
#             cache=cache,
#         )

#     @classmethod
#     def error(
#         cls,
#         message: str = "Error",
#         errors: dict | list | None = None,
#         status: int = 400,
#         request=None,
#         meta: dict | None = None,
#         cache: str | None = None,
#     ) -> Response:
#         return cls._base_response(
#             "error",
#             False,
#             status,
#             message,
#             request,
#             data=None,
#             errors=errors,
#             meta=meta,
#             cache=cache,
#         )


# components/responses/response_factory.py
from rest_framework.response import Response
from uuid import uuid4
from datetime import datetime
import time


class ResponseFactory:
    """
    Centralized API Response Factory.

    ✅ Consistent JSON schema for all responses
    ✅ Handles success + error
    ✅ Always includes request tracing info
    ✅ Production-grade (inspired by GitHub / Stripe APIs)
    """

    @staticmethod
    def _base_response(
        status: str,
        success: bool,
        code: int,
        message: str,
        request,
        data=None,
        errors=None,
        meta: dict | None = None,
        cache: str | None = None,
    ) -> Response:
        start_time = getattr(request, "_start_time", time.time())

        response = {
            "status": status,  # "success" | "error"
            "success": success,
            "code": code,
            "message": message,
            "request": {
                "id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "latency_ms": round((time.time() - start_time) * 1000, 2),
                "region": "Nepal-01",  # TODO: make configurable
                # "cache": cache or "MISS",
                "cache": cache if cache else "MISS",  # ✅ auto defaults to MISS
            },
            "meta": meta or {},
            "errors": errors if errors else None,
            "data": data,
        }
        return Response(response, status=code)

    # -----------------------
    # Success Responses
    # -----------------------

    @classmethod
    def success_collection(
        cls,
        items: list,
        pagination: dict | None = None,
        message: str = "Success",
        status: int = 200,
        request=None,
        cache: str | None = None,
    ) -> Response:
        """
        Success response for collection resources.
        """
        meta = pagination or {}
        return cls._base_response(
            "success",
            True,
            status,
            message,
            request,
            data=items,
            meta=meta,
            cache=cache,
        )

    @classmethod
    def success_resource(
        cls,
        item: dict,
        message: str = "Success",
        status: int = 200,
        request=None,
        cache: str | None = None,
    ) -> Response:
        """
        Success response for single resource.
        """
        return cls._base_response(
            "success", True, status, message, request, data=item, meta={}, cache=cache
        )

    # -----------------------
    # Error Responses
    # -----------------------

    @classmethod
    def error(
        cls,
        message: str = "Error",
        errors: list | None = None,
        status: int = 400,
        request=None,
        cache: str | None = None,
    ) -> Response:
        """
        Error response factory.
        """
        normalized_errors = errors or [{"code": "UNKNOWN", "message": message}]
        return cls._base_response(
            "error",
            False,
            status,
            message,
            request,
            errors=normalized_errors,
            meta={},
            cache=cache,
            data=None,
        )
