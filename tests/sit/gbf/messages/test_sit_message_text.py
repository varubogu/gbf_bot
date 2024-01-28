import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.messages.message_text import MessageText
from gbf.models.guild_messages import GuildMessages
from gbf.models.messages import Messages

class TestSitMessageText:

    @pytest.mark.asyncio
    async def test_get_common(self, mocker, async_db_session: AsyncSession):
        """
        このテストは、ギルドメッセージが存在しない場合に共通メッセージを取得する機能をテストします。
        """
        mock_guild_messages_select = mocker.patch.object(GuildMessages, 'select_single', new_callable=AsyncMock)
        mock_messages_select = mocker.patch.object(Messages, 'select_single', new_callable=AsyncMock)
        
        guild_id = 1
        message_id = 'test_id'
        mock_guild_messages_select.return_value = None
        mock_messages_select.return_value = 'message'

        message_text = MessageText()
        result = await message_text.get(async_db_session, guild_id, message_id)

        assert result == 'message'
        mock_guild_messages_select.assert_called_once_with(async_db_session, guild_id, message_id)
        mock_messages_select.assert_called_once_with(async_db_session, message_id)

    @pytest.mark.asyncio
    async def test_get_guild(self, mocker, async_db_session: AsyncSession):
        """
        このテストは、ギルドメッセージが存在する場合にそのメッセージを取得する機能をテストします。
        """
        mock_guild_messages_select = mocker.patch.object(GuildMessages, 'select_single', new_callable=AsyncMock)
        mock_messages_select = mocker.patch.object(Messages, 'select_single', new_callable=AsyncMock)
        
        guild_id = 1
        message_id = 'test_id'
        mock_guild_messages_select.return_value = 'guild_message'
        mock_messages_select.return_value = None

        message_text = MessageText()
        result = await message_text.get(async_db_session, guild_id, message_id)

        assert result == 'guild_message'
        mock_guild_messages_select.assert_called_once_with(async_db_session, guild_id, message_id)
        mock_messages_select.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_guild_override(self, mocker, async_db_session: AsyncSession):
        """
        このテストは、ギルドメッセージが存在し、共通メッセージも存在する場合に、
        ギルドメッセージが優先されることを確認する機能をテストします。
        """

        mock_guild_messages_select = mocker.patch.object(GuildMessages, 'select_single', new_callable=AsyncMock)
        mock_messages_select = mocker.patch.object(Messages, 'select_single', new_callable=AsyncMock)
        
        guild_id = 1
        message_id = 'test_id'
        mock_guild_messages_select.return_value = 'guild_message'
        mock_messages_select.return_value = 'message'

        message_text = MessageText()
        result = await message_text.get(async_db_session, guild_id, message_id)

        assert result == 'guild_message'
        mock_guild_messages_select.assert_called_once_with(async_db_session, guild_id, message_id)
        mock_messages_select.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_not_found(self, mocker, async_db_session: AsyncSession):
        """
        このテストは、メッセージIDが存在しない場合に例外が発生することを確認します。
        """
        mock_guild_messages_select = mocker.patch.object(GuildMessages, 'select_single', new_callable=AsyncMock)
        mock_messages_select = mocker.patch.object(Messages, 'select_single', new_callable=AsyncMock)
        
        guild_id = 1
        message_id = 'not_exist_id'
        mock_guild_messages_select.return_value = None
        mock_messages_select.return_value = None

        message_text = MessageText()
        with pytest.raises(KeyError) as e:
            await message_text.get(async_db_session, guild_id, message_id)

        assert str(e.value.args[0]) == f'メッセージIDが存在しません:{message_id}'
        mock_guild_messages_select.assert_called_once_with(async_db_session, guild_id, message_id)
        mock_messages_select.assert_called_once_with(async_db_session, message_id)