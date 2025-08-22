# aliexpressapi/utils/encoders.py

import json
from uuid import UUID
from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    """
    Custom JSON encoder to safely handle UUID and other Django-specific types.
    Converts UUID objects to strings for JSON serialization.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)  # Convert UUID to string
        return super().default(obj)


def dumps(data):
    """
    Wrapper for json.dumps using CustomJSONEncoder.
    """
    return json.dumps(data, cls=CustomJSONEncoder)


def loads(data):
    """
    Wrapper for json.loads (just passthrough for symmetry).
    """
    return json.loads(data)
