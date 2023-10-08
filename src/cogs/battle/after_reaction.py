
import asyncio
import discord
from discord.ext import commands
from models.model_base import SessionLocal
from models.battle_recruitments import BattleRecruitments
from util.exception.abort_process_exception import AbortProcessException
from cogs.battle.target_enum import Target
from cogs.battle.battle_type import BattleTypeEnum


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

            (
                (recruitment, battle_type, target),
                message
            ) = await asyncio.gather(
                self.fetch_recruitment(paylood),
                self.fetch_reaction_message(paylood)
            )

            reaction_users = await self.get_reaction_users(
                message, battle_type.reactions)

            if self.bot.user in reaction_users:
                reaction_users.remove(self.bot.user)

            if len(reaction_users) == target.recruit_count:
                mention = ''.join(f"{user.mention}" for user in reaction_users)
                await message.channel.send(
                    mention + '\nメンバーが揃いました。',
                    reference=message
                )
        except AbortProcessException:
            # 処理対象外のため正常終了
            pass
        except Exception as e:
            print(f"エラー発生{e}")

    async def fetch_recruitment(
            self,
            paylood: discord.RawReactionActionEvent
    ) -> (BattleRecruitments, BattleTypeEnum, Target):

        with SessionLocal() as session:
            recruitment = BattleRecruitments.select(
                session,
                paylood.guild_id,
                paylood.channel_id,
                paylood.message_id
            )

        if recruitment is None:
            raise AbortProcessException()
        battle_type = BattleTypeEnum.find(
            recruitment.battle_type_id)

        target = Target.find_target(recruitment.target_id)
        if target is None:
            raise Exception('Target is none')
        return recruitment, battle_type, target

    async def fetch_reaction_message(
            self,
            paylood: discord.RawReactionActionEvent
    ):
        channel = await self.bot.fetch_channel(paylood.channel_id)
        message = await channel.fetch_message(paylood.message_id)
        if message.author != self.bot.user:
            raise AbortProcessException()
        return message

    async def get_reaction_users(
            self,
            message: discord.Message,
            reactions: list[str]
    ) -> [discord.Member]:
        """リアクション集計

        Args:
            message (discord.Message): 集計対象のメッセージオブジェクト
            reactions (list[str]): 集計対象のリアクション配列

        Returns:
            [discord.Member]: 集計結果
        """
        reaction_users = []
        for r in message.reactions:
            if r.emoji in reactions:
                async for user in r.users():
                    reaction_users.append(user)

        return set(reaction_users)


async def setup(bot: commands.Bot):
    await bot.add_cog(AfterReaction(bot))
