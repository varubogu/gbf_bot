
import asyncio
from datetime import datetime
from typing import Optional
import discord
from discord import Interaction as Interaction
from discord import app_commands
from discord.ext import commands
from gbf.messages.message_text import MessageText
from gbf.models.quests import Quests
from gbf.models.quests_alias import QuestsAlias

from gbf.models.session import AsyncSessionLocal
from gbf.models.battle_recruitments import BattleRecruitments
from gbf.schedules.manager import ScheduleManager
from gbf.utils.convert_datetime import convert_recruit_datetime
from gbf_discord_bot.cogs.commons.battle.battle_type \
    import BattleTypeEnum as BT


class BattleRecruitmentCog(commands.Cog):

    def __init__(
            self,
            bot: commands.Bot

    ):
        self.__bot = bot
        self.quests = None
        self.quest_aliases = None
        self.choices = None

    @property
    def bot(self) -> commands.Bot:
        return self.__bot

    async def cog_load(self) -> None:
        async with AsyncSessionLocal() as session:
            q, qa = await asyncio.gather(
                Quests.select_all(session),
                QuestsAlias.select_all(session)
            )

        self.quests = q
        self.quest_aliases = qa
        self.choices = {
            app_commands.Choice(name=alias.alias, value=alias.alias)
            for alias in self.quest_aliases
        }

    async def _default_expiry_date(self) -> datetime:
        now = datetime.now()
        now = now.replace(hour=21, minute=0, second=0, microsecond=0)
        return now

    async def _quest_autocomplete(
            self,
            interaction: Interaction,
            current: str
    ) -> list[app_commands.Choice[str]]:
        """オートコンプリート文字列を返す

        Args:
            interaction (Interaction): Discord応答
            current (str): 入力中の文字列

        Returns:
            list[app_commands.Choice[str]]: _description_
        """

        try:
            results = [
                choice for choice in self.choices
                if current in choice.name
            ]
        except Exception as e:
            print(f"battle_recruitmentのsuggestでエラー：{e}")
            return []

        return results

    async def _get_quest(self, quest_alias: str) -> Quests:
        try:
            return [
                q for q in self.quests
                for qa in self.quest_aliases
                if qa.alias == quest_alias and q.target_id == qa.target_id
            ][0]
        except Exception as e:
            print(f"battle_recruitmentの_send_messageの対象クエスト取得部分でエラー：{e}")
            raise

    async def _send_message(
            self,
            interaction: Interaction,
            quest: Quests,
            battle_type: BT,
            event_date: datetime = None
    ):
        if battle_type == BT.ALL_ELEMENT:
            message_id = "MSG00029"
        else:
            message_id = "MSG00028"

        async with AsyncSessionLocal() as session:
            m = await MessageText.get(
                session,
                interaction.guild_id,
                message_id
            )
        m = await MessageText.replace(
            str(m.message_jp),
            {'quest_name': str(quest.quest_name)}
        )
        if event_date is not None:
            m += f"\n開催日時：{event_date.strftime('%m/%d %H:%M')}"

        embed = discord.Embed(title='参加者一覧', description='')
        embed.add_field(name="", value="現在参加者はいません。")

        await interaction.followup.send(m, embed=embed)
        return await interaction.original_response()

    async def _add_reaction(self, message, battle_type: BT):
        for reaction in battle_type.reactions:
            await message.add_reaction(reaction)

    async def _regist(
            self,
            message: discord.Message,
            quest: Quests,
            battle_type: BT = None,
            _event_date: datetime = None
    ):
        recruitment = BattleRecruitments()
        recruitment.guild_id = message.guild.id
        recruitment.channel_id = message.channel.id
        recruitment.message_id = message.id
        recruitment.expiry_date = _event_date
        recruitment.target_id = quest.target_id
        recruitment.battle_type_id = battle_type.type_value

        sm = ScheduleManager()
        (schedule, rs) = await sm.convert_global_recruitment(recruitment)

        async with AsyncSessionLocal() as session:
            session.add(recruitment)
            session.add(schedule)
            session.add(rs)
            await session.commit()


    @app_commands.command(name="recruit", description="マルチバトルを募集します")
    @app_commands.describe(
        quest="募集するクエスト",
        battle_type="クエストの攻略方法",
        event_date="クエスト開始日時(月/日 時:分)"
    )
    @app_commands.autocomplete(quest=_quest_autocomplete)
    async def recruitment(
            self,
            interaction: Interaction,
            quest: str,
            battle_type: BT = BT.DEFAULT,
            event_date: Optional[str] = None
    ):
        try:
            await interaction.response.defer()

            target = await self._get_quest(quest)

            # 初期値の場合は上書き
            if battle_type == BT.DEFAULT:
                try:
                    battle_type = BT.find(int(target.default_battle_type))
                except ValueError as e:
                    print(f"battle_recruitmentのbattle_typeの初期値設定部分でエラー：{e}")
                    battle_type = BT.DEFAULT

            if event_date is None:
                event_date_datetime = await self._default_expiry_date()
            else:
                try:
                    event_date_datetime = await convert_recruit_datetime(event_date)
                except Exception:
                    raise ValueError('event_dateが日時として認識できません')

            message = await self._send_message(interaction, target, battle_type, event_date_datetime)
            await self._add_reaction(message, battle_type)

            await self._regist(message, target, battle_type, event_date_datetime)
        except ValueError as e:
            print(e)
            await interaction.followup.send(f'エラーが発生しました {e}', ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.followup.send('不明なエラーが発生しました', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(BattleRecruitmentCog(bot))
