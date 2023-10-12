from datetime import datetime
from gbf.utils.convert_time import convert_time
import pytest


@pytest.mark.asyncio
async def test_hour_minute():
    actual = await convert_time('0:00')
    assert actual == datetime.min

    actual = await convert_time('1:23')
    assert actual == datetime.min.replace(hour=1, minute=23)


@pytest.mark.asyncio
async def test_hour_minute_from_date():
    from_date = datetime(2022, 12, 31, 23, 59, 59)

    actual = await convert_time('0:00', from_date)
    assert actual == datetime(2022, 12, 31, 0, 0, 0)

    actual = await convert_time('1:23', from_date)
    assert actual == datetime(2022, 12, 31, 1, 23)


@pytest.mark.asyncio
async def test_hour_minute_second():
    actual = await convert_time('0:00:00')
    assert actual == datetime.min

    actual = await convert_time('00:00:00')
    assert actual == datetime.min

    actual = await convert_time('4:56:12')
    assert actual == datetime.min.replace(hour=4, minute=56, second=12)


@pytest.mark.asyncio
async def test_hour_minute_second_from_date():
    from_date = datetime(2022, 12, 31, 23, 59, 59)

    actual = await convert_time('0:00:00', from_date)
    assert actual == datetime(2022, 12, 31, 0, 0, 0)

    actual = await convert_time('00:00:00', from_date)
    assert actual == datetime(2022, 12, 31, 0, 0, 0)

    actual = await convert_time('4:56:12', from_date)
    assert actual == datetime(2022, 12, 31, 4, 56, 12)


@pytest.mark.asyncio
async def test_exception():

    # none
    with pytest.raises(Exception):
        await convert_time(None)

    # empty
    with pytest.raises(ValueError):
        await convert_time('')

    # date
    with pytest.raises(ValueError):
        await convert_time('0/1/1')

    # date
    with pytest.raises(ValueError):
        await convert_time('2023/13/1')

    # date
    with pytest.raises(ValueError):
        await convert_time('2023/1/32')

    # invalid hour
    with pytest.raises(ValueError):
        await convert_time('25:00')

    # invalid minute
    with pytest.raises(ValueError):
        await convert_time('10:60')

    # invalid second
    with pytest.raises(ValueError):
        await convert_time('23:59:60')
