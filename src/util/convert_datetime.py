from datetime import datetime
import re


async def convert_datetime(date_str: str):
    if not date_str:
        return None

    pattern = (
        r'(?P<year>\d{4})[-/](?P<month>\d{1,2})[-/](?P<day>\d{1,2})'
        r'(?: (?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?::(?P<second>\d{1,2}))?)?'
    )
    match = re.match(pattern, date_str)

    if not match:
        raise ValueError(f"時間'{date_str}'は認識されるフォーマットではありません")

    # マッチした情報を取得
    parts = match.groupdict()

    # 非Noneの部分を整数に変換
    parts = {k: int(v) for k, v in parts.items() if v is not None}

    return datetime(**parts)
