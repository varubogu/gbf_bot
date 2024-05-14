
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
from gbf_discord_bot.utils.reaction_util import ReactionUtil
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

                    quest = await Quests.select_single(session, recruitment.target_id)

                    # Botユーザーは除外してリアクションとユーザーの一覧を取得
                    reactions = await ReactionUtil.get_reaction_users(
                        message,
                        lambda user: user == self.bot.user
                    )
                    reaction_users = await AfterReaction.get_reaction_users(
                        reactions,
                        battle_type.reactions
                    )

                    # 参加者一覧を作成
                    embed = message.embeds[0]
                    embed.clear_fields()
                    await self.embed_quest_members(reactions, embed)
                    await message.edit(embed=embed)

                    # 全員集まった場合
                    if len(reaction_users) == quest.recruit_count:
                        if recruitment.recruit_end_message_id is not None:
                            return

                        complete_message = await MessageText.get(
                            session,
                            paylood.guild_id,
                            "MSG00032"
                        )

                        # 参加者にメンションを出す
                        mention = ' '.join(f"{user.mention}" for user in reaction_users)
                        end_message = await message.channel.send(
                            mention + '\n' + complete_message.message_jp,
                            reference=message
                        )

                        # 全員集まったメッセージを登録（一度だけメッセージを出す）
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
        """
        募集情報と戦闘タイプをフェッチする

        Args:
            session (AsyncSession): データベースセッション
            paylood (discord.RawReactionActionEvent): リアクションイベントのペイロード

        Raises:
            AbortProcessException: 募集情報が見つからない場合に発生

        Returns:
            Tuple[BattleRecruitments, BattleTypeEnum]: 募集情報と戦闘タイプ
        """

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
        """
        リアクションが付けられたメッセージを取得する

        Args:
            paylood (discord.RawReactionActionEvent): リアクションイベントのペイロード

        Raises:
            AbortProcessException: ボット自身が投稿したメッセージでない場合に発生

        Returns:
            discord.Message: リアクションが付けられたメッセージオブジェクト
        """
        channel: discord.TextChannel = await self.bot.fetch_channel(paylood.channel_id)
        message = await channel.fetch_message(paylood.message_id)
        if message.author != self.bot.user:
            raise AbortProcessException()
        return message

    @classmethod
    async def get_reaction_users(
            cls,
            reactions: dict[str, list[discord.User | discord.Member]],
            target_reactions: list[str] | None = None
    ) -> set[discord.User | discord.Member]:
        """全てのリアクションからユーザーを抽出する

        Args:
            message (discord.Message): 集計対象のメッセージオブジェクト
            reactions (list[str]): 集計対象のリアクション配列

        Returns:
            [discord.Member]: 集計結果
        """
        reaction_users: list[discord.User | discord.Member] = []
        for reaction, users  in reactions.items():
            if target_reactions is None or reaction in target_reactions:
                for user in users:
                    reaction_users.append(user)

        return set(reaction_users)

    async def embed_quest_members(self, reactions, embed):
        """
        埋め込みメッセージにクエスト参加者(メンション)一覧を追加する

        Args:
            reactions (dict[str, list[discord.User | discord.Member]]): リアクションとそれに対応するユーザーの辞書
            embed (discord.Embed): 更新する埋め込みメッセージ
        """
        EMPTY = ''
        for reaction, users in reactions.items():
            user_names = EMPTY
            for reaction_user in users:
                if user_names != EMPTY:
                    # 複数人の場合は間隔を空ける
                    user_names += '  '
                user_names += reaction_user.mention
            if user_names == EMPTY:
                user_names = '無し'
            embed.add_field(name=reaction, value=user_names)


async def setup(bot: commands.Bot):
    await bot.add_cog(AfterReaction(bot))
