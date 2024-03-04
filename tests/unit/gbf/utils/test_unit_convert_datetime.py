from datetime import datetime
import pytest
from gbf.utils.convert_datetime import (
    convert_datetime,
    adjust_datetime
)


@pytest.mark.asyncio
async def test_convert_datetime():
    # 正常系
    now = datetime.now()

    actual = await convert_datetime("2022-01-01")
    assert actual == datetime(2022, 1, 1, 0, 0, 0, 0)

    actual = await convert_datetime("2022/12/31")
    assert actual == datetime(2022, 12, 31)

    actual = await convert_datetime("01-01")
    assert actual == datetime(now.year, 1, 1, 0, 0, 0, 0)

    actual = await convert_datetime("12/31")
    assert actual == datetime(now.year, 12, 31, 0, 0, 0, 0)

    actual = await convert_datetime("2021-01-01 23:59:59")
    assert actual == datetime(2021, 1, 1, 23, 59, 59)

    actual = await convert_datetime("2022-01-01 12:00")
    assert actual == datetime(2022, 1, 1, 12, 0)

    # empty系

    # none
    x = await convert_datetime(None)
    assert x is None

    # empty
    x = await convert_datetime('')
    assert x is None

    # 異常系
    # date
    with pytest.raises(ValueError):
        await convert_datetime('2023/1/32')

    # none day
    with pytest.raises(ValueError):
        await convert_datetime('2023/1')

    # invalid hour
    with pytest.raises(ValueError):
        await convert_datetime('25:00')

    # invalid minute
    with pytest.raises(ValueError):
        await convert_datetime('10:60')

    # invalid second
    with pytest.raises(ValueError):
        await convert_datetime('23:59:60')

@pytest.mark.asyncio
async def test_adjust_datetime():
    now = datetime.now()
    default_datetime = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # 過去日付
    actual = await adjust_datetime(datetime(now.year, 1, 1), default_datetime)
    assert actual == datetime(now.year + 1, 1, 1)

    # 当日同時刻
    actual = await adjust_datetime(datetime(now.year, now.month, now.day), default_datetime)
    assert actual == datetime(now.year, now.month, now.day)

    # 当日1ミリ秒経過
    default_datetime_old = default_datetime.replace(microsecond=1)
    actual = await adjust_datetime(datetime(now.year, now.month, now.day, 0, 0, 0, 0), default_datetime_old)
    assert actual == datetime(now.year + 1, now.month, now.day)

    # 未来日付
    actual = await adjust_datetime(datetime(now.year, 12, 31), default_datetime)
    assert actual == datetime(now.year, 12, 31)

