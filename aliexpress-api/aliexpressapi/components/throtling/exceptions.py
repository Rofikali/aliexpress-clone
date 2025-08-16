from rest_framework.exceptions import Throttled


class ThrottledError(Throttled):
    default_detail = "Request was throttled."
    default_code = "throttled"

    def __init__(self, wait=None, detail=None, code=None, meta=None):
        super().__init__(wait=wait, detail=detail or self.default_detail, code=code)
        self.meta = meta or {}

    def get_full_details(self):
        data = super().get_full_details()
        if self.meta:
            data["meta"] = self.meta
        return data
