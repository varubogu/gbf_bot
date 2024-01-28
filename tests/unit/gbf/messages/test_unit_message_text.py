import pytest
from gbf.messages.message_text import MessageText

class TestUnitMessageText:

    @pytest.mark.asyncio
    async def test_replace_single(self):
        message = 'Hello, {name}!'
        param_dict = {'name': 'World'}

        message_text = MessageText()
        result = await message_text.replace(message, param_dict)

        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_replace_double(self):
        message = '{name}, {name}!'
        param_dict = {'name': 'World'}

        message_text = MessageText()
        result = await message_text.replace(message, param_dict)

        assert result == 'World, World!'

    @pytest.mark.asyncio
    async def test_replace_multi(self):
        message = '{id}, {name}!'
        param_dict = {
            'id': 'Hello',
            'name': 'World'
        }

        message_text = MessageText()
        result = await message_text.replace(message, param_dict)

        assert result == 'Hello, World!'
