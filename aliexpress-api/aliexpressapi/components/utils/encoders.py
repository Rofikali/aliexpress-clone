# # aliexpressapi/utils/encoders.py

# import json
# from uuid import UUID
# from django.core.serializers.json import DjangoJSONEncoder


# class CustomJSONEncoder(DjangoJSONEncoder):
#     """
#     Custom JSON encoder to safely handle UUID and other Django-specific types.
#     Converts UUID objects to strings for JSON serialization.
#     """

#     def default(self, obj):
#         if isinstance(obj, UUID):
#             return str(obj)  # Convert UUID to string
#         return super().default(obj)


# def dumps(data):
#     """
#     Wrapper for json.dumps using CustomJSONEncoder.
#     """
#     return json.dumps(data, cls=CustomJSONEncoder)


# def loads(data):
#     """
#     Wrapper for json.loads (just passthrough for symmetry).
#     """
#     return json.loads(data)


# aliexpressapi/utils/encoders.py

import json
from uuid import UUID
from decimal import Decimal
from datetime import datetime, date
from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    """
    JSON encoder for Django objects, UUID, Decimal, datetime, and date.
    Converts unsupported objects to safe JSON types for caching.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def dumps(data) -> str:
    """
    JSON serialize data using CustomJSONEncoder.
    Returns a UTF-8 string ready for caching.
    """
    return json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)


def loads(data: str):
    """
    Deserialize JSON string from cache back to Python objects.
    """
    if data is None:
        return None
    return json.loads(data)
