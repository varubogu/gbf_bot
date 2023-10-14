import os

import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

from gbf import models
from gbf.models.session import engine

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
            'cogs.battle.after_reaction',
            'cogs.battle.ultimate_bahamut',
            'cogs.battle.lucifer',
            'cogs.battle.beelzebub',
            'cogs.battle.belial',
            'cogs.battle.super_ultimate_bahamut',
            'cogs.manager.reload_cog',
            'cogs.schedule.minute_schedule',
            'cogs.schedule.schedule_loader',
            'cogs.sync.environ_load',
            'cogs.sync.gspread_load',
            'cogs.sync.gspread_push',
            # 'cogs.sync.gspread_sync',
        ]

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
    async with engine.begin() as conn:
        await models.init_db(conn)
    bot = GbfBot()
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
