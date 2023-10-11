from datetime import datetime
import pytest
from src.gbf.utils.convert_datetime import convert_datetime as cdt


@pytest.mark.asyncio
async def test_convert_datetime():
    actual = await cdt("2022-01-01")
    assert actual == datetime(2022, 1, 1, 0, 0, 0, 0)

    actual = await cdt("2022/12/31")
    assert actual == datetime(2022, 12, 31)

    actual = await cdt("2021-01-01 23:59:59")
    assert actual == datetime(2021, 1, 1, 23, 59, 59)

    actual = await cdt("2022-01-01 12:00")
    assert actual == datetime(2022, 1, 1, 12, 0)
