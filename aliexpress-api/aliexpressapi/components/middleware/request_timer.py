import time


class RequestTimerMiddleware:
    """
    Middleware to track request processing time (latency).
    Adds request.start_time so we can calculate latency in responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = time.time()
        response = self.get_response(request)
        return response
