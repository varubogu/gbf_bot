import os
from datetime import datetime
from discord.ext import commands, tasks

from gbf.schedules.minute_executor import MinuteScheduleExecutor
from gbf.models.messages import Messages
from gbf.models.session import AsyncSessionLocal


class MinuteSchedule(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None
        self.executor = MinuteScheduleExecutor()

    def cog_load(self):
        self.loop.start()

    def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(seconds=60)
    async def loop(self):
        now = datetime.now()
        if self.channel is None:
            await self.init()

        if self.bot.is_ready():
            return

        async with AsyncSessionLocal() as session:

            schedules = await self.executor.fetch_schedules(session, now)
            message_ids = [schedule.message_id for schedule in schedules]
            db_messages = await Messages.select_multi(session, message_ids)

            for schedule in schedules:
                db_message: Messages = next(
                    (m for m in db_messages
                        if m.message_id == schedule.message_id),
                    None)

                if db_message is None:
                    continue

                channel = await self.bot.fetch_channel(schedule.channel_id)
                message = await channel.send(db_message.message_jp)
                if db_message.reactions:
                    for reaction in db_message.reactions.split(","):
                        if reaction:
                            await message.add_reaction(reaction)

    async def init(self):
        channel_id = os.environ.get('SCHEDULE_CHANNEL_ID', None)
        self.channel = await self.bot.fetch_channel(channel_id)
        print(f"「{self.channel.name}」に定期発言開始")


async def setup(bot: commands.Bot):
    await bot.add_cog(MinuteSchedule(bot))