from contextvars import ContextVar


request_id: ContextVar[str] = ContextVar("request_id", default="")
trace_id: ContextVar[str] = ContextVar("trace_id", default="")
