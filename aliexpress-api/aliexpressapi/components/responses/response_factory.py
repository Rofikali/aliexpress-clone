# components/responses/response_factory.py
from rest_framework.response import Response
from uuid import uuid4
from datetime import datetime
import time


class ResponseFactory:
    @staticmethod
    def _base_response(
        status_str,
        success,
        code,
        message,
        request,
        data=None,
        errors=None,
        # extra=None,
        cache=None,
    ):
        start_time = getattr(request, "_start_time", time.time())

        response = {
            "status": status_str,
            "success": success,
            "code": code,
            "message": message,
            "request": {
                "id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "latency_ms": round((time.time() - start_time) * 1000, 2),
                "region": "Nepal-01",
                "cache": cache if cache else "MISS",  # ✅ auto defaults to MISS
            },
            # "meta": extra or {},
            **(data or {}),  # ✅ always expand a dict
            "errors": errors,
        }
        return Response(response, status=code)

    @classmethod
    def success(
        cls,
        data=None,
        message="Success",
        status_code=200,
        request=None,
        # extra=None,
        cache=None,
    ):
        return cls._base_response(
            "success",
            True,
            status_code,
            message,
            request,
            data=data,
            # extra=extra,
            cache=cache,
        )

    @classmethod
    def error(
        cls,
        message="Error",
        errors=None,
        status_code=400,
        request=None,
        # extra=None,
        cache=None,
    ):
        return cls._base_response(
            "error",
            False,
            status_code,
            message,
            request,
            errors=errors,
            # extra=extra,
            cache=cache,
        )
