import re
from datetime import datetime


def convert_time(
        time_str: str,
        from_day: datetime = None
) -> datetime:
    if not from_day:
        from_day = datetime.min

    matched = re.match(r'(\d{1,2}):(\d{2}):(\d{2})', time_str)
    if matched:
        hour, min, sec = matched.groups()
        return from_day.replace(
            hour=int(hour),
            minute=int(min),
            second=int(sec),
            microsecond=0
        )

    matched = re.match(r'(\d{1,2}):(\d{2})', time_str)
    if matched:
        hour, min = matched.groups()
        return from_day.replace(
            hour=int(hour),
            minute=int(min),
            second=0,
            microsecond=0
        )

    raise Exception("time_strが不正です")
