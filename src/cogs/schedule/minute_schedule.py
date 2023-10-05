from datetime import datetime
import os
from discord.ext import commands
from discord.ext import tasks

from enums.last_process_type import LastProcessType
from models.base import SessionLocal
from models.messages import Messages
from models.schedules import Schedules
from models.last_process_times import LastProcessTimes


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
        now = datetime.now()
        if self.channel is None:
            await self.init()

        await self.channel.send('1分メッセージ')

        with SessionLocal() as session:
            (last, now) = LastProcessTimes.select_and_update(
                session,
                LastProcessType.SCHEDULE,
                now
            )
            session.commit()

            schedules = Schedules.select_sinse_last_time(session, last, now)

            for schedule in schedules:
                db_message = Messages.select(session, schedule.message_id)
                if db_message is None:
                    continue

                channel = await self.bot.fetch_channel(schedule.channel_id)
                message = await channel.send(db_message.message_jp)
                if db_message.reactions:
                    for reaction in db_message.reactions.split(","):
                        if reaction:
                            await message.add_reaction(reaction)

    async def init(self):
        channel_id = os.environ['SCHEDULE_CHANNEL_ID']
        self.channel = await self.bot.fetch_channel(channel_id)
        print(f"「{self.channel.name}」に定期発言開始")


async def setup(bot: commands.Bot):
    await bot.add_cog(MinuteSchedule(bot))
