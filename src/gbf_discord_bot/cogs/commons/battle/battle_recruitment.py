
import asyncio
from datetime import datetime, timedelta
import discord
from discord import Interaction as Interaction
from discord import app_commands
from discord.ext import commands
from gbf.messages.message_text import MessageText
from gbf.models.quests import Quests
from gbf.models.quests_alias import QuestsAlias

from gbf.models.session import AsyncSessionLocal
from gbf.models.battle_recruitments import BattleRecruitments
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
        self.DEFAULT_TIMEDELTA = timedelta(days=7)

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
        return datetime.now() + self.DEFAULT_TIMEDELTA

    async def _quest_autocompolete(
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
            battle_type: BT
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
        m = await MessageText.replace(m.message_jp, {'quest_name': quest.quest_name})

        await interaction.followup.send(m)
        return await interaction.original_response()

    async def _add_reaction(self, message, battle_type: BT):
        for reaction in battle_type.reactions:
            await message.add_reaction(reaction)

    async def _regist(
            self,
            message: discord.Message,
            quest: Quests,
            battle_type: BT = None,
            _expiry_date: datetime = None
    ):
        record = BattleRecruitments()
        record.guild_id = message.guild.id
        record.channel_id = message.channel.id
        record.message_id = message.id
        record.expiry_date = _expiry_date or self._default_expiry_date()
        record.target_id = quest.target_id
        record.battle_type_id = battle_type.type_value

        async with AsyncSessionLocal() as session:
            session.add(record)
            await session.commit()

    @app_commands.command(name="recruit", description="マルチバトルを募集します")
    @app_commands.autocomplete(quest=_quest_autocompolete)
    async def recruitment(
            self,
            interaction: Interaction,
            quest: str,
            battle_type: BT = BT.DEFAULT,
            expiry_date: str = None
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

            if expiry_date is None:
                expiry_date = await self._default_expiry_date()

            message = await self._send_message(interaction, target, battle_type)
            await self._add_reaction(message, battle_type)

            await self._regist(message, target, battle_type, expiry_date)
        except Exception as e:
            print(e)
            await interaction.followup.send('エラーが発生しました', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(BattleRecruitmentCog(bot))
