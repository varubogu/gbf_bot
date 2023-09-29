import os
from discord.ext import commands
from discord.ext import tasks


class MinuteSchedule(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None

    def cog_load(self):
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(seconds=60)
    async def loop(self):
        if self.channel is None:
            channel_id = os.environ['SCHEDULE_CHANNEL_ID']
            self.channel = await self.bot.fetch_channel(channel_id)
            print(f"「{self.channel.name}」に定期発言開始")

        await self.channel.send('1分メッセージ')


async def setup(bot: commands.Bot):
    await bot.add_cog(MinuteSchedule(bot))
