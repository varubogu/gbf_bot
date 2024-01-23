import os

import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# 環境変数読み込み
dotenv_filepath = os.path.join(os.environ['CONFIG_FOLDER'], '.env')
load_dotenv(override=True, dotenv_path=dotenv_filepath)

# 自分の Bot のアクセストークン
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents.all()


class GbfBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='/gbf',
            intents=intents
        )

        self.INITIAL_EXTENSIONS = [
            'cogs.sample',
            'cogs.commons.battle.after_reaction',
            'cogs.commons.battle.battle_recruitment',
            'cogs.commons.manager.reload_cog',
            'cogs.commons.schedule.minute_schedule',
            'cogs.commons.schedule.schedule_loader',
            'cogs.commons.sync.environ_load',
            'cogs.commons.sync.gspread_load',
            'cogs.commons.sync.gspread_push',
            # 'cogs.sync.gspread_sync',
        ]
        self.db_lock = asyncio.Lock()

    async def on_ready(self):
        print('gbf_bot is online')

    async def load_cogs(self, extensions):
        for extension in extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f'{extension}の読み込みでエラー発生 {e}')

    async def setup_hook(self):
        await self.load_cogs(self.INITIAL_EXTENSIONS)
        await self.tree.sync()

    async def close(self):
        await super().close()


async def main():
    from gbf import models
    from gbf.models.session import engine

    async with engine.begin() as conn:
        await models.init_db(conn)
    bot = GbfBot()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
