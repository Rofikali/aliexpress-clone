import re


def parse_rate(rate: str):
    """
    Parse "100/min", "60/second", "3000/hour" -> (capacity, refill_per_sec).
    Token-bucket: capacity tokens, refill evenly over the period.
    """
    if not rate or "/" not in rate:
        raise ValueError(f"Invalid rate: {rate!r}")
    num, period = rate.split("/", 1)
    capacity = int(num)

    period = period.strip().lower()
    m = re.match(
        r"^(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours|d|day|days)$",
        period,
    )
    if not m:
        raise ValueError(f"Invalid period: {rate!r}")

    lookup = {
        "s": 1,
        "sec": 1,
        "second": 1,
        "seconds": 1,
        "m": 60,
        "min": 60,
        "minute": 60,
        "minutes": 60,
        "h": 3600,
        "hr": 3600,
        "hour": 3600,
        "hours": 3600,
        "d": 86400,
        "day": 86400,
        "days": 86400,
    }
    seconds = lookup[m.group(0)]
    refill_per_sec = capacity / float(seconds)
    return capacity, refill_per_sec
