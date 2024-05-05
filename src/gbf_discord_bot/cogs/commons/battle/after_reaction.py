
import asyncio
from typing import Tuple
import discord
from sqlalchemy.ext.asyncio import AsyncSession
from discord.ext import commands
from gbf.messages.message_text import MessageText
from gbf.models.session import AsyncSessionLocal
from gbf.models.battle_recruitments import BattleRecruitments
from gbf.models.quests import Quests
from gbf.utils.exception.abort_process_exception import AbortProcessException
from gbf_discord_bot.cogs.commons.battle.battle_type import BattleTypeEnum


class AfterReaction(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(
            self,
            paylood: discord.RawReactionActionEvent
    ):
        if paylood.user_id == self.bot.user.id:
            return

        try:
            async with self.bot.db_lock:
                async with AsyncSessionLocal() as session:
                    (
                        (recruitment, battle_type),
                        message
                    ) = await asyncio.gather(
                        self.fetch_recruitment(session, paylood),
                        self.fetch_reaction_message(paylood)
                    )

                    if recruitment.recruit_end_message_id is not None:
                        return

                    quest = await Quests.select_single(session, recruitment.target_id)

                    reaction_users = await AfterReaction.get_reaction_users(
                        message, battle_type.reactions)

                    if self.bot.user in reaction_users:
                        reaction_users.remove(self.bot.user)

                    # 
                    embed = message.embeds[0]
                    embed.clear_fields()
                    for reaction in message.reactions:
                        user_name = ''
                        async for reaction_user in reaction.users():
                            if self.bot.user == reaction_user:
                                continue
                            if user_name != '':
                                user_name += '  '
                            user_name += reaction_user.mention
                        if user_name == '':
                            user_name = '無し'
                        embed.add_field(name=reaction.emoji, value=user_name)

                    await message.edit(embed=embed)

                    # 全員集まった場合
                    if len(reaction_users) == quest.recruit_count:

                        complete_message = await MessageText.get(
                            session,
                            paylood.guild_id,
                            "MSG00032"
                        )

                        mention = ' '.join(f"{user.mention}" for user in reaction_users)
                        end_message = await message.channel.send(
                            mention + '\n' + complete_message.message_jp,
                            reference=message
                        )
                        recruitment.recruit_end_message_id = end_message.id
                        session.add(recruitment)
                        await session.commit()
        except AbortProcessException:
            # 処理対象外のため正常終了
            pass
        except Exception as e:
            print(f"エラー発生{e}")

    async def fetch_recruitment(
            self,
            session: AsyncSession,
            paylood: discord.RawReactionActionEvent
    ) -> Tuple[BattleRecruitments, BattleTypeEnum]:

        recruitment = await BattleRecruitments.select_single_row_lock(
            session,
            paylood.guild_id,
            paylood.channel_id,
            paylood.message_id
        )

        if recruitment is None:
            # クエスト募集以外のメッセージは正常終了
            raise AbortProcessException()
        battle_type = BattleTypeEnum.find(
            recruitment.battle_type_id)

        return recruitment, battle_type

    async def fetch_reaction_message(
            self,
            paylood: discord.RawReactionActionEvent
    ):
        channel: discord.TextChannel = await self.bot.fetch_channel(paylood.channel_id)
        message = await channel.fetch_message(paylood.message_id)
        if message.author != self.bot.user:
            raise AbortProcessException()
        return message

    @classmethod
    async def get_reaction_users(
            cls,
            message: discord.Message,
            reactions: list[str] | None = None
    ) -> list[discord.Member]:
        """リアクション集計

        Args:
            message (discord.Message): 集計対象のメッセージオブジェクト
            reactions (list[str]): 集計対象のリアクション配列

        Returns:
            [discord.Member]: 集計結果
        """
        reaction_users: list[discord.User | discord.Member] = []
        for r in message.reactions:
            if reactions is None or r.emoji in reactions:
                async for user in r.users():
                    reaction_users.append(user)

        return set(reaction_users)


async def setup(bot: commands.Bot):
    await bot.add_cog(AfterReaction(bot))
