import pytest
from src.util.environment_eval import environment_eval


@pytest.mark.asyncio
async def test_environment_eval():

    actual = await environment_eval('abc')
    assert actual == 'abc'

    actual = await environment_eval('ab${TEST_VALUE}c')
    assert actual == 'abc'

    actual = await environment_eval('ab${TEST_VALUE}cd${TEST_VALUE}e')
    assert actual == 'abc'

    actual = await environment_eval('ab${TEST_VALUE}cd${TEST_VALUE2}e')
    assert actual == 'abc'
