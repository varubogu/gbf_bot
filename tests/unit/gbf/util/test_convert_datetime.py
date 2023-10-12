from datetime import datetime
import pytest
from gbf.utils.convert_datetime import convert_datetime as cdt


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


@pytest.mark.asyncio
async def test_exception():

    # none
    x = await cdt(None)
    assert x is None

    # empty
    x = await cdt('')
    assert x is None

    # date
    with pytest.raises(ValueError):
        await cdt('2023/1/32')

    # invalid hour
    with pytest.raises(ValueError):
        await cdt('25:00')

    # invalid minute
    with pytest.raises(ValueError):
        await cdt('10:60')

    # invalid second
    with pytest.raises(ValueError):
        await cdt('23:59:60')
