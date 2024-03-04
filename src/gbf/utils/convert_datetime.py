from datetime import datetime
import re


async def convert_datetime(date_str: str) -> datetime | None:
    if not date_str:
        return None
    now = datetime.now()

    pattern = (
        r'(?:\b(?P<year>\d{4})[-/])?(?P<month>\d{1,2})[-/](?P<day>\d{1,2})'
        r'(?: (?P<hour>\d{1,2}):(?P<minute>\d{1,2})(?::(?P<second>\d{1,2}))?)?'
    )
    match = re.match(pattern, date_str)

    if not match:
        raise ValueError(f"時間'{date_str}'は認識されるフォーマットではありません")

    # マッチした情報を取得
    parts = match.groupdict()

    # 非Noneの部分を整数に変換
    parts = {k: int(v) for k, v in parts.items() if v is not None}
    if 'year' not in parts:
        parts['year'] = now.year


    return datetime(**parts)


async def convert_recruit_datetime(
        datetime_str: str,
        default_datetime: datetime = datetime.now()
) -> datetime:
    result = await convert_datetime(datetime_str)
    
    if isinstance(result, datetime):
        result = await adjust_datetime(result, default_datetime)
        return result

    raise ValueError("入力形式が正しくありません: " + datetime_str)

async def adjust_datetime(result: datetime, default_datetime: datetime) -> datetime:
    """
    指定された日時オブジェクトが基準日よりも前の日時担ってしまう場合、年を調整します。

    Args:
        result (datetime): 調整する日時オブジェクト
        default_datetime (datetime): 基準日の日時オブジェクト

    Returns:
        datetime: 調整された日時オブジェクト
    """
    if result < default_datetime:
        result = result.replace(year=default_datetime.year + 1)
    return result