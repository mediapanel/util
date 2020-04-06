"""
Utility function for formatting a datetime.timedelta as a string.
"""
from datetime import timedelta


def _make_plural(count: int, modifier: str, extention: str = "s") -> str:
    if count == 1:
        return str(count) + " " + modifier
    return str(count) + " " + modifier + extention


def human_readable(td: timedelta) -> str:
    if td.days > 30:  # x months
        return _make_plural(td.days // 30, "month")
    elif td.days > 0:  # x days
        return _make_plural(td.days, "day")
    elif td.seconds > 3600:  # x hours
        return _make_plural(td.seconds // 3600, "hour")
    else:  # x minutes
        return _make_plural(td.seconds // 60, "minute")
