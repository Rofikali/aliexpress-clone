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
        success: bool,
        code: int,
        message: str,
        request,
        data=None,
        errors=None,
        meta: dict | None = None,
        cache: str | None = None,
    ) -> Response:
        """
        Core response builder.
        - success: bool
        - code: HTTP status code
        - message: human-readable message
        - request: DRF request object (for tracing)
        - data: payload
        - errors: list of {code, message}
        - meta: pagination / extra info
        - cache: HIT/MISS
        """
        start_time = getattr(request, "_start_time", time.time())

        # Normalize errors: always array of {code, message}
        normalized_errors = []
        if errors:
            for err in errors:
                if isinstance(err, dict) and "code" in err and "message" in err:
                    normalized_errors.append(err)
                elif isinstance(err, str):
                    normalized_errors.append({"code": "UNKNOWN", "message": err})
        elif not success:
            normalized_errors.append({"code": "UNKNOWN", "message": message})

        response = {
            "success": success,
            "code": code,
            "message": message,
            "request": {
                "id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "latency_ms": round((time.time() - start_time) * 1000, 2),
                "region": "Nepal-01",
                "cache": cache if cache else "MISS",
            },
            "meta": meta or {},
            "errors": normalized_errors if normalized_errors else None,
            "data": data,
        }
        return Response(response, status=code)

    # -----------------------
    # Success Responses
    # -----------------------

    @classmethod
    def success_collection(cls,items: list,pagination: dict | None = None,message: str = "Success",status: int = 200,request=None,cache: str | None = None,) -> Response:
        meta = pagination or {}
        return cls._base_response(
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
        return cls._base_response(
            True,
            status,
            message,
            request,
            data=item,
            meta={},
            cache=cache,
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
        return cls._base_response(
            False,
            status,
            message,
            request,
            errors=errors,
            meta={},
            cache=cache,
            data=None,
        )
