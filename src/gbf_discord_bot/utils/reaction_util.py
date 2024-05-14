from typing import Callable, Optional
import discord

class ReactionUtil:

    @classmethod
    async def get_reaction_users(
            cls,
            message: discord.Message,
            exclude_user: Optional[Callable[[Optional[discord.User | discord.Member]], bool]]
    ) -> dict[str, list[discord.User | discord.Member]]:
        """リアクション集計

        Args:
            message (discord.Message): 集計対象のメッセージオブジェクト

        Returns:
            [str: discord.Member]: 集計結果
        """
        reactions: dict[str, list[discord.User | discord.Member]] = {}
        for r in message.reactions:
            reaction_str = str(r)
            reactions[reaction_str] = []
            async for user in r.users():
                if exclude_user is not None and exclude_user(user):
                    continue

                reactions[reaction_str].append(user)

        return reactions

