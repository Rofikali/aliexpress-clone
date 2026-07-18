import json
import logging
from datetime import UTC, datetime

from components.observability.context import request_id, trace_id


class JsonFormatter(logging.Formatter):
    reserved_fields = set(logging.makeLogRecord({}).__dict__) | {
        "message",
        "asctime",
    }

    def format(self, record):
        payload = {
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id.get() or None,
            "trace_id": trace_id.get() or None,
        }
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in self.reserved_fields and not key.startswith("_")
            }
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str, separators=(",", ":"))
