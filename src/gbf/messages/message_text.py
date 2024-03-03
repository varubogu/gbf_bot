from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.guild_messages import GuildMessages

from gbf.models.messages import Messages

class MessageText:

    @classmethod
    async def get_replace(
            cls,
            session: AsyncSession,
            guild_id: int,
            message_id: str,
            param_dict: dict[str, str]
    ):
        """
        ギルドID、メッセージID、およびパラメータ辞書を指定して、置換されたメッセージを取得します。

        メッセージ文字列内のプレースホルダーは、パラメータ辞書の値で置換されます。
        プレースホルダーは {key} の形式で、辞書のキーに対応しています。
        辞書の値には文字列が含まれている必要があります。

        Args:
            session (AsyncSession): SQLAlchemyの非同期セッションオブジェクト。
            guild_id (int): ギルドのID。
            message_id (str): メッセージのID。
            param_dict (dict): 置換に使用するパラメータの辞書。

        Returns:
            str: 置換されたメッセージの文字列。
        """
        m = await cls.get(session, guild_id, message_id)
        message = await cls.replace(m.message_jp, param_dict)
        return message

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            guild_id: int | None,
            message_id: str
            ) -> Messages | GuildMessages:
        """
        ギルドIDとメッセージIDを指定して、メッセージを取得します。

        ギルドメッセージが存在する場合は、それを返します。
        ギルドメッセージが存在しない場合は、共通メッセージを返します。

        Args:
            session (AsyncSession): SQLAlchemyの非同期セッションオブジェクト。
            guild_id (int): ギルドのID。
            message_id (str): メッセージのID。

        Returns:
            str: 取得したメッセージの文字列。
        """
        if guild_id is not None:
            m = await GuildMessages.select_single(session, guild_id, message_id)
            if m is not None:
                return m
        m = await Messages.select_single(session, message_id)
        if m is not None:
            return m
        raise KeyError(f'メッセージIDが存在しません:{message_id}')
    
    @classmethod
    async def replace(
            cls,
            message: str,
            param_dict: dict[str, str]
    ):
        """
        メッセージ文字列内のプレースホルダーを辞書の値で置換します。

        プレースホルダーは {key} の形式で、辞書のキーに対応しています。
        辞書の値には文字列が含まれている必要があります。

        Args:
            message (str): 置換するメッセージの文字列。
            param_dict (dict): 置換に使用するパラメータの辞書。

        Returns:
            str: 置換されたメッセージの文字列。
        Example:
        >>> message = "こんにちは、{name}さん。本日は{event}にご招待します。"
        >>> param_dict = {"name": "山田", "event": "パーティー"}
        >>> result = MessageText.replace(message, param_dict)
        >>> print(result)  # 出力: こんにちは、山田さん。本日はパーティーにご招待します。
        """
        for k, v in param_dict.items():
            message = message.replace(f"{{{k}}}", v)
        return message

