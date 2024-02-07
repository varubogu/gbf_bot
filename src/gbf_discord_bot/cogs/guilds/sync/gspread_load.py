import discord
from discord import app_commands
from discord.ext import commands
from gbf.environment.environment_singleton import EnvironmentSingleton
from gbf.models.session import AsyncSessionLocal
from gbf.schedules.manager import ScheduleManager
from gbf.sync.db.register import DbRegister
from gbf.sync.gspread.loader import GSpreadLoader
from sqlalchemy.ext.asyncio import AsyncSession


class GSpreadLoad(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.init_message = "スプレッドシートからデータ読み込み中..."
        self.complete_message = "スプレッドシートからデータ読み込み完了"
        self.error_message = "スプレッドシートからデータ読み込み失敗"

    @app_commands.command(
            name="gspread_load",
            description="スプレッドシートからデータ読み込み"
    )
    @app_commands.checks.has_role("gbf_bot_control")
    async def command_execute(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            await interaction.followup.send(self.init_message)
            await self.execute(interaction)
            await interaction.followup.send(self.complete_message)
        except Exception as e:
            await interaction.followup.send(self.error_message)
            print(e)
            raise

    async def execute(self, interaction: discord.Interaction):
        loader = GSpreadLoader()
        await loader.open()

        register = DbRegister()
        db_model = dict()

        for table_dif in loader.core.table_definition:

            if table_dif.table_io != 'in':
                continue

            await interaction.followup.send(
                f'{table_dif.table_name_jp} load...'
            )

            worksheet = loader.core.book.worksheet(table_dif.table_name_jp)
            data = worksheet.get_all_records()
            table_model = await loader.convert_table(data, table_dif)

            if len(table_model) == 0:
                continue

            db_model[table_dif.table_name_en] = table_model

        await interaction.followup.send(
            'table writes...'
        )

        async with self.bot.db_lock:
            async with AsyncSessionLocal() as session:
                for key, table_model in db_model.items():
                    table_name_jp = [
                        table_dif.table_name_jp
                        for table_dif
                        in loader.core.table_definition
                        if table_dif.table_name_en == key
                    ]

                    await interaction.followup.send(
                        f'{table_name_jp[0]} write...'
                    )
                    await register.regist(session, table_model)

            await self.after(session)

    async def after(
            self,
            session: AsyncSession
    ):
        # シングルトン再読み込み
        env = EnvironmentSingleton()
        await env.load_db(session)

        # スケジュール再計算
        register = ScheduleManager()
        await register.event_schedule_clear(session)
        await register.event_schedule_create(session)
        await session.commit()



async def setup(bot: commands.Bot):
    await bot.add_cog(GSpreadLoad(bot))
