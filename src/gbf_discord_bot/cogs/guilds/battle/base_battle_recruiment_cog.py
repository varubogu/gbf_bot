
from datetime import datetime, timedelta
import discord
from discord import Interaction as Interaction
from discord.ext import commands

from gbf.models.session import AsyncSessionLocal
from gbf.models.battle_recruitments import BattleRecruitments
from gbf_discord_bot.cogs.guilds.battle.target_enum import Target
from gbf_discord_bot.cogs.guilds.battle.battle_type import BattleTypeEnum as BT


class BaseBattleRecruitmentCog(commands.Cog):

    def __init__(
            self,
            bot: commands.Bot,
            target: Target

    ):
        self.__bot = bot
        self.__target = target

    @property
    def bot(self) -> discord.ext.commands.Bot:
        return self.__bot

    @property
    def target(self) -> Target:
        return self.__target

    async def recruitment(
            self,
            interaction: Interaction,
            battle_type: BT = BT.DEFAULT
    ):
        message = await self._send_message(interaction, battle_type)
        await self._add_reaction(message, battle_type)
        await self._regist(message, battle_type)

    async def _send_message(self, interaction: Interaction, battle_type: BT):
        m = f"{self.target.quest_alias}の参加者を募集します。"
        if battle_type == BT.ALL_ELEMENT:
            m += '\n参加属性を選んでください'
        await interaction.response.send_message(m)
        return await interaction.original_response()

    async def _add_reaction(self, message, battle_type: BT):
        for reaction in battle_type.reactions:
            await message.add_reaction(reaction)

    async def _regist(self, message: discord.Message, battle_type: BT):
        record = BattleRecruitments()
        record.guild_id = message.guild.id
        record.channel_id = message.channel.id
        record.message_id = message.id
        record.expiry_date = datetime.now() + timedelta(days=7)
        record.target_id = self.target.target_id
        record.battle_type_id = battle_type.type_value

        async with AsyncSessionLocal() as session:
            session.add(record)
            await session.commit()
