import os

import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

import models

# 環境変数読み込み
load_dotenv()

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
            'cogs.sync.gspread_sync',
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
    models.init_db()

if __name__ == "__main__":
    asyncio.run(main())
    bot = GbfBot()
    bot.run(DISCORD_TOKEN)
